[app]
title = Asistencia QR
package.name = asistenciafinal
package.domain = com.comagro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 4.0

# --- REQUISITOS (Vital para que no se cierre) ---
requirements = python3,kivy==2.3.0,camera4kivy,gestures4kivy,pillow,requests,openssl

# --- LOGO E ICONO (¡AQUÍ ESTÁ LA SOLUCIÓN DEL LOGO!) ---
icon.filename = %(source.dir)s/logo.png
presplash.filename = %(source.dir)s/logo.png

# --- PERMISOS (Vital para cámara) ---
android.permissions = INTERNET,CAMERA,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE

orientation = portrait
fullscreen = 0

# --- CONFIGURACIÓN ANDROID ---
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.enable_androidx = True
android.accept_sdk_license = True

# --- DRIVERS DE CÁMARA (Para evitar el crash) ---
android.gradle_dependencies = androidx.camera:camera-camera2:1.1.0-beta01, androidx.camera:camera-lifecycle:1.1.0-beta01, androidx.camera:camera-view:1.1.0-beta01

p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
