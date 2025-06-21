from fastapi import FastAPI, HTTPException
from models import Review, ReviewOut
from service import (
    create_review_service,
    get_reviews_service,
    get_review_by_id_service,
    update_review_service
)

app = FastAPI()

@app.post("/reviews/", response_model=ReviewOut, description="Add a new movie review")
async def create_review(review: Review):
    return await create_review_service(review)

@app.get("/reviews", response_model=list[ReviewOut], description="See all movie reviews")
async def get_reviews():
    return await get_reviews_service()

@app.get("/reviews/{review_id}", response_model=ReviewOut, description="Get movie review by it's ID")
async def get_user_by_id(review_id: str):
    return await get_review_by_id_service(review_id)

@app.put("/reviews/{review_id}", response_model=ReviewOut, description="Update the movie review by ID")
async def update_review(review_id: str, review: Review):
    return await update_review_service(review_id, review)
