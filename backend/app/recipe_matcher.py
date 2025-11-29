import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
from typing import List, Dict

class RecipeMatcher:
    def __init__(self, recipe_file: str = None, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.recipes = []
        self.embeddings = None
        self.index = None
        if recipe_file and os.path.exists(recipe_file):
            self.load_recipes(recipe_file)
        else:
            self._load_toy_recipes()

    def _load_toy_recipes(self):
        self.recipes = [
            {"id":"r1","title":"Tomato Omelette","ingredients":["eggs","tomato","salt","pepper"], "steps":["mix","cook"]},
            {"id":"r2","title":"Spinach Rice","ingredients":["rice","spinach","salt","garlic"], "steps":["cook rice","saute spinach"]},
            {"id":"r3","title":"Chicken Curry","ingredients":["chicken","onion","tomato","spices"], "steps":["marinate","cook"]},
        ]
        self._build_index()

    def load_recipes(self, path):
        with open(path,'r') as f:
            self.recipes = json.load(f)
        self._build_index()

    def _build_index(self):
        corpus = [" ".join(r["ingredients"]) for r in self.recipes]
        emb = self.model.encode(corpus, convert_to_numpy=True, show_progress_bar=False)
        self.embeddings = emb.astype('float32')
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)

    def search_recipes(self, pantry_items: List[str], topk: int = 5) -> List[Dict]:
        query = " ".join(pantry_items)
        q_emb = self.model.encode([query], convert_to_numpy=True).astype('float32')
        dists, ids = self.index.search(q_emb, topk)
        results = []
        for i in ids[0]:
            if i < len(self.recipes):
                results.append(self.recipes[i])
        return results

    def get_recipe_by_id(self, rid):
        for r in self.recipes:
            if r["id"] == rid:
                return r
        return None

    def adapt_recipe_to_pantry(self, recipe, pantry):
        pantry_names = [p['name'].lower() for p in pantry]
        adapted = recipe.copy()
        adapted['missing'] = []
        adapted['substitutions'] = {}
        adapted['available'] = []
        for ing in recipe["ingredients"]:
            if ing.lower() in pantry_names:
                adapted['available'].append(ing)
            else:
                adapted['missing'].append(ing)
                subs = {"spinach":"kale","tomato":"canned tomato","butter":"oil"}
                if ing in subs:
                    adapted['substitutions'][ing] = subs[ing]
        return adapted
