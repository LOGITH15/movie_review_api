from pydantic import BaseModel, Field

class Review(BaseModel):
    title: str = Field(..., example="enter the movie name")
    review: str = Field(..., example="enter ur review here")
    rating: float = Field(..., ge=0, le=5, example="rate from 0 to 5")
    reviewer: str = Field(..., example="enter your name")

class ReviewOut(Review):
    id: str
