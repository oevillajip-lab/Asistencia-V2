from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import NumericProperty

# LIBRERÍA DE CÁMARA MODERNA (Evita errores de compilación)
from camera4kivy import Preview

# =======================================================
# ⚠️ PEGA TU URL DE GOOGLE APPS SCRIPT AQUÍ
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzsn2osZ82UQtX9yd-MtCuh1Im4Fk6ypxSpNz7i9nDpTAvFTHKW3FW7iKCYhHgtv0l/exec"
# =======================================================

KV = '''
#:import hex kivy.utils.get_color_from_hex

<LoadingSpinner@Widget>:
    angle: 0
    canvas.before:
        PushMatrix
        Rotate:
            angle: self.angle
            origin: self.center
    canvas:
        Color:
            rgba: 0, 0.7, 1, 1  # Azul brillante
        Line:
            circle: (self.center_x, self.center_y, 15, 0, 300) # Círculo incompleto (arco)
            width: 2.5
    canvas.after:
        PopMatrix

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
                rgba: 0.1, 0.1, 0.1, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        # Espaciador arriba
        Widget:
            size_hint_y: 0.4

        Image:
            source: 'logo.png'
            size_hint: None, None
            size: dp(100), dp(100) # Aprox 2.5cm
            pos_hint: {'center_x': 0.5}
            allow_stretch: True

        LoadingSpinner:
            id: spinner
            size_hint: None, None
            size: dp(40), dp(40)
            pos_hint: {'center_x': 0.5}
        
        # Espaciador abajo
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
            size: dp(80), dp(80)
            pos_hint: {'center_x': 0.5}

        Label:
            text: 'CONTROL DE ACCESO'
            font_size: '24sp'
            bold: True
            size_hint_y: None
            height: dp(50)
            color: 1, 1, 1, 1

        Widget: # Espacio flexible
            size_hint_y: 0.1

        Button:
            text: '📸 ESCANEAR QR'
            font_size: '20sp'
            background_color: 0, 0.6, 1, 1
            size_hint_y: None
            height: dp(80)
            on_release: app.iniciar_camara()

        Button:
            text: '➕ NUEVO ASISTENTE'
            font_size: '20sp'
            background_color: 0, 0.8, 0, 1
            size_hint_y: None
            height: dp(80)
            on_release: app.root.current = 'form'
        
        Widget: # Espacio final

<ScannerScreen>:
    name: 'scanner'
    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            id: camera_layout
            size_hint_y: 0.85
        
        Button:
            text: 'VOLVER AL MENÚ'
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
                rgba: 0.12, 0.12, 0.12, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: 'REGISTRO MANUAL'
            font_size: '22sp'
            bold: True
            size_hint_y: None
            height: 50

        TextInput:
            id: ti_nombre
            hint_text: 'Nombre'
            multiline: False
            size_hint_y: None
            height: dp(50)

        TextInput:
            id: ti_id
            hint_text: 'ID (Número QR)'
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
            text: 'CANCELAR'
            background_color: 0.4, 0.4, 0.4, 1
            size_hint_y: None
            height: dp(50)
            on_release: app.root.current = 'menu'
'''

class AsistenciaApp(App):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        # 1. ANIMAR SPINNER
        splash_screen = self.root.get_screen('splash')
        spinner = splash_screen.ids.spinner
        anim = Animation(angle=-360, duration=1.5, t='linear')
        anim += Animation(angle=-720, duration=1.5, t='linear') # Gira continuo
        anim.repeat = True
        anim.start(spinner)

        # 2. ESPERAR 3 SEGUNDOS Y CAMBIAR A MENÚ
        Clock.schedule_once(self.ir_al_menu, 3)
        
        self.camera = None
        self.permisos_android()

    def ir_al_menu(self, *args):
        self.root.current = 'menu'

    # --- CÁMARA ---
    def iniciar_camara(self):
        self.root.current = 'scanner'
        if not self.camera:
            screen = self.root.get_screen('scanner')
            # Camera4Kivy Preview (Más estable)
            self.camera = Preview(letterbox_ratio=16/9)
            self.camera.connect_camera(enable_analyze_pixels=True, default_zoom=0.0)
            screen.ids.camera_layout.add_widget(self.camera)

    def detener_camara(self):
        if self.camera:
            self.camera.disconnect_camera()
            screen = self.root.get_screen('scanner')
            screen.ids.camera_layout.remove_widget(self.camera)
            self.camera = None
        self.root.current = 'menu'

    # CALLBACK DE ESCANEO (Camera4Kivy)
    def analyze_pixels_callback(self, pixels, size, pos, scale, mirror):
        # Para evitar problemas de compilación con ZBar ahora mismo,
        # dejaremos la cámara solo como "Visualizador" en este paso.
        # Si esto compila bien, en el siguiente paso activamos el lector QR real.
        pass

    # --- COMUNICACIÓN GOOGLE ---
    def enviar_formulario(self):
        s = self.root.get_screen('form')
        nom = s.ids.ti_nombre.text
        uid = s.ids.ti_id.text
        cel = s.ids.ti_cel.text
        emp = s.ids.ti_empresa.text
        
        if not nom or not uid:
            self.mostrar_popup("Error", "Nombre e ID son obligatorios")
            return

        import urllib.parse
        params = urllib.parse.urlencode({'action':'nuevo','nombre':nom,'id':uid,'celular':cel,'empresa':emp})
        
        self.mostrar_popup("Guardando...", "Enviando datos...")
        UrlRequest(f"{GOOGLE_SCRIPT_URL}?{params}", on_success=self.res_exito, on_failure=self.res_error, on_error=self.res_error)

    def res_exito(self, req, result):
        texto = result if isinstance(result, str) else result.decode('utf-8')
        self.mostrar_popup("Éxito", texto)
        self.root.current = 'menu'
        # Limpiar
        s = self.root.get_screen('form')
        s.ids.ti_nombre.text = ""
        s.ids.ti_id.text = ""

    def res_error(self, req, error):
        self.mostrar_popup("Error", "Revisa tu internet")

    def mostrar_popup(self, t, m):
        Popup(title=t, content=Label(text=m), size_hint=(0.8, 0.4)).open()

    def permisos_android(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA, Permission.INTERNET])

if __name__ == '__main__':
    AsistenciaApp().run()
