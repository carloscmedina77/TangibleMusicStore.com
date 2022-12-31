from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash
from flask_app.models import user


class Music:
    def __init__(self, data):
        self.id = data['id']
        self.artist = data['artist']
        self.album_title = data['album_title']
        self.release_date = data['release_date']
        self.format = data['format']
        self.picture = data['picture']
        self.new_or_used = data['new_or_used']
        self.price = data['price']
        self.genre = data['genre']
        self.description = data['description']
        self.label = data['label']
        self.listen_link = data['listen_link']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO musics (artist, album_title, release_date, format, picture, new_or_used, price, genre, description, label, listen_link, user_id) VALUES (%(artist)s,%(album_title)s,%(release_date)s,%(format)s,%(picture)s,%(new_or_used)s,%(price)s,%(genre)s,%(description)s,%(label)s,%(listen_link)s,%(user_id)s)"
        return connectToMySQL("music_db").query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM musics WHERE id=%(id)s"
        return connectToMySQL('music_db').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE musics SET artist=%(artist)s, album_title=%(album_title)s, release_date=%(release_date)s, format=%(format)s, picture=%(picture)s, new_or_used=%(new_or_used)s,price=%(price)s, genre=%(genre)s, description=%(description)s, label=%(label)s, listen_link=%(listen_link)s WHERE id=%(id)s"
        return connectToMySQL('music_db').query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM musics WHERE id = %(id)s"
        results = connectToMySQL("music_db").query_db(query, data)

        if len(results) < 1:
            return False

        return cls(results[0])

    @classmethod
    def get_all_musics(cls):
        query = "SELECT * FROM musics JOIN users ON users.id = musics.user_id"

        results = connectToMySQL("music_db").query_db(query)

        musics = []

        for result in results:
            music = cls(result)
            data = {
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at'],

            }
            creator = user.User(data)
            music.creator = creator

            musics.append(music)

        return musics

    staticmethod
    def validate(data):
        is_valid = True

        if len(data['label']) < 1:
            is_valid = False
            flash('Label must not be blank')
        if len(data['release_date']) < 1:
            is_valid = False
            flash('Release date must not be blank')
        if len(data['artist']) < 1:
            is_valid = False
            flash('Artist must not be blank')
        if len(data['album_title']) < 1:
            is_valid = False
            flash('Album title must not be blank')
        if len(data['price']) < 1:
            is_valid = False
            flash('Price must not be blank')
        if len(data['description']) < 1:
            is_valid = False
            flash('Description must not be blank')
        if len(data['listen_link']) < 1:
            is_valid = False
            flash('Listen link must not be blank')
        if len(data['picture']) < 1:
            is_valid = False
            flash('Picture must not be blank')
        
        return is_valid
