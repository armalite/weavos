from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime, timedelta

app = FastAPI()

# Mocked Kafka events
mocked_events = [
    {"table": "X", "product": "Product A", "timestamp": datetime.now().isoformat()}
]

# Ruleset storage
rulesets: Dict[str, List[Dict[str, Any]]] = {}

class RuleSet(BaseModel):
    product: str
    depends_on_table: str
    depends_on_product: str
    cooldown_hours: int
    last_triggered: datetime = datetime.min

@app.post("/register_ruleset/")
async def register_ruleset(ruleset: RuleSet):
    if ruleset.product not in rulesets:
        rulesets[ruleset.product] = []
    rulesets[ruleset.product].append(ruleset.dict())
    return {"message": "Ruleset registered successfully"}

def evaluate_rulesets():
    now = datetime.now()
    for product, product_rulesets in rulesets.items():
        for ruleset in product_rulesets:
            if now - ruleset['last_triggered'] < timedelta(hours=ruleset['cooldown_hours']):
                continue  # Skip evaluation if within cooldown period
            for event in mocked_events:
                if event["product"] == ruleset["depends_on_product"] and event["table"] == ruleset["depends_on_table"]:
                    trigger_workflow(product, ruleset)
                    ruleset['last_triggered'] = now  # Update last triggered time

def trigger_workflow(product: str, ruleset: Dict[str, Any]):
    # Placeholder for triggering a workflow
    print(f"Triggering workflow for {product} based on ruleset {ruleset}")

@app.get("/evaluate/")
async def evaluate():
    evaluate_rulesets()
    return {"message": "Evaluation complete"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
