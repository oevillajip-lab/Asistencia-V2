[app]
title = Asistencia QR
package.name = asistencia
package.domain = com.comagro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# REQUISITOS (Zbar y Kivy)
requirements = python3,kivy==2.3.0,android,requests,kivy_garden.zbarcam,zbar,pillow,openssl

# PERMISOS
android.permissions = INTERNET,CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

orientation = portrait
fullscreen = 0

# --- CONFIGURACIÓN ANDROID (CRUCIAL) ---
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.enable_androidx = True

# ACEPTAR LICENCIAS AUTOMÁTICAMENTE (Esto evita el error oculto)
android.accept_sdk_license = True

# (He quitado p4a.branch = master para usar la versión ESTABLE)

[buildozer]
log_level = 2
warn_on_root = 1
