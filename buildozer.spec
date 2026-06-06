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

# IMPORTANT: fixes many modern builds
p4a.branch = master

[buildozer]

log_level = 2
warn_on_root = 1
