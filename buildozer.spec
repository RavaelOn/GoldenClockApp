[app]
# (str) Title of your application
title = Golden Analog Clock

# (str) Package name
package.name = goldenclock

# (str) Package domain (unique identifier, reverse DNS style)
package.domain = org.example

# (str) Source code directory (where main.py is located)
source.dir = .

# (str) The main .py file
source.main = main.py

# (str) Application version
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (str) Supported orientations (portrait, landscape, or all)
orientation = all

# (list) Permissions (leave empty unless needed)
android.permissions = INTERNET

# (str) Android API levels
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk_api = 21

# (bool) Automatically accept SDK licenses
android.accept_sdk_license = True

# (str) Directory where APKs will be placed
dist.dir = ./bin

[buildozer]
# (str) Log level (1 = minimal, 2 = normal, 3 = verbose)
log_level = 2
