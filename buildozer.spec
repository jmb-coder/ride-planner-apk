[app]

title = Ride Planner
package.name = rideplanner
package.domain = org.alton

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,webp,npz
source.include_patterns = *.npz,*.webp

version = 0.1

# Core dependencies
requirements = python3,kivy==2.3.0,numpy

orientation = portrait

# Permissions
android.permissions = INTERNET

# Android config (IMPORTANT FIXES)
android.api = 33
android.minapi = 21
android.ndk_api = 21

# CPU architectures
android.archs = arm64-v8a,armeabi-v7a

# Build system
p4a.bootstrap = sdl2

# Fix AIDL + SDK issues
android.build_tools_version = 33.0.2
android.accept_sdk_license = True

# Packaging optimizations
android.private_storage = True

# Optional: improves stability for numpy apps
android.enable_androidx = True


[buildozer]

log_level = 2
warn_on_root = 1
