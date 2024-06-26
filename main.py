from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "My Movie API"
app.version = "0.0.1"


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
    return movies

@app.get("/movies/{id}", tags=["Movies"])
def get_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            return movie
    return {"message": "Movie not found"}