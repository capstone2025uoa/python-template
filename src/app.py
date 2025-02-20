from flask import Flask
from adapters.rest.userController import user_bp

app  = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(user_bp, url_prefix='/users')

if __name__ == '__main__':
    app.run(debug=True)