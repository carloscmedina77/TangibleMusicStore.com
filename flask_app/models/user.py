from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL("music_db").query_db(query, data)

    @classmethod
    def find_by_id(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s"
        results = connectToMySQL("music_db").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def find_by_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s"

        results = connectToMySQL("music_db").query_db(query, data)

        if len(results) < 1:
            return False

        return cls(results[0])

    @staticmethod
    def validate(data):
        is_valid = True

        if len(data['first_name']) < 1:
            is_valid = False
            flash("First name must not be blank!")

        if len(data['last_name']) < 1:
            is_valid = False
            flash("Last name must not be blank!")

        if len(data['password']) < 1:
            is_valid = False
            flash("Password must not be blank!")

        if len(data['email']) < 1:
            is_valid = False
            flash("email must not be blank!")

        data_for_email_validator = {
            'email': data['email']
        }

        if not EMAIL_REGEX.match(data['email']):
            flash("Email invalid")
            is_valid = False
        if User.find_by_email(data_for_email_validator):
            flash("Email already registered!")
            is_valid = False

        return is_valid
