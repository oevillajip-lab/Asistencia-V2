[app]
title = Asistencia V3
package.name = asistenciav3
package.domain = com.comagro
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 3.0

# REQUISITOS (Sin zbarcam, con camera4kivy)
requirements = python3,kivy==2.3.0,android,requests,camera4kivy,pillow,openssl

# PERMISOS
android.permissions = INTERNET,CAMERA,WRITE_EXTERNAL_STORAGE

orientation = portrait
fullscreen = 0

# ANDROID CONFIG
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.enable_androidx = True
android.accept_sdk_license = True

# COMPILADOR ESTABLE
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
