"""
flask rest
run app on port 2000
"""
from flask import Flask
from routing import Routing
from log import Log

app = Flask(__name__)

# set app secret key
app.config['SECRET_KEY'] = 'app-secret-key'
routing = Routing(app)
log = Log()

routing.serve()


if __name__ == '__main__':
    app.run(host="localhost", port=2000, debug=True)
