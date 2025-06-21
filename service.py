from bson import ObjectId
from fastapi import HTTPException
from database import collection
from models import Review, ReviewOut

async def create_review_service(review: Review):
    review_dict = review.model_dump()
    result = await collection.insert_one(review_dict)
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to create review")
    return ReviewOut(id=str(result.inserted_id), **review_dict)

async def get_reviews_service():
    reviews = []
    async for review in collection.find():
        review_out = ReviewOut(id=str(review["_id"]), **review)
        reviews.append(review_out)
    return reviews

async def get_review_by_id_service(review_id: str):
    review = await collection.find_one({"_id": ObjectId(review_id)})
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return ReviewOut(id=str(review["_id"]), **review)

async def update_review_service(review_id: str, review: Review):
    result = await collection.update_one({"_id": ObjectId(review_id)}, {"$set": review.model_dump()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")

    updated_review = await collection.find_one({"_id": ObjectId(review_id)})
    if updated_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    return ReviewOut(id=str(updated_review["_id"]), **updated_review)
