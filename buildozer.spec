[app]
title = Asistencia QR
package.name = asistenciafinal
package.domain = com.comagro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 7.0

# REQUISITOS (Incluimos android para permisos)
requirements = python3,kivy==2.3.0,camera4kivy,gestures4kivy,pillow,requests,openssl,android

# --- ESTO ARREGLA EL LOGO GIGANTE ---
# Quitamos presplash.filename para que no estire la imagen.
# Ponemos fondo NEGRO elegante mientras carga.
android.presplash_color = #000000
# El icono de la app en el menú SÍ será tu logo
icon.filename = logo.png

orientation = portrait
fullscreen = 0

# PERMISOS
android.permissions = INTERNET,CAMERA,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE

# CONFIGURACIÓN TÉCNICA
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.enable_androidx = True
android.accept_sdk_license = True

# DRIVERS DE CÁMARA (Vital para que no crashee)
android.gradle_dependencies = androidx.camera:camera-camera2:1.1.0-beta01, androidx.camera:camera-lifecycle:1.1.0-beta01, androidx.camera:camera-view:1.1.0-beta01

p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
