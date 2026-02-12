[app]
title = Asistencia QR
package.name = asistencia
package.domain = com.comagro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# REQUISITOS (Cámara y QR)
requirements = python3,kivy==2.3.0,android,requests,kivy_garden.zbarcam,zbar,pillow,openssl

# PERMISOS
android.permissions = INTERNET,CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

orientation = portrait
fullscreen = 0

# CONFIGURACION ANDROID
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.enable_androidx = True

# --- ¡ESTA ES LA LÍNEA QUE FALTABA! ---
android.accept_sdk_license = True
# --------------------------------------

# CONFIGURACION COMPILADOR
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
