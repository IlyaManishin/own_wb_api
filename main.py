from fastapi import FastAPI
from fastapi import Request
from parser import get_promotions, get_keywords_stats, get_clusters
app = FastAPI()


@app.get("/")
def root(request: Request):
    value = request.headers.get("Authorization")
    if not value:
        return {"None" : "None"}
    result = get_promotions(value)
    return result

@app.get("/keywords")
def keywords(request: Request):
    value = request.headers.get("Authorization")
    if not value:
        return {"None" : "None"}
    result = get_keywords_stats(value)
    return result

@app.get("/clusters")
def keywords(request: Request):
    value = request.headers.get("Authorization")
    if not value:
        return {"None" : "None"}
    result = get_clusters(value)
    return result