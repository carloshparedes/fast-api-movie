from models.movie import Movie as MovieModel
from services.schemas.movie import Movie

class MovieService():
    
    def __init__(self, db):
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    
    def get_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movies_by_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return {"message": "Movie created successfully"}
    
    def update_movie(self, id: int, movie: Movie):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        movie.title = movie.title
        movie.overview = movie.overview
        movie.year = movie.year
        movie.rating = movie.rating
        movie.category = movie.category
        self.db.commit()
        return movie