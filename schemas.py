"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List

# Example schemas (kept for reference/other tools)
class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: Optional[str] = Field(None, description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# --------------------------------------------------
# Gentle Giant Maine Coon App Schemas
# --------------------------------------------------

class Kitten(BaseModel):
    """
    Collection: "kitten"
    Represents an available or example kitten card.
    """
    name: str = Field(..., description="Kitten name")
    color: str = Field(..., description="Color/pattern, e.g., Smoke Black")
    sex: str = Field(..., description="Male or Female")
    age_weeks: Optional[int] = Field(None, ge=0, description="Age in weeks")
    location: str = Field(..., description="Miami, FL or Los Angeles, CA")
    giant: bool = Field(True, description="Giant size tag")
    price_usd: Optional[int] = Field(None, ge=0, description="Optional price for admin use")
    status: str = Field("available", description="available / reserved / sold")
    images: List[HttpUrl] = Field(default_factory=list, description="Primary + gallery images")
    description: Optional[str] = Field(None, description="Short personality notes")

class Inquiry(BaseModel):
    """
    Collection: "inquiry"
    Waitlist/contact form submissions.
    """
    name: str = Field(...)
    email: EmailStr = Field(...)
    phone: Optional[str] = Field(None, description="Phone for text/FaceTime")
    preferred_color: Optional[str] = Field(None)
    location: Optional[str] = Field(None)
    contact_method: Optional[str] = Field(None, description="text | facetime | email")
    message: Optional[str] = Field(None)

class Testimonial(BaseModel):
    """
    Collection: "testimonial"
    """
    author: str = Field(...)
    handle: Optional[str] = Field(None, description="Social handle like @giantcoonsfan")
    content: str = Field(...)
    rating: int = Field(5, ge=1, le=5)
    avatar_url: Optional[HttpUrl] = Field(None)
    image_url: Optional[HttpUrl] = Field(None)
