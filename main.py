from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window

# --- IMPORTACIÓN SEGURA ---
# No importamos la cámara aquí arriba para evitar crashes al inicio.
# La importaremos solo cuando se pulse el botón.

# =======================================================
# TU URL (VERIFICADA)
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxXJc1hd8v4mw_LiSn6E6RzT4pTsnv40DhQBLTl_uDD17wLSv5BffObXFBsaPBMBR0Y/exec"
# =======================================================

KV = '''
ScreenManager:
    MenuScreen:
    ScannerScreen:
    FormScreen:

<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        canvas.before:
            Color:
                rgba: 0.1, 0.1, 0.1, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        # LOGO EN EL MENU
        Image:
            source: 'logo.png'
            size_hint: None, None
            size: dp(100), dp(100)
            pos_hint: {'center_x': 0.5}

        Label:
            text: 'CONTROL DE ACCESO'
            font_size: '24sp'
            bold: True
            size_hint_y: None
            height: dp(50)

        Button:
            text: '📸 ESCANEAR QR'
            font_size: '20sp'
            background_color: 0, 0.6, 1, 1
            on_release: app.ir_a_scanner()

        Button:
            text: '➕ NUEVO ASISTENTE'
            font_size: '20sp'
            background_color: 0, 0.8, 0, 1
            on_release: app.root.current = 'form'

<ScannerScreen>:
    name: 'scanner'
    BoxLayout:
        orientation: 'vertical'
        # Aquí se insertará la cámara por código
        BoxLayout:
            id: camera_placeholder
            size_hint_y: 0.85
        
        Button:
            text: 'VOLVER / DETENER'
            size_hint_y: 0.15
            background_color: 1, 0, 0, 1
            on_release: app.detener_camara()

<FormScreen>:
    name: 'form'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        canvas.before:
            Color:
                rgba: 0.15, 0.15, 0.15, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: 'REGISTRO MANUAL'
            font_size: '22sp'
            size_hint_y: None
            height: 40

        TextInput:
            id: ti_nombre
            hint_text: 'Nombre'
            multiline: False
            size_hint_y: None
            height: dp(50)
        
        TextInput:
            id: ti_id
            hint_text: 'ID'
            input_filter: 'int'
            multiline: False
            size_hint_y: None
            height: dp(50)

        TextInput:
            id: ti_cel
            hint_text: 'Celular'
            input_filter: 'int'
            multiline: False
            size_hint_y: None
            height: dp(50)
        
        TextInput:
            id: ti_empresa
            hint_text: 'Empresa'
            multiline: False
            size_hint_y: None
            height: dp(50)

        Button:
            text: 'GUARDAR'
            bold: True
            background_color: 0, 0.8, 0, 1
            size_hint_y: None
            height: dp(60)
            on_release: app.enviar_formulario()

        Button:
            text: 'VOLVER'
            background_color: 0.5, 0.5, 0.5, 1
            size_hint_y: None
            height: dp(50)
            on_release: app.root.current = 'menu'
'''

class AsistenciaApp(App):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        self.camera_widget = None
        # PEDIR PERMISOS NADA MAS ARRANCAR
        self.pedir_permisos()

    def pedir_permisos(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            # Pedimos todo de una vez
            request_permissions([
                Permission.CAMERA, 
                Permission.RECORD_AUDIO, 
                Permission.INTERNET, 
                Permission.WRITE_EXTERNAL_STORAGE
            ])

    def ir_a_scanner(self):
        # Solo al pulsar este botón intentamos cargar la cámara
        self.root.current = 'scanner'
        # Pequeño retraso para dejar que la UI cambie antes de cargar la cámara pesada
        Clock.schedule_once(self.iniciar_camara_segura, 0.2)

    def iniciar_camara_segura(self, dt):
        if self.camera_widget: return
        
        try:
            # Importación LOCAL para que si falla, no rompa la app al inicio
            from camera4kivy import Preview
            
            self.camera_widget = Preview(letterbox_ratio=16/9)
            # Conectar hardware
            self.camera_widget.connect_camera(enable_analyze_pixels=True)
            # Agregar a la pantalla
            screen = self.root.get_screen('scanner')
            screen.ids.camera_placeholder.add_widget(self.camera_widget)
            
        except Exception as e:
            self.popup("Error de Cámara", f"No se pudo iniciar: {str(e)}\nVerifica permisos.")

    def detener_camara(self):
        if self.camera_widget:
            try:
                self.camera_widget.disconnect_camera()
                screen = self.root.get_screen('scanner')
                screen.ids.camera_placeholder.remove_widget(self.camera_widget)
                self.camera_widget = None
            except: pass
        self.root.current = 'menu'

    # Callback de lectura de QR (Placeholder para que no de error)
    def analyze_pixels_callback(self, pixels, size, pos, scale, mirror):
        pass

    def enviar_formulario(self):
        s = self.root.get_screen('form')
        d = {'action': 'nuevo', 'nombre': s.ids.ti_nombre.text, 'id': s.ids.ti_id.text, 
             'celular': s.ids.ti_cel.text, 'empresa': s.ids.ti_empresa.text}
        
        if not d['nombre'] or not d['id']:
            self.popup("Atención", "Nombre e ID obligatorios")
            return

        import urllib.parse
        self.popup("Enviando...", "Conectando con Google...")
        UrlRequest(f"{GOOGLE_SCRIPT_URL}?{urllib.parse.urlencode(d)}", 
                   on_success=self.exito, on_failure=self.error, on_error=self.error)

    def exito(self, req, res):
        self.popup("¡Guardado!", "Registro exitoso")
        self.root.get_screen('form').ids.ti_nombre.text = ""
        self.root.current = 'menu'

    def error(self, req, err):
        self.popup("Error", "No hay internet o falló Google")

    def popup(self, t, m):
        Popup(title=t, content=Label(text=str(m)), size_hint=(0.8, 0.4)).open()

if __name__ == '__main__':
    AsistenciaApp().run()
