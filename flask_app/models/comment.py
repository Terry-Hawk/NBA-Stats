# Import the ability to connect to MySQL Workbench using the config file after installation of pymysql
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user

class Comment:
    db = "nba_tracker"

    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.rating = data['rating']
        self.add_drop = data['add_drop']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data["user_id"]
        self.creator = None

# --------------------------Create Class Methods--------------------------------#
# Class methods are used for data submission to the database
    @classmethod
    def create_comment(cls,user_data):
        query="""
        INSERT INTO social (comment, rating, add_drop, user_id)
        VALUES (%(comment)s,%(rating)s,%(add_drop)s,%(user_id)s)
        """
        result = connectToMySQL(cls.db).query_db(query,user_data)
        return result
    
    @classmethod
    def get_all_comments(cls):
        query="""
        SELECT * FROM social JOIN users on social.user_id = users.id;
        """
        results=connectToMySQL(cls.db).query_db(query)
        comments=[]
        for row in results:
            comment = cls(row)
            comment_creator_info={
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["created_at"],
                "updated_at":row["updated_at"]
            }
            creator = user.User(comment_creator_info)
            comment.creator=creator
            comments.append(comment)
        return comments

    @classmethod
    def get_comment_by_id(cls,id):
        data={"id":id}
        query="""
        SELECT * FROM social where id =%(id)s;
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) == 0:
            return False
        else:
            return cls(result[0])
        
    @classmethod
    def get_user_comments(cls,user_id):
        data={"id":user_id}
        query="""
        SELECT * FROM social Join users on social.user_id = users.id where users.id = %(id)s;
        """
        results=connectToMySQL(cls.db).query_db(query,data)
        comments=[]
        for row in results:
            comment=cls(row)
            comment_creator_info={
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["created_at"],
                "updated_at":row["updated_at"]
            }
            creator = user.User(comment_creator_info)
            comment.creator=creator
            comments.append(comment)
        return comments

    @classmethod
    def update_comment(cls,data):
        query= """
        UPDATE social
        SET
        comment = %(comment)s, rating = %(rating)s, add_drop = %(add_drop)s, user_id = %(user_id)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete_comment_by_id(cls, comment_id):
        data={"id":comment_id}
        query="""
        DELETE FROM social WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query,data)

# --------------------------Create Static Methods--------------------------------#
# Static methods are used for validation of the data that is input
