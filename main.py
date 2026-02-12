# MODO A PRUEBA DE FALLOS
try:
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.uix.screenmanager import ScreenManager, Screen
    from kivy.clock import Clock
    from kivy.utils import platform
    from kivy.uix.popup import Popup
    from kivy.uix.label import Label
    from kivy.network.urlrequest import UrlRequest
    import traceback # Para cazar el error
except Exception as e:
    # Si falla algo básico, no podemos hacer nada, pero esto es raro.
    pass

# URL DE TU SHEET (Verificada)
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxXJc1hd8v4mw_LiSn6E6RzT4pTsnv40DhQBLTl_uDD17wLSv5BffObXFBsaPBMBR0Y/exec"

KV = '''
ScreenManager:
    SplashScreen:
    ErrorScreen:
    MenuScreen:
    ScannerScreen:
    FormScreen:

<ErrorScreen>:
    name: 'error'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        canvas.before:
            Color:
                rgba: 0.8, 0, 0, 1 # FONDO ROJO DE ALERTA
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: "¡OCURRIÓ UN ERROR!"
            font_size: '24sp'
            bold: True
            size_hint_y: None
            height: 50
        ScrollView:
            Label:
                id: error_label
                text: "Esperando..."
                text_size: self.width, None
                size_hint_y: None
                height: self.texture_size[1]
        Button:
            text: "COPIAR / SALIR"
            size_hint_y: None
            height: 50
            on_release: app.stop()

<SplashScreen>:
    name: 'splash'
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        spacing: 20
        canvas.before:
            Color:
                rgba: 0.08, 0.08, 0.08, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        Widget:
            size_hint_y: 0.4

        # TU LOGO PEQUEÑO Y CENTRADO
        Image:
            source: 'logo.png'
            size_hint: None, None
            size: dp(100), dp(100)
            pos_hint: {'center_x': 0.5}
            allow_stretch: True
            keep_ratio: True

        # TEXTO "Iniciando..."
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
            on_release: app.ir_scanner()

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
            id: camera_placeholder
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
            on_release: app.enviar()
        Button:
            text: 'VOLVER'
            background_color: 0.5, 0.5, 0.5, 1
            size_hint_y: None
            height: dp(50)
            on_release: app.root.current = 'menu'
'''

class AsistenciaApp(App):
    def build(self):
        # Capturamos errores globales
        import sys
        sys.excepthook = self.handle_exception
        return Builder.load_string(KV)

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        # SI OCURRE UN ERROR, MOSTRAMOS LA PANTALLA ROJA EN LUGAR DE CERRAR
        error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        try:
            self.root.current = 'error'
            self.root.get_screen('error').ids.error_label.text = error_msg
        except:
            print("Error critico:", error_msg)

    def on_start(self):
        try:
            self.camera_widget = None
            self.dots = ""
            
            # Pedir permisos inmediatamente
            self.pedir_permisos()
            
            # Animacion texto
            Clock.schedule_interval(self.animar, 0.5)
            # Pasar al menu a los 3 seg
            Clock.schedule_once(self.ir_menu, 3)
            
        except Exception as e:
            self.handle_exception(type(e), e, e.__traceback__)

    def pedir_permisos(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA, Permission.RECORD_AUDIO, Permission.INTERNET, Permission.WRITE_EXTERNAL_STORAGE])

    def animar(self, dt):
        self.dots += "."
        if len(self.dots) > 3: self.dots = ""
        try: self.root.get_screen('splash').ids.lbl_loading.text = f"Iniciando{self.dots}"
        except: pass

    def ir_menu(self, dt):
        self.root.current = 'menu'

    def ir_scanner(self):
        self.root.current = 'scanner'
        # Importamos camara DENTRO de un try para atrapar el error si faltan drivers
        try:
            Clock.schedule_once(self.iniciar_camara_real, 0.2)
        except Exception as e:
            self.handle_exception(type(e), e, e.__traceback__)

    def iniciar_camara_real(self, dt):
        if self.camera_widget: return
        try:
            from camera4kivy import Preview
            self.camera_widget = Preview(letterbox_ratio=16/9)
            self.camera_widget.connect_camera(enable_analyze_pixels=True)
            self.root.get_screen('scanner').ids.camera_placeholder.add_widget(self.camera_widget)
        except Exception as e:
            self.handle_exception(type(e), e, e.__traceback__)

    def detener_camara(self):
        if self.camera_widget:
            try:
                self.camera_widget.disconnect_camera()
                self.root.get_screen('scanner').ids.camera_placeholder.remove_widget(self.camera_widget)
                self.camera_widget = None
            except: pass
        self.root.current = 'menu'

    def enviar(self):
        try:
            s = self.root.get_screen('form')
            d = {'action':'nuevo', 'nombre':s.ids.ti_nombre.text, 'id':s.ids.ti_id.text, 
                 'celular':s.ids.ti_cel.text, 'empresa':s.ids.ti_empresa.text}
            
            if not d['nombre'] or not d['id']:
                self.popup("Error", "Faltan datos")
                return

            import urllib.parse
            UrlRequest(f"{GOOGLE_SCRIPT_URL}?{urllib.parse.urlencode(d)}", 
                       on_success=self.exito, on_failure=self.error, on_error=self.error)
        except Exception as e:
            self.handle_exception(type(e), e, e.__traceback__)

    def exito(self, req, res):
        self.popup("Éxito", "Guardado")
        self.root.current = 'menu'

    def error(self, req, err):
        self.popup("Error", "Fallo de conexión")

    def popup(self, t, m):
        Popup(title=t, content=Label(text=str(m)), size_hint=(0.8, 0.4)).open()

    def analyze_pixels_callback(self, pixels, size, pos, scale, mirror):
        pass

if __name__ == '__main__':
    try:
        AsistenciaApp().run()
    except Exception as e:
        # Ultimo recurso si falla al arrancar
        print("CRASH FATAL")
