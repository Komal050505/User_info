"""
Flask Application for User Management

This module defines a Flask application that manages user records in a database.
It provides endpoints to retrieve, create, update, and delete user information.

Endpoints:
    - /get_all_records: Retrieves all user records.
    - /get_custom_columns: Retrieves user records with custom columns excluded.
    - /create_user: Creates a new user record.
    - /update_user/<int:emp_id>: Updates an existing user record based on Employee ID.
    - /delete_user/<int:emp_id>: Deletes a user record based on Employee ID.

Logging:
    The module uses a logging utility to log informational, error, and debug messages
    for tracking operations and troubleshooting.

Dependencies:
    - Flask: Web framework for creating the API.
    - SQLAlchemy: ORM for database interactions.
    - Logging: Provides logging functionality.

Configuration:
    - Database: Uses SQLAlchemy with a configured engine and session.
    - Logging: Configured to handle different levels of logging.

Module Functions:
    - get_records: Fetches all user records from the database.
    - get_custom_columns: Fetches user records with specified columns excluded.
    - exclude_columns: Utility function to exclude specified columns from user data.
    - create_user: Creates a new user record in the database.
    - update_user: Updates an existing user record in the database.
    - delete_user: Deletes a user record from the database.
"""

from flask import Flask, jsonify, request
from sqlalchemy.orm import sessionmaker
from db_connections.configurations import engine, create_tables
from email_setup.email_operations import notify_success, notify_failure
from logging_package.logging_utility import log_info, log_error, log_warning
from user_models.tables import UserInfo

# Flask Setup
app = Flask(__name__)

# Create all tables
create_tables()

# Dependency Injection of Database Session
Session = sessionmaker(bind=engine)


@app.route('/get_all_records', methods=["GET"])
def get_records():
    """
    Retrieves all user records from the database.
    """
    session = Session()
    log_info("Entering get_records function")
    try:
        result = session.query(UserInfo).all()
        response = [user.__dict__ for user in result]
        for user in response:
            user.pop('_sa_instance_state', None)
        log_info("Fetched all user records successfully")
        notify_success("Records fetched", "All user records have been successfully fetched.")
        return jsonify(response)
    except Exception as e:
        log_error(f"Error fetching records: {str(e)}")
        notify_failure("Error fetching records", str(e))
        return jsonify({"message": "Error fetching records", "error": str(e)}), 500
    finally:
        session.close()
        log_info("Exiting get_records function")


@app.route('/get_custom_columns', methods=["GET"])
def get_custom_columns():
    """
    Retrieves user records with custom columns excluded.
    """
    session = Session()
    log_info("Entering get_custom_columns function")
    try:
        result = session.query(UserInfo).all()
        response = [exclude_columns(user.__dict__) for user in result]
        log_info("Fetched custom columns successfully")
        notify_success("Custom columns fetched",
                       "User records with custom columns excluded have been successfully fetched.")
        return jsonify(response)
    except Exception as e:
        log_error(f"Error fetching custom columns: {str(e)}")
        notify_failure("Error fetching custom columns", str(e))
        return jsonify({"message": "Error fetching custom columns", "error": str(e)}), 500
    finally:
        session.close()
        log_info("Exiting get_custom_columns function")


def exclude_columns(user_dict):
    """
    Excludes specified columns from the user dictionary.

    This function removes specified columns from the user dictionary before returning it.

    :param user_dict: Dictionary containing user data
    :return: Dictionary with specified columns excluded
    """
    exclude = ['_sa_instance_state']  # Specify columns to exclude here
    final_dict = {key: user_dict[key] for key in user_dict if key not in exclude}
    return final_dict


@app.route('/create_user', methods=["POST"])
def create_user():
    """
    Creates a new user record in the database.
    """
    data = request.json
    session = Session()
    log_info("Entering create_user function")
    try:
        new_user = UserInfo(
            EmployeeID=data['emp_id'],
            Age=data['age'],
            Name=data['name'],
            Exp=data['exp'],
            Gender=data['gender'],
            Dept=data['dept'],
            Country=data['country']
        )
        session.add(new_user)
        session.commit()
        log_info(f"User {data['name']} created successfully")
        notify_success("User created", f"User {data['name']} has been created successfully.")
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        session.rollback()
        log_error(f"Error creating user: {str(e)}")
        notify_failure("Error creating user", str(e))
        return jsonify({"message": "Error creating user", "error": str(e)}), 500
    finally:
        session.close()
        log_info("Exiting create_user function")


@app.route('/update_user/<int:emp_id>', methods=["PUT"])
def update_user(emp_id):
    """
    Updates an existing user record.
    """
    data = request.json
    session = Session()
    log_info("Entering update_user function")
    try:
        user = session.query(UserInfo).filter_by(EmployeeID=emp_id).first()
        if not user:
            log_warning(f"User with ID {emp_id} not found")
            return jsonify({"message": "User not found"}), 404

        user.Age = data.get('age', user.Age)
        user.Name = data.get('name', user.Name)
        user.Exp = data.get('exp', user.Exp)
        user.Gender = data.get('gender', user.Gender)
        user.Dept = data.get('dept', user.Dept)
        user.Country = data.get('country', user.Country)

        session.commit()
        log_info(f"User {emp_id} updated successfully")
        notify_success("User updated", f"User with ID {emp_id} has been updated successfully.")
        return jsonify({"message": "User updated successfully"})
    except Exception as e:
        session.rollback()
        log_error(f"Error updating user: {str(e)}")
        notify_failure("Error updating user", str(e))
        return jsonify({"message": "Error updating user", "error": str(e)}), 500
    finally:
        session.close()
        log_info("Exiting update_user function")


@app.route('/delete_user/<int:emp_id>', methods=["DELETE"])
def delete_user(emp_id):
    """
    Deletes a user record from the database.
    """
    session = Session()
    log_info("Entering delete_user function")
    try:
        user = session.query(UserInfo).filter_by(EmployeeID=emp_id).first()
        if not user:
            log_warning(f"User with ID {emp_id} not found")
            return jsonify({"message": "User not found"}), 404

        session.delete(user)
        session.commit()
        log_info(f"User {emp_id} deleted successfully")
        notify_success("User deleted", f"User with ID {emp_id} has been deleted successfully.")
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        session.rollback()
        log_error(f"Error deleting user: {str(e)}")
        notify_failure("Error deleting user", str(e))
        return jsonify({"message": "Error deleting user", "error": str(e)}), 500
    finally:
        session.close()
        log_info("Exiting delete_user function")


@app.route('/get_docs', methods=["GET"])
def get_docs():
    """
    Provides documentation for the API endpoints.
    """
    documentation = """
    Flask Application for User Management

    This module defines a Flask application that manages user records in a database.
    It provides endpoints to retrieve, create, update, and delete user information.

    Endpoints:
        - /get_all_records: Retrieves all user records.
        - /get_custom_columns: Retrieves user records with custom columns excluded.
        - /create_user: Creates a new user record.
        - /update_user/<int:emp_id>: Updates an existing user record based on Employee ID.
        - /delete_user/<int:emp_id>: Deletes a user record based on Employee ID.
        - /docs: Provides documentation for the API endpoints.

    Logging:
        The module uses a logging utility to log informational, error, and debug messages
        for tracking operations and troubleshooting.

    Dependencies:
        - Flask: Web framework for creating the API.
        - SQLAlchemy: ORM for database interactions.
        - Logging: Provides logging functionality.

    Configuration:
        - Database: Uses SQLAlchemy with a configured engine and session.
        - Logging: Configured to handle different levels of logging.

    Module Functions:
        - get_records: Fetches all user records from the database.
        - get_custom_columns: Fetches user records with specified columns excluded.
        - exclude_columns: Utility function to exclude specified columns from user data.
        - create_user: Creates a new user record in the database.
        - update_user: Updates an existing user record in the database.
        - delete_user: Deletes a user record from the database.
    """
    return jsonify({"documentation": documentation})


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
