from models.movie import Movie as MovieModel

class MovieService():
    
    def __init__(self, db):
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result