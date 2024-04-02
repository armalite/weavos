from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

app = FastAPI()

# Placeholder storage for rulesets
rulesets: Dict[str, List[Dict[str, Dict]]] = {}

# Pydantic models for request body validation
class ProcessIdentifier(BaseModel):
    type: str
    identifier: str

class SourceIdentifier(BaseModel):
    type: str
    identifier: str

class FreshnessCriteria(BaseModel):
    businessDataFreshnessMinutes: Optional[int] = Field(None, ge=0)
    technicalDataFreshnessMinutes: Optional[int] = Field(None, ge=0)
    jobExecutionFreshnessMinutes: Optional[int] = Field(None, ge=0)

class Criteria(BaseModel):
    eventType: str
    freshnessCriteria: FreshnessCriteria
    details: dict

class Dependency(BaseModel):
    dependencyType: str
    sourceIdentifier: SourceIdentifier
    criteria: Criteria

class RuleSetRegistration(BaseModel):
    processIdentifier: ProcessIdentifier
    dependencies: List[Dependency]

@app.post("/register_ruleset/")
async def register_ruleset(ruleset: RuleSetRegistration):
    # Convert process identifier to a unique key
    process_key = f"{ruleset.processIdentifier.type}:{ruleset.processIdentifier.identifier}"
    # Ensure a list exists for this key
    if process_key not in rulesets:
        rulesets[process_key] = []
    # Append the new ruleset
    rulesets[process_key].append(ruleset.dict())
    return {"message": "Ruleset registered successfully"}

# Placeholder endpoint for rule evaluation
@app.get("/evaluate/")
async def evaluate():
    # Logic for evaluating rules against incoming events would go here
    return {"message": "Evaluation triggered"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
