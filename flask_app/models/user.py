# Import the ability to connect to MySQL Workbench using the config file after installation of pymysql
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')

bcrypt = Bcrypt(app)

class User:
    db = "nba_tracker"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# --------------------------Create Class Methods--------------------------------#
# Class methods are used for data submission to the database

    @classmethod
    def register(cls,user_data):
        data={
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "email": user_data["email"],
            "password": bcrypt.generate_password_hash(user_data["password"])
        }
        query="""
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password)s)
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        return result
    
    @classmethod
    def get_all_users(cls):
        query="""
        SELECT * FROM users;
        """
        results = connectToMySQL(cls.db).query_db(query)
        users=[]
        for row in results:
            users.append(cls(row))
        return users
    
    @classmethod
    def get_user_by_email(cls,email):
        data={"email":email}
        query="""
        SELECT * FROM users WHERE email = %(email)s;
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) == 0:
            return False
        else:
            # There should only be one result because we are looking by email, and only 1 email can be used to sign up for the app
            return (cls(result[0]))
        
    @classmethod
    def get_user_by_id(cls,id):
        data={"id":id}
        query="""
        SELECT * FROM users where id = %(id)s;
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) == 0:
            return False
        else:
            # There should only be one result because we are looking by id, and each person will have a unique id
            return cls(result[0])
        
# --------------------------Create Static Methods--------------------------------#
# Static methods are used for validation of the data that is input

    @staticmethod
    def validate_registration(user):
        is_valid = True
        user_in_db = User.get_user_by_email(user["email"])
        if len(user["first_name"]) < 2:
            flash("First name must be more than 2 characters long", "register")
            is_valid = False
        if len(user["last_name"]) < 2:
            flash("Last name must be at least 2 characters long", "register")
            is_valid = False
        if len(user["email"]) == 0 or not EMAIL_REGEX.match(user["email"]):
            flash("Email invalid, must follow format: example@email.com", "register")
            is_valid = False
        if len(user["password"]) < 8:
            flash("Your password must be at least 8 characters","register")
            is_valid = False
        if user["password"] != user["confirm"]:
            flash("Password and confirm password must match!")
            is_valid = False
        if user_in_db is not False:
            flash("Email address already in use, please login or use a different email", "register")
            is_valid = False
        print(user_in_db)
        return is_valid
    
    @staticmethod
    def validate_login(user):
        is_valid = True 
        user_in_db = User.get_user_by_email(user["email"])
        if len(user["email"]) == 0 or not EMAIL_REGEX.match(user["email"]):
            flash("Invalid Email/Password","login")
            is_valid = False
        if user_in_db is False:
            flash("Invalid Email/Password", "login")
            is_valid = False
        elif len(user["password"]) < 8 or not bcrypt.check_password_hash(user_in_db.password,user["password"]):
            flash("Invalid Email/Password","login")
            is_valid = False
        if len(user["password"]) < 8:
            flash("Invalid Email/Password")
            is_valid = False
        if is_valid:
            return user_in_db
        else:
            return is_valid