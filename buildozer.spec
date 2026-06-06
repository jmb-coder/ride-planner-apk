[app]
title = Ride Planner
package.name = rideplanner
package.domain = org.alton

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,webp,npz

version = 0.1

requirements = python3,kivy==2.3.0,numpy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.api = 33
android.minapi = 21

android.archs = arm64-v8a, armeabi-v7a

p4a.bootstrap = sdl2

# 🔥 CRITICAL FIXES (prevents AIDL errors)
android.ndk_version = 25b
android.build_tools_version = 33.0.2
