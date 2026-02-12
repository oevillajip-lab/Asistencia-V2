from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.animation import Animation
from camera4kivy import Preview

# =======================================================
# TU NUEVA URL ACTUALIZADA
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxXJc1hd8v4mw_LiSn6E6RzT4pTsnv40DhQBLTl_uDD17wLSv5BffObXFBsaPBMBR0Y/exec"
# =======================================================

KV = '''
<LoadingSpinner@Widget>:
    angle: 0
    canvas.before:
        PushMatrix
        Rotate:
            angle: self.angle
            origin: self.center
    canvas:
        Color:
            rgba: 0, 0.7, 1, 1
        Line:
            circle: (self.center_x, self.center_y, 20, 0, 320)
            width: 3
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
        canvas.before:
            Color:
                rgba: 0.05, 0.05, 0.05, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        Widget:
            size_hint_y: 0.4
        
        Image:
            source: 'logo.png'
            size_hint: None, None
            size: dp(150), dp(150)
            pos_hint: {'center_x': 0.5}
            allow_stretch: True
            keep_ratio: True

        Widget:
            size_hint_y: 0.1

        LoadingSpinner:
            id: spinner
            size_hint: None, None
            size: dp(50), dp(50)
            pos_hint: {'center_x': 0.5}
        
        Label:
            text: "Cargando Sistema..."
            color: 0.7, 0.7, 0.7, 1
            font_size: '14sp'
        
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
            size: dp(100), dp(100)
            pos_hint: {'center_x': 0.5}

        Label:
            text: 'CONTROL DE ACCESO'
            font_size: '24sp'
            bold: True
            size_hint_y: None
            height: dp(40)

        Button:
            text: '📸 ESCANEAR QR'
            font_size: '20sp'
            background_color: 0, 0.6, 1, 1
            on_release: app.iniciar_camara()

        Button:
            text: '➕ NUEVO ASISTENTE'
            font_size: '20sp'
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
        spacing: 10
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
        # Animación Spinner
        splash = self.root.get_screen('splash')
        anim = Animation(angle=-360, duration=1, t='linear')
        anim += Animation(angle=0, duration=0)
        anim.repeat = True
        anim.start(splash.ids.spinner)

        # Esperar 4 segundos y pasar al menú
        Clock.schedule_once(self.ir_menu, 4)
        self.camera = None
        self.permisos()

    def ir_menu(self, *args):
        self.root.current = 'menu'

    def iniciar_camara(self):
        self.root.current = 'scanner'
        if not self.camera:
            self.camera = Preview(letterbox_ratio=16/9)
            self.camera.connect_camera(enable_analyze_pixels=True)
            self.root.get_screen('scanner').ids.camera_layout.add_widget(self.camera)

    def detener_camara(self):
        if self.camera:
            self.camera.disconnect_camera()
            self.root.get_screen('scanner').ids.camera_layout.remove_widget(self.camera)
            self.camera = None
        self.root.current = 'menu'

    def analyze_pixels_callback(self, pixels, size, pos, scale, mirror):
        # Escaneo desactivado por ahora para probar estabilidad de la app
        pass

    def enviar_formulario(self):
        s = self.root.get_screen('form')
        d = {
            'action': 'nuevo',
            'nombre': s.ids.ti_nombre.text,
            'id': s.ids.ti_id.text,
            'celular': s.ids.ti_cel.text,
            'empresa': s.ids.ti_empresa.text
        }
        if not d['nombre'] or not d['id']:
            self.popup("Error", "Faltan datos")
            return
        
        import urllib.parse
        self.popup("Enviando...", "Espere...")
        UrlRequest(f"{GOOGLE_SCRIPT_URL}?{urllib.parse.urlencode(d)}", 
                   on_success=self.exito, on_failure=self.error, on_error=self.error)

    def exito(self, req, res):
        self.popup("Éxito", str(res))
        self.root.get_screen('form').ids.ti_nombre.text = ""
        self.root.current = 'menu'

    def error(self, req, err):
        self.popup("Error", "Fallo de conexión")

    def popup(self, t, m):
        Popup(title=t, content=Label(text=str(m)), size_hint=(0.8, 0.4)).open()

    def permisos(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA, Permission.INTERNET, Permission.RECORD_AUDIO])

if __name__ == '__main__':
    AsistenciaApp().run()
