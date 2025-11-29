from datetime import datetime
from collections import defaultdict
import pulp

class MealPlanner:
    def __init__(self, recipe_matcher):
        self.recipe_matcher = recipe_matcher

    def _estimate_expiry_priority(self, pantry):
        pri = {}
        for it in pantry:
            if 'estimated_expiry_date' in it:
                try:
                    d = datetime.fromisoformat(it['estimated_expiry_date'])
                    days = (d - datetime.now()).days
                except:
                    days = 7
            else:
                days = 7
            pri[it['name'].lower()] = max(0, days)
        return pri

    def generate_weekly_plan(self, pantry, preferences=None):
        pantry_names = [p['name'].lower() for p in pantry]
        expiry_map = self._estimate_expiry_priority(pantry)
        candidates = self.recipe_matcher.search_recipes(pantry_names, topk=20)
        def score_recipe(r):
            s = 0
            for ing in r['ingredients']:
                name = ing.lower()
                if name in expiry_map:
                    s += max(0, 10 - expiry_map[name])
                else:
                    s += 0.5
            return s
        scored = sorted(candidates, key=score_recipe, reverse=True)
        plan = {"week": [], "selected_recipes": []}
        day_count = 7
        i = 0
        for day in range(day_count):
            if i >= len(scored):
                i = 0
            chosen = scored[i]
            plan['week'].append({"day": day+1, "recipe": chosen})
            plan['selected_recipes'].append(chosen['id'])
            i += 1
        grocery = defaultdict(int)
        for rid in plan['selected_recipes']:
            r = self.recipe_matcher.get_recipe_by_id(rid)
            for ing in r['ingredients']:
                if ing.lower() not in pantry_names:
                    grocery[ing] += 1
        plan['grocery_list'] = [{"item":k,"qty":v} for k,v in grocery.items()]
        return plan

    def generate_weekly_plan_ilp(self, pantry, preferences=None):
        pantry_names = [p['name'].lower() for p in pantry]
        candidates = self.recipe_matcher.search_recipes(pantry_names, topk=50)
        expiry_map = self._estimate_expiry_priority(pantry)
        utilities = {}
        for r in candidates:
            u = 0
            for ing in r['ingredients']:
                if ing.lower() in expiry_map:
                    u += max(0, 10 - expiry_map[ing.lower()])
            utilities[r['id']] = u + 1
        prob = pulp.LpProblem('plan', pulp.LpMaximize)
        x = pulp.LpVariable.dicts('x', utilities.keys(), lowBound=0, upBound=7, cat='Integer')
        penalty = {}
        for rid in utilities:
            r = next(filter(lambda rr: rr['id']==rid, candidates))
            missing = sum(1 for ing in r['ingredients'] if ing.lower() not in pantry_names)
            penalty[rid] = missing
        prob += pulp.lpSum([utilities[rid]*x[rid] - 0.5*penalty[rid]*x[rid] for rid in utilities])
        prob += pulp.lpSum([x[rid] for rid in utilities]) == 7
        prob.solve(pulp.PULP_CBC_CMD(msg=False))
        plan = []
        for rid in utilities:
            val = int(pulp.value(x[rid]))
            for _ in range(val):
                plan.append(self.recipe_matcher.get_recipe_by_id(rid))
        grocery = {}
        pantry_names_set = set(pantry_names)
        for r in plan:
            for ing in r['ingredients']:
                if ing.lower() not in pantry_names_set:
                    grocery[ing] = grocery.get(ing,0)+1
        return {"week": [{"recipe": r} for r in plan], "grocery_list":[{"item":k,"qty":v} for k,v in grocery.items()]}
