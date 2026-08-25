[app]

# (str) Title of your application
title = JARVIS Mobile

# (str) Package name
package.name = jarvis_mobile

# (str) Package domain (needed for android/ios packaging)
package.domain = org.jarvis.mobile

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the directory)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,pyjnius,requests,speechrecognition,pyaudio,beautifulsoup4,pypdf

# (list) Permissions
permissions = INTERNET,RECORD_AUDIO,FOREGROUND_SERVICE,CALL_PHONE,SEND_SMS,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,SYSTEM_ALERT_WINDOW

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 24

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Services to declare
services = JarvisBackgroundService:services/background_service.py

# (str) Orientation
orientation = portrait
