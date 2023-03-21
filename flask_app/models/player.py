# Import the ability to connect to MySQL Workbench using the config file after installation of pymysql
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models import user

class Player:
    db = "nba_tracker"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.season = data['season']
        self.gp = data['gp']
        self.mins = data['mins']
        self.fgm = data['fgm']
        self.fg3m = data['fg3m']
        self.ftm = data['ftm']
        self.reb = data['reb']
        self.ast = data['ast']
        self.stl = data['stl']
        self.blk = data['blk']
        self.pts = data['pts']
        self.team = data['team']
        self.user_id = data["user_id"]
        self.creator = None

# --------------------------Create Class Methods--------------------------------#
# Class methods are used for data submission to the database
    @classmethod
    def create_player(cls,user_data):
        query="""
        INSERT INTO players (first_name, last_name, season, gp, mins, fgm, fg3m, ftm, reb, ast, stl, blk, pts, team, user_id)
        VALUES (%(first_name)s,%(last_name)s,%(season)s,%(gp)s,%(mins)s,%(fgm)s,%(fg3m)s,%(ftm)s,%(reb)s,%(ast)s,%(stl)s,%(blk)s,%(pts)s,%(team)s,%(user_id)s)
        """
        result = connectToMySQL(cls.db).query_db(query,user_data)
        return result
    
    @classmethod
    def get_all_players(cls):
        query="""
        SELECT * FROM players JOIN users on players.user_id = users.id;
        """
        results = connectToMySQL(cls.db).query_db(query)
        players=[]
        for row in results:
            player=cls(row)
            player_creator_info={
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["created_at"],
                "updated_at":row["updated_at"]
            }
            creator = user.User(player_creator_info)
            player.creator=creator
            players.append(player)
        return players
        
    @classmethod
    def get_player_by_id(cls,id):
        data={"id":id}
        query="""
        SELECT * FROM players where id = %(id)s;
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) == 0:
            return False
        else:
            # There should only be one result because we are looking by id, and each person will have a unique id
            return cls(result[0])
        
    @classmethod
    def get_user_players(cls, user_id):
        data={"id":user_id}
        query="""
        SELECT * from players JOIN users on players.user_id = users.id where users.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query,data)
        players=[]
        for row in results:
            player=cls(row)
            player_creator_info={
                "id":row["users.id"],
                "first_name":row["first_name"],
                "last_name":row["last_name"],
                "email":row["email"],
                "password":row["password"],
                "created_at":row["created_at"],
                "updated_at":row["updated_at"]
            }
            creator = user.User(player_creator_info)
            player.creator=creator
            players.append(player)
        return players


    @classmethod
    def update_player(cls,data):
        query="""
        UPDATE players SET
        first_name =%(first_name)s,
        last_name =%(last_name)s,
        team =%(team)s,
        season =%(season)s,
        gp =%(gp)s,
        mins =%(mins)s,
        fgm =%(fgm)s,
        fg3m =%(fg3m)s,
        ftm =%(ftm)s,
        reb =%(reb)s,
        ast =%(ast)s,
        stl =%(stl)s,
        blk =%(blk)s,
        pts =%(pts)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def delete_player_by_id(cls, player_id):
        data={"id": player_id}
        query="""
        DELETE FROM players WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query,data)
    
# --------------------------Create Static Methods--------------------------------#
# Static methods are used for validation of the data that is input

    @staticmethod
    def validate_player(player):
        is_valid = True
        if len(player["first_name"]) < 1:
            flash("First name must be more than 2 characters long", "create")
            is_valid = False
        if len(player["last_name"]) < 2:
            flash("Last name must be at least 2 characters long", "create")
            is_valid = False
        if len(player["team"]) < 2:
            flash("Team name must be at least 2 characters long", "create")
            is_valid = False
        if len(player["season"]) < 4:
            flash("Please choose a season between 1960 and 2023", "create")
            is_valid = False
        if len(player["gp"]) == 0:
            flash("Please indicate how many games were played by this player, even if it is 0", "create")
            is_valid = False
        if len(player["mins"]) == 0:
            flash("Please indicate how many minutes were played by this player, even if it is 0", "create")
            is_valid = False
        if len(player["fgm"]) == 0:
            flash("Please indicate how many field goals were made by this player, even if it is 0", "create")
            is_valid = False
        if len(player["fg3m"]) == 0:
            flash("Please indicate how many 3-pointers were made by this player, even if it is 0", "create")
            is_valid = False
        if len(player["ftm"]) == 0:
            flash("Please indicate how many free throws were made by this player, even if it is 0", "create")
            is_valid = False
        if len(player["reb"]) == 0:
            flash("Please indicate how many rebounds this player got, even if it is 0", "create")
            is_valid = False
        if len(player["ast"]) == 0:
            flash("Please indicate how many assists this player had, even if it is 0", "create")
            is_valid = False
        if len(player["stl"]) == 0:
            flash("Please indicate how many steals this player had, even if it is 0", "create")
            is_valid = False
        if len(player["blk"]) == 0:
            flash("Please indicate how many blocks this player had, even if it is 0", "create")
            is_valid = False
        if len(player["pts"]) == 0:
            flash("Please indicate how many points this player had, even if it is 0", "create")
            is_valid = False

        return is_valid
    
    