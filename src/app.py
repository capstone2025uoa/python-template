from flask import Flask
from adapters.rest.userController import user_bp
from flasgger import Swagger

app  = Flask(__name__)
app.url_map.strict_slashes = False
# Swagger UI running on http://localhost:5000/apidocs
swagger = Swagger(app)

app.register_blueprint(user_bp, url_prefix='/users')

if __name__ == '__main__':
    app.run(debug=True)