from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient

app=FastAPI()
MONGO_URL="mongodb://localhost:27017"
client=AsyncIOMotorClient(MONGO_URL)
db=client["movie_review"]
collection=db["reviews"]

class Review(BaseModel):
    title: str = Field(..., example="enter the movie name")
    review: str = Field(..., example="enter ur review here")
    rating: float = Field(..., ge=0, le=5, example="rate from 0 to 5")
    reviewer: str = Field(..., example="enter your name")

class ReviewOut(Review):
    id: str

@app.post("/reviews/", response_model=ReviewOut)
async def create_review(review: Review):
    review_dict = review.model_dump()
    result = await collection.insert_one(review_dict)
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to create review")
    
    review_out = ReviewOut(id=str(result.inserted_id), **review_dict)
    return review_out
@app.get("/reviews",response_model=list[ReviewOut])
async def get_reviews():
    reviews = []
    async for review in collection.find():
        review_out = ReviewOut(id=str(review["_id"]), **review)
        reviews.append(review_out)
    return reviews
@app.get("/reviews/{review_id}", response_model=ReviewOut)
async def get_user_by_id(review_id: str):
    review = await collection.find_one({"_id": ObjectId(review_id)})
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return ReviewOut(id=str(review["_id"]), **review)

@app.put("/reviews/{review_id}", response_model=ReviewOut)
async def update_review(review_id: str, review: Review):
    result = await collection.update_one({"_id": ObjectId(review_id)}, {"$set": review.model_dump()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")

    updated_review = await collection.find_one({"_id": ObjectId(review_id)})
    if updated_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    return ReviewOut(id=str(updated_review["_id"]), **updated_review)
@app.delete("/reviews/{review_id}")
async def delete_review(review_id: str):
    result = await collection.delete_one({"_id": ObjectId(review_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"detail": "Review deleted successfully"}
