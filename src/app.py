from flask import Flask
from adapters.rest.user_controller import user_bp
from flasgger import Swagger
from database.db import create_tables

app  = Flask(__name__)
app.url_map.strict_slashes = False
# Swagger UI running on http://localhost:5000/apidocs
# Initial requests might fail if using AWS Aurora serverlessv2 with a cold start
# Sample error: server closed the connection unexpectedly
# Aurora pauses databases to save costs for developement
# The issue won't happen in production
swagger = Swagger(app)
app.register_blueprint(user_bp, url_prefix='/users')

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)