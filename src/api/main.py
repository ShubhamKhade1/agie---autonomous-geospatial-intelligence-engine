from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.engine.dialogue.dialogue_manager import DialogueManager
from src.engine.reasoning.anomaly_scorer import AnomalyScorer
from src.engine.simulation.anomaly_simulator import generate_dark_vessel_anomaly
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AGIE",
    description="AI-powered geospatial intelligence engine for environmental monitoring.",
    version="1.0.0"
)

# Initialize Intelligence Engine Components
dialogue_manager = DialogueManager()
anomaly_scorer = AnomalyScorer()

# Global State for Demo Simulation
CURRENT_ANOMALY = {
    "priority": 42.1,
    "status": "No critical anomalies detected in the last 24h.",
    "roi": "Mumbai Coast"
}

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthStatus(BaseModel):
    status: str
    version: str

@app.get("/", response_model=HealthStatus)
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/anomalies")
async def get_anomalies(limit: int = 10):
    # TODO: Fetch from TimescaleDB
    return {"anomalies": []}

@app.post("/ingest/trigger")
async def trigger_ingestion(roi_id: str):
    # TODO: Trigger Celery task
    return {"message": f"Ingestion triggered for ROI: {roi_id}"}

class DialogueRequest(BaseModel):
    query: str
    roi_id: Optional[str] = "default_roi"

@app.post("/dialogue")
async def dialogue_handler(request: DialogueRequest):
    """
    Dialogue Layer (Step 5): Semantic search and operator interface.
    """
    # In a full run, we would retrieve recent anomalies from TimescaleDB here
    # Now using the DialogueManager's semantic query logic
    response = dialogue_manager.query_knowledge_base(request.query)
    
    return {
        "query": request.query,
        "response": response,
        "operator_action": "Verify ROI coordinates and deploy manual inspection if anomaly persists."
    }

@app.get("/anomalies/status")
async def get_current_anomaly_status():
    """
    Dashboard Status (Step 6): Returns the current live/simulated anomaly state.
    """
    return CURRENT_ANOMALY

@app.post("/simulation/inject")
async def inject_simulation():
    """
    Simulation Controller (Step 6): Triggers the 'Dark Vessel' scenario.
    """
    global CURRENT_ANOMALY
    
    # 1. Generate Synthetic Multi-Sensor Data
    signals = generate_dark_vessel_anomaly(points=100)
    
    # 2. Compute Hybrid Priority Score (STL + LSTM)
    priority_score = anomaly_scorer.compute_hybrid_score(signals, recency_val=1.0)
    
    # 3. Synthesize Operator Report via Gemini/DialogueManager
    report = dialogue_manager.query_knowledge_base("what is the current status?")
    
    # 4. Update Global State
    CURRENT_ANOMALY = {
        "priority": round(priority_score, 1),
        "status": report,
        "roi": "Mumbai Coast (Simulated)"
    }
    
    return {"message": "Dark Vessel Simulation Injected", "priority": CURRENT_ANOMALY["priority"]}
