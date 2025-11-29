import os
import requests
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def adapt_recipe_with_openai(recipe, pantry):
    pantry_names = [p['name'].lower() for p in pantry]
    prompt = f"""
You are a helpful kitchen assistant. Adapt the following recipe to use available pantry items.
Recipe title: {recipe.get('title')}
Ingredients: {', '.join(recipe.get('ingredients',[]))}
Steps: {', '.join(recipe.get('steps',[]))}
Pantry items: {', '.join(pantry_names)}

Return a JSON with keys:
- adapted_ingredients: list of {{"ingredient": <name>, "quantity": <text>, "status": "available|missing|substituted", "substitute": <text or null>}}
- adapted_steps: list of steps adapted for substitutions
- notes: any important notes (max 50 words)
Only return the JSON.
    """
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type":"application/json"}
    data = {
        "model":"gpt-4o-mini",
        "messages":[{"role":"user","content":prompt}],
        "temperature":0.2,
        "max_tokens":600,
    }
    resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=30)
    if resp.status_code != 200:
        raise Exception(f"LLM error: {resp.text}")
    out = resp.json()
    content = out['choices'][0]['message']['content']
    import re
    match = re.search(r'(\{[\s\S]+\})', content)
    if not match:
        raise Exception("Could not parse LLM output")
    return json.loads(match.group(1))
