from datetime import date
from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Coroutine, Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = "My Movie API "
app.version = "0.0.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        valid_token = validate_token(auth.credentials)
        if valid_token['username'] != 'admin':
            raise HTTPException(status_code=403, detail="Unauthorized")
     
class User(BaseModel):
    username: str
    password: str

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

@app.post("/login", tags=["auth"])
def login(user: User):
     if user.username == "admin" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content={"token": token})
    
@app.get("/movies", tags=["Movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get("/movies/{id}", tags=["Movies"], response_model=Movie)
def get_movie(id: int = Path(ge = 1, le=2000)) -> Movie:
    for movie in movies:
        if movie["id"] == id:
                return JSONResponse(content=movie)
    return JSONResponse(status_code=404, content={"message": "Movie not found"})


@app.get('/movies/', tags=["Movies"], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [movie for movie in movies if movie["category"] == category]
    return JSONResponse(content=data)

@app.post("/movies", tags=["Movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message": "Movie created successfully"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie):
	for item in movies:
		if item["id"] == id:
			item['title'] = movie.title
			item['overview'] = movie.overview
			item['year'] = movie.year
			item['rating'] = movie.rating
			item['category'] = movie.category
			return JSONResponse(status_code=200, content={"message": "Movie updated successfully"})

@app.delete('/movies/{id}', tags=["Movies"], response_model=dict, status_code=200)
def delete_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            return JSONResponse(status_code=200, content={"message": "Movie deleted successfully"})