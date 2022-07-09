
import sys

path = '/home/scuaaa/web_app2/web_app_python_flask_mongodb'  # path to your repos
if path not in sys.path:
    sys.path.append(path)

from wsgi import app as application