import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Kitten, Inquiry, Testimonial

app = FastAPI(title="Gentle Giant Maine Coon API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Gentle Giant Maine Coon API Running"}


# Health check + DB info
@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:120]}"

    return response


# ------------------------------
# Kittens Endpoints
# ------------------------------

class KittenOut(Kitten):
    id: Optional[str] = None


@app.get("/api/kittens", response_model=List[KittenOut])
def list_kittens(color: Optional[str] = None, location: Optional[str] = None, sex: Optional[str] = None, status: Optional[str] = None):
    if db is None:
        return []
    query = {}
    if color:
        query["color"] = {"$regex": color, "$options": "i"}
    if location:
        query["location"] = {"$regex": location, "$options": "i"}
    if sex:
        query["sex"] = {"$regex": sex, "$options": "i"}
    if status:
        query["status"] = status

    docs = get_documents("kitten", query)
    out: List[KittenOut] = []
    for d in docs:
        d["id"] = str(d.get("_id"))
        d.pop("_id", None)
        out.append(KittenOut(**d))
    return out


@app.post("/api/kittens", response_model=dict)
def create_kitten(kitten: Kitten):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not available")
    inserted_id = create_document("kitten", kitten)
    return {"id": inserted_id}


# ------------------------------
# Inquiries (Waitlist / Contact)
# ------------------------------

class InquiryResponse(BaseModel):
    id: str
    success: bool = True


@app.post("/api/inquiries", response_model=InquiryResponse)
def submit_inquiry(inquiry: Inquiry):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not available")
    inserted_id = create_document("inquiry", inquiry)
    return InquiryResponse(id=inserted_id)


# ------------------------------
# Testimonials
# ------------------------------

class TestimonialOut(Testimonial):
    id: Optional[str] = None


@app.get("/api/testimonials", response_model=List[TestimonialOut])
def list_testimonials(limit: int = 10):
    if db is None:
        # graceful fallback with a couple of curated examples
        examples = [
            {
                "author": "Sofia R.",
                "handle": "@sof_and_max",
                "content": "Our shaded silver boy is massive and so gentle. The FaceTime call sealed our trust—everything was exactly as promised.",
                "rating": 5,
                "avatar_url": "https://images.unsplash.com/photo-1607746882042-944635dfe10e?w=200&h=200&fit=crop"
            },
            {
                "author": "Michael T.",
                "handle": "@mt_angeleno",
                "content": "Hand delivery to LA was seamless. Genetics and health transparency are top-tier. Couldn’t be happier!",
                "rating": 5,
                "avatar_url": "https://images.unsplash.com/photo-1544723795-3fb6469f5b39?w=200&h=200&fit=crop"
            }
        ]
        return [TestimonialOut(**e) for e in examples][:limit]

    docs = get_documents("testimonial", {}, limit)
    out: List[TestimonialOut] = []
    for d in docs:
        d["id"] = str(d.get("_id"))
        d.pop("_id", None)
        out.append(TestimonialOut(**d))
    return out


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
