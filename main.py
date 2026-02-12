from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from camera4kivy import Preview

# =======================================================
# TU URL DEL SHEET (La que probamos en el navegador)
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxXJc1hd8v4mw_LiSn6E6RzT4pTsnv40DhQBLTl_uDD17wLSv5BffObXFBsaPBMBR0Y/exec"
# =======================================================

KV = '''
ScreenManager:
    SplashScreen:
    MenuScreen:
    ScannerScreen:
    FormScreen:

<SplashScreen>:
    name: 'splash'
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        spacing: 20
        canvas.before:
            Color:
                rgba: 0.08, 0.08, 0.08, 1  # Fondo Oscuro Elegante
            Rectangle:
                pos: self.pos
                size: self.size
        
        # Espaciador para centrar verticalmente
        Widget:
            size_hint_y: 0.4

        # TU LOGO (Pequeño y centrado)
        Image:
            source: 'logo.png'
            size_hint: None, None
            size: dp(100), dp(100)  # Tamaño controlado (aprox 2cm)
            pos_hint: {'center_x': 0.5}
            allow_stretch: True
            keep_ratio: True

        # TEXTO ANIMADO
        Label:
            id: lbl_loading
            text: "Iniciando"
            font_size: '18sp'
            color: 0.8, 0.8, 0.8, 1
            size_hint_y: None
            height: dp(30)
        
        Widget:
            size_hint_y: 0.4

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
        
        Image:
            source: 'logo.png'
            size_hint: None, None
            size: dp(60), dp(60)
            pos_hint: {'center_x': 0.5}

        Label:
            text: 'CONTROL DE ACCESO'
            font_size: '22sp'
            bold: True
            size_hint_y: None
            height: dp(40)

        Button:
            text: '📸 ESCANEAR QR'
            font_size: '18sp'
            background_color: 0, 0.6, 1, 1
            on_release: app.iniciar_camara()

        Button:
            text: '➕ NUEVO ASISTENTE'
            font_size: '18sp'
            background_color: 0, 0.8, 0, 1
            on_release: app.root.current = 'form'

<ScannerScreen>:
    name: 'scanner'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            id: camera_layout
            size_hint_y: 0.85
        Button:
            text: 'VOLVER'
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
            hint_text: 'ID (DNI/QR)'
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
        self.camera = None
        self.dots = ""
        self.request_android_permissions()
        
        # Animación de puntitos (...)
        Clock.schedule_interval(self.animar_puntos, 0.5)
        # Cambiar al menú a los 3 segundos
        Clock.schedule_once(self.ir_al_menu, 3)

    def animar_puntos(self, dt):
        self.dots += "."
        if len(self.dots) > 3: self.dots = ""
        try:
            # Actualizamos el texto del Label en Splash
            self.root.get_screen('splash').ids.lbl_loading.text = f"Iniciando{self.dots}"
        except: pass

    def ir_al_menu(self, *args):
        self.root.current = 'menu'

    def iniciar_camara(self):
        # Pedimos permisos de nuevo por si acaso
        self.request_android_permissions()
        self.root.current = 'scanner'
        
        # Iniciar cámara segura
        if not self.camera:
            try:
                self.camera = Preview(letterbox_ratio=16/9)
                self.camera.connect_camera(enable_analyze_pixels=True)
                self.root.get_screen('scanner').ids.camera_layout.add_widget(self.camera)
            except Exception as e:
                self.popup("Error Cámara", "Reinicia la App y acepta permisos.")

    def detener_camara(self):
        if self.camera:
            self.camera.disconnect_camera()
            self.root.get_screen('scanner').ids.camera_layout.remove_widget(self.camera)
            self.camera = None
        self.root.current = 'menu'

    def analyze_pixels_callback(self, pixels, size, pos, scale, mirror):
        # Aquí iría la lógica de lectura, pero primero aseguramos que no crashee
        pass

    def enviar_formulario(self):
        s = self.root.get_screen('form')
        # ... Logica de envio igual que antes ...
        d = {'action': 'nuevo', 'nombre': s.ids.ti_nombre.text, 'id': s.ids.ti_id.text, 
             'celular': s.ids.ti_cel.text, 'empresa': s.ids.ti_empresa.text}
        
        if not d['nombre'] or not d['id']:
            self.popup("Error", "Faltan datos")
            return
            
        import urllib.parse
        UrlRequest(f"{GOOGLE_SCRIPT_URL}?{urllib.parse.urlencode(d)}", 
                   on_success=self.exito, on_failure=self.error, on_error=self.error)

    def exito(self, req, res):
        self.popup("Éxito", "Guardado Correctamente")
        self.root.current = 'menu'

    def error(self, req, err):
        self.popup("Error", "Fallo de conexión")

    def popup(self, t, m):
        Popup(title=t, content=Label(text=str(m)), size_hint=(0.8, 0.4)).open()

    def request_android_permissions(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.CAMERA, 
                Permission.RECORD_AUDIO, 
                Permission.INTERNET, 
                Permission.WRITE_EXTERNAL_STORAGE
            ])

if __name__ == '__main__':
    AsistenciaApp().run()
