# Educational Documentation for Flask REST API Sample Application

This document provides an overview and educational insights into a simple Flask-based REST API application. The sample is designed to demonstrate the following concepts:

- How to structure a Flask application using blueprints
- How to define and register RESTful routes for CRUD operations
- Using Flask's request and jsonify functionalities

---

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Setup and Installation](#setup-and-installation)
4. [Application Components](#application-components)
    - [Main Application (app.py)](#main-application-apppy)
    - [User Controller (userController.py)](#user-controller-usercontrollerpy)
5. [API Endpoints](#api-endpoints)
6. [Further Considerations](#further-considerations)

---

## Overview

This sample application demonstrates a simple REST API built using Flask. It showcases basic operations for managing user data (retrieval, creation, and update) by using a Flask blueprint. The data source in this sample is a mock dataset defined in `data/mock.py` (not shown in this sample). 

The API is accessible under the `/users` path, supporting both plural and singular forms with/without a trailing slash due to Flask's `strict_slashes` configuration.

---

## Project Structure

The key parts of the project include:

- **src/app.py**: The main entry point for the Flask application. It creates the Flask app instance, registers the blueprint, and runs the server.
- **src/adapters/rest/userController.py**: Contains the user-related endpoints (GET, POST, and PUT) using a Flask blueprint, making the code modular and maintainable.
- **data/mock.py**: (Not shown here) Contains a mock list of users (`MOCK_USERS`) used as the data source for demonstration purposes.

---

## Setup and Installation

1. **Install Python** (version 3.6+ is recommended).
2. **Install dependencies**: Run `pip install flask` in your terminal.
3. **Run the application**:
   ```bash
   python src/app.py
   ```
   The application will start in debug mode, listening on the default Flask port (usually 5000).

---

## Application Components

### Main Application (app.py)

- **Purpose**: Initializes the Flask application and registers the user blueprint.
- **Key Elements**:
  - `app = Flask(__name__)`: Creates the Flask application instance.
  - `app.register_blueprint(user_bp, url_prefix='/users')`: Registers the user blueprint under the `/users` prefix. This means that routes defined in the blueprint will be prefixed with `/users`.
  - `app.url_map.strict_slashes = False`: Allows both URLs with and without a trailing slash to be handled in the same way.

### User Controller (userController.py)

- **Purpose**: Handles routes related to user operations.
- **Key Endpoints**:
  - **GET `/users/`**: Returns a JSON list of all users from the `MOCK_USERS` dataset.
  - **GET `/users/<int:user_id>`**: Returns JSON details of a single user by `user_id`. If no matching user is found, returns a 404 error with an appropriate message.
  - **POST `/users/`**: Accepts JSON data to create a new user. The new user is appended to the `MOCK_USERS` list with an auto-generated `id` based on the list length.
  - **PUT `/users/<int:user_id>`**: Intended to update an existing user. (Note: The sample code shows the beginning of this function, indicating an area for further development.)

---

## API Endpoints

| Method | Endpoint                 | Description                                                     |
|--------|--------------------------|-----------------------------------------------------------------|
| GET    | `/users/`                | Retrieves a list of all users.                                  |
| GET    | `/users/<user_id>`       | Retrieves details for a specified user.                         |
| POST   | `/users/`                | Creates a new user with the provided JSON data.                 |
| PUT    | `/users/<user_id>`       | Updates the details of an existing user (function under development)|

---

## Further Considerations

- **Data Persistence**: The current implementation uses a mock data list (`MOCK_USERS`). For a real application, consider integrating a database for persistent storage.
- **Validation and Error Handling**: Additional validation and error handling can be implemented to ensure data integrity.
- **Extending the API**: To support full CRUD operations, consider implementing DELETE and completing the PUT endpoint for updating user records.
- **Modular Design**: The use of blueprints in Flask helps manage complexity as the application grows. Each resource (like users) can have its own blueprint.

---

## Conclusion

This sample serves as an educational tool for understanding the basics of building a REST API with Flask. By using blueprints to modularize the application, it lays the groundwork for a scalable web service architecture. Experiment with extending this sample to add more features, integrate with a database, or improve the API's robustness.

Happy Learning! 