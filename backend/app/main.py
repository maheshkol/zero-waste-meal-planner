from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import uuid
import os

from .image_processing import parse_pantry_image
from .recipe_matcher import RecipeMatcher
from .optimizer import MealPlanner
from .models import PantryItemCreate

app = FastAPI(title="Zero-Waste Meal Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory stores for prototype
PANTRIES = {}   # user_id -> list of pantry items
RECIPE_MATCHER = RecipeMatcher()   # loads/creates vectorstore
PLANNER = MealPlanner(RECIPE_MATCHER)

class GeneratePlanRequest(BaseModel):
    user_id: str
    week_start: str = None
    preferences: dict = {}

@app.post("/api/pantry/upload-photo")
async def upload_pantry_photo(user_id: str, file: UploadFile = File(...)):
    os.makedirs("tmp_uploads", exist_ok=True)
    filename = f"tmp_uploads/{uuid.uuid4().hex}_{file.filename}"
    with open(filename, "wb") as f:
        shutil.copyfileobj(file.file, f)
    parsed_items = parse_pantry_image(filename)
    items = PANTRIES.setdefault(user_id, [])
    items.extend(parsed_items)
    return {"parsed_items": parsed_items}

@app.post("/api/pantry/add")
async def add_pantry_item(user_id: str, item: PantryItemCreate):
    items = PANTRIES.setdefault(user_id, [])
    items.append(item.dict())
    return {"status": "ok", "pantry": items}

@app.get("/api/pantry")
async def get_pantry(user_id: str):
    return {"pantry": PANTRIES.get(user_id, [])}

@app.post("/api/plan/generate")
async def generate_plan(req: GeneratePlanRequest):
    pantry = PANTRIES.get(req.user_id, [])
    if not pantry:
        raise HTTPException(status_code=400, detail="Pantry empty. Add items or upload photo.")
    plan = PLANNER.generate_weekly_plan(pantry, preferences=req.preferences)
    return {"plan": plan}

@app.post("/api/recipes/adjust")
async def adjust_recipe(user_id: str, recipe_id: str, pantry_only: bool = True):
    recipe = RECIPE_MATCHER.get_recipe_by_id(recipe_id)
    if recipe is None:
        raise HTTPException(404, "recipe not found")
    pantry = PANTRIES.get(user_id, [])
    adjusted = RECIPE_MATCHER.adapt_recipe_to_pantry(recipe, pantry)
    return {"adjusted_recipe": adjusted}
