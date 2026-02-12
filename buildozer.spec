[app]
title = Asistencia V3
package.name = asistenciav3
package.domain = com.comagro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 3.0

# REQUISITOS (Agregamos 'gestures4kivy' que a veces es necesario para camera4kivy)
requirements = python3,kivy==2.3.0,android,requests,camera4kivy,gestures4kivy,pillow,openssl

# PERMISOS
android.permissions = INTERNET,CAMERA,WRITE_EXTERNAL_STORAGE,RECORD_AUDIO

orientation = portrait
fullscreen = 0

# --- CONFIGURACIÓN ANDROID ---
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.enable_androidx = True
android.accept_sdk_license = True

# --- ¡ESTA ES LA LÍNEA QUE FALTABA! (DRIVERS DE CÁMARA) ---
android.gradle_dependencies = androidx.camera:camera-camera2:1.1.0-beta01, androidx.camera:camera-lifecycle:1.1.0-beta01, androidx.camera:camera-view:1.1.0-beta01

# --- OPTIMIZACIÓN DE IMÁGENES (Para que no falle Pillow) ---
android.add_jars = foo.jar
p4a.branch = master
p4a.bootstrap = sdl2

# WHITELIST (Para evitar errores de archivos faltantes)
android.whitelist = lib-dynload/

[buildozer]
log_level = 2
warn_on_root = 1
