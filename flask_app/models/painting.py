from flask_app.config.mysqlconnection import connectToMySQL, DB
from flask import flash
from flask_app.models.user import User

class Painting:

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM paintings JOIN users ON paintings.user_id = users.id;"

        results = connectToMySQL(DB).query_db(query)
        
        paintings = []
        for row in results:
            painting = cls(row)
            user_dict = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            painting.user = User(user_dict)
            paintings.append(painting)

        return paintings
    
    @classmethod 
    def get_by_id(cls, data):
        query = "SELECT * FROM paintings JOIN users ON users.id = paintings.user_id WHERE paintings.id = %(id)s;"
        
        results = connectToMySQL(DB).query_db(query, data)

        if len(results) < 1:
            return False
        
        row = results[0]

        painting = cls(row)
        
        user_dict = {
            'id': row['users.id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'password': row['password'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at'],
        }

        painting.user = User(user_dict)
        return painting

    @classmethod
    def create(cls, data):
        query = "INSERT INTO paintings (title, description, price, user_id) VALUES (%(title)s, %(description)s, %(price)s, %(user_id)s);"
        results = connectToMySQL(DB).query_db(query , data)
        return results
    
    @classmethod
    def update(cls, data):
        query = "UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, user_id = %(user_id)s WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        return results
    
    @classmethod 
    def delete(cls, data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @staticmethod
    def validation(painting):
        is_valid = True
        if len(painting['title']) < 2:
            flash("name must be at least 2 characters!","painting")
            is_valid = False
        if len(painting['description']) < 10:
            flash("description must be at least 10 characters!","painting")
            is_valid = False
        if len(painting['price']) < 0:
            flash("instructions must be greater than 0!","painting")
            is_valid = False
        return is_valid


