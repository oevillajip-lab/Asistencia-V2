[app]
title = Asistencia QR Final
package.name = asistenciafinal
package.domain = com.comagro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 5.0

# REQUISITOS (Vitales para la cámara)
requirements = python3,kivy==2.3.0,camera4kivy,gestures4kivy,pillow,requests,openssl

# --- IMPORTANTE: COMENTAMOS ESTO PARA QUE NO SALGA EL LOGO GIGANTE ---
# El logo lo manejamos nosotros por código ahora
# presplash.filename = %(source.dir)s/logo.png

# Icono de la App (En el menú del celular)
icon.filename = %(source.dir)s/logo.png

orientation = portrait
fullscreen = 0

# --- PERMISOS ---
android.permissions = INTERNET,CAMERA,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE

# --- CONFIGURACIÓN TÉCNICA (PARA EVITAR EL CRASH) ---
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.enable_androidx = True
android.accept_sdk_license = True

# --- ¡ESTAS SON LAS LÍNEAS QUE EVITAN QUE SE CIERRE! ---
# Descargan el motor de la cámara de Google
android.gradle_dependencies = androidx.camera:camera-camera2:1.1.0-beta01, androidx.camera:camera-lifecycle:1.1.0-beta01, androidx.camera:camera-view:1.1.0-beta01

p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
