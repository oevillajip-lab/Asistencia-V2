from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy_garden.zbarcam import ZBarCam

# =======================================================
# PEGA AQUÍ TU URL DE GOOGLE APPS SCRIPT
# =======================================================
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/TU_URL_LARGA_AQUI/exec" 
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
        
        Label:
            text: 'CONTROL ASISTENCIA'
            font_size: '26sp'
            bold: True
            size_hint_y: 0.2
            color: 1, 1, 1, 1

        Button:
            text: '📸 ESCANEAR QR'
            font_size: '20sp'
            background_color: 0, 0.6, 1, 1
            on_release: app.root.current = 'scanner'

        Button:
            text: '➕ NUEVO ASISTENTE'
            font_size: '20sp'
            background_color: 0, 0.8, 0, 1
            on_release: app.root.current = 'form'

<ScannerScreen>:
    name: 'scanner'
    BoxLayout:
        orientation: 'vertical'
        ZBarCam:
            id: zbarcam
            # Escanear solo QR para más velocidad
            code_types: 'QRCODE', 'EAN13'
        
        Button:
            text: 'CANCELAR / VOLVER'
            size_hint_y: 0.15
            background_color: 1, 0, 0, 1
            on_release: app.root.current = 'menu'

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
            bold: True
            size_hint_y: None
            height: 50

        TextInput:
            id: ti_nombre
            hint_text: 'Nombre Completo'
            multiline: False
            size_hint_y: None
            height: 60
            padding_y: [20,0]
            background_color: 1, 1, 1, 1
            foreground_color: 0, 0, 0, 1

        TextInput:
            id: ti_id
            hint_text: 'ID / DNI (El número del QR)'
            multiline: False
            input_filter: 'int'
            size_hint_y: None
            height: 60
            padding_y: [20,0]

        TextInput:
            id: ti_cel
            hint_text: 'Celular'
            multiline: False
            input_filter: 'int'
            size_hint_y: None
            height: 60
            padding_y: [20,0]
        
        TextInput:
            id: ti_empresa
            hint_text: 'Empresa'
            multiline: False
            size_hint_y: None
            height: 60
            padding_y: [20,0]

        Button:
            text: 'GUARDAR REGISTRO'
            bold: True
            background_color: 0, 0.8, 0, 1
            size_hint_y: None
            height: 70
            on_release: app.enviar_formulario()

        Button:
            text: 'VOLVER'
            background_color: 0.5, 0.5, 0.5, 1
            size_hint_y: None
            height: 50
            on_release: app.root.current = 'menu'
'''

class AsistenciaApp(App):
    def build(self):
        self.permisos_android()
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_interval(self.chequear_qr, 1.0 / 30.0)

    def chequear_qr(self, dt):
        if self.root.current != 'scanner': return
        
        screen = self.root.get_screen('scanner')
        zbarcam = screen.ids.zbarcam
        
        if zbarcam.symbols:
            codigo = zbarcam.symbols[0].data.decode('utf-8')
            self.enviar_scan(codigo)
            self.root.current = 'menu'

    def enviar_scan(self, uid):
        req_url = f"{GOOGLE_SCRIPT_URL}?action=scan&id={uid}"
        self.mostrar_popup("Procesando...", "Verificando identidad...")
        UrlRequest(req_url, on_success=self.res_exito, on_failure=self.res_error, on_error=self.res_error)

    def enviar_formulario(self):
        screen = self.root.get_screen('form')
        nom = screen.ids.ti_nombre.text
        uid = screen.ids.ti_id.text
        cel = screen.ids.ti_cel.text
        emp = screen.ids.ti_empresa.text
        
        if not nom or not uid:
            self.mostrar_popup("Faltan Datos", "Nombre e ID son obligatorios")
            return

        import urllib.parse
        params = urllib.parse.urlencode({
            'action': 'nuevo', 'nombre': nom, 'id': uid, 'celular': cel, 'empresa': emp
        })
        
        req_url = f"{GOOGLE_SCRIPT_URL}?{params}"
        self.mostrar_popup("Guardando...", "Registrando en la nube...")
        UrlRequest(req_url, on_success=self.res_exito, on_failure=self.res_error, on_error=self.res_error)

    def res_exito(self, req, result):
        texto = result if isinstance(result, str) else result.decode('utf-8')
        self.mostrar_popup("Respuesta Google", texto)
        # Limpiar campos
        s = self.root.get_screen('form')
        s.ids.ti_nombre.text = ""; s.ids.ti_id.text = ""; s.ids.ti_cel.text = ""; s.ids.ti_empresa.text = ""

    def res_error(self, req, error):
        self.mostrar_popup("Error", "No hay conexión con Google")

    def mostrar_popup(self, titulo, mensaje):
        p = Popup(title=titulo, content=Label(text=mensaje), size_hint=(0.8, 0.4))
        p.open()

    def permisos_android(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA, Permission.INTERNET])

if __name__ == '__main__':
    AsistenciaApp().run()
