from datetime import date
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from fastapi import APIRouter
from services.movie import MovieService

movie_router = APIRouter()
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=10, max_length=50)
    year: int = Field(le = 2022)
    rating: float 
    category: str

    model_config = {
            "json_schema_extra": {
                "examples": [
                {
                    'id': 1,
                    'title' : 'Crepusculo',
                    'overview' : 'The twilight is almost better than sunday',
                    'year' : '2022',
                    'rating' : 9.5,
                    'category' : 'Phantasy'
                }
                ]
            }
        }


@movie_router.get("/movies", tags=["Movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get("/movies/{id}", tags=["Movies"], response_model=Movie)
def get_movie(id: int = Path(ge = 1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
         return JSONResponse(status_code=404, content={"message": "Movie not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get('/movies/', tags=["Movies"], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movies not found"})
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.post("/movies", tags=["Movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie):
    db = Session()
    new_movie = MovieModel(title=movie.title, overview=movie.overview, year=movie.year, rating=movie.rating, category=movie.category)
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Movie created successfully"})

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Movie updated successfully"})

@movie_router.delete('/movies/{id}', tags=["Movies"], response_model=dict, status_code=200)
def delete_movie(id: int):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Movie deleted successfully"})