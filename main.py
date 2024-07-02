from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
app.title = "My Movie API "
app.version = "0.0.1"

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

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "The Shawshank Redemption",
        "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "year": "1994",
        "rating": 9.3,
        "category": "Drama"
    }
]

@app.get("/", tags=["Home"])
def message():
    return HTMLResponse("<h1>Welcome to My Movie API</h1>")

@app.get("/movies", tags=["Movies"])
def get_movies():
    return JSONResponse(content=movies)

@app.get("/movies/{id}", tags=["Movies"])
def get_movie(id: int = Path(ge = 1, le=2000)):
    for movie in movies:
        if movie["id"] == id:
                return JSONResponse(content=movie)
    return JSONResponse(content={"message": "Movie not found"}, status_code=404)


@app.get('/movies/', tags=["Movies"])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    data = [movie for movie in movies if movie["category"] == category]
    return JSONResponse(content=data)

@app.post("/movies", tags=["Movies"])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies 

@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie):
	for item in movies:
		if item["id"] == id:
			item['title'] = movie.title
			item['overview'] = movie.overview
			item['year'] = movie.year
			item['rating'] = movie.rating
			item['category'] = movie.category
			return movies

@app.delete('/movies/{id}', tags=["Movies"])
def delete_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
    return movies
            

