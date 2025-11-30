from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import pandas as pd
from typing import List, Optional
from pydantic import BaseModel
from data_manager import load_data_core
from auth_manager import SecureAuthManager

app = FastAPI(
    title="Virunga Dashboard API",
    description="API pour accéder aux données du Virunga Intelligent Dashboard",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()
auth_manager = SecureAuthManager()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify credentials against users.json"""
    if not auth_manager.check_login(credentials.username, credentials.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Data Models
class Activity(BaseModel):
    Date_Activite: Optional[str]
    Nom: Optional[str]
    Organisateur: Optional[str]
    Type: Optional[str]
    Secteur: Optional[str]
    Lieu_Precis: Optional[str]
    Total_Participants: Optional[int]

class Visit(BaseModel):
    Date: Optional[str]
    Nombre: Optional[int]
    Objet: Optional[str]
    Organisation: Optional[str]

class PressArticle(BaseModel):
    Date: Optional[str]
    Media: Optional[str]
    Titre: Optional[str]
    Ton: Optional[str]
    Thematique: Optional[str]
    Zone: Optional[str]

# Load data on startup
df_activities = pd.DataFrame()
df_visits = pd.DataFrame()
df_press = pd.DataFrame()

@app.on_event("startup")
async def startup_event():
    global df_activities, df_visits, df_press
    df_activities, df_visits, df_press = load_data_core()
    # Convert dates to string for JSON serialization
    if 'Date_Activite' in df_activities.columns:
        df_activities['Date_Activite'] = df_activities['Date_Activite'].astype(str)
    if 'Date' in df_visits.columns:
        df_visits['Date'] = df_visits['Date'].astype(str)
    if 'Date' in df_press.columns:
        df_press['Date'] = df_press['Date'].astype(str)

@app.get("/")
def read_root():
    return {"message": "Welcome to Virunga Dashboard API. Visit /docs for documentation."}

@app.get("/activities", response_model=List[Activity])
def get_activities(username: str = Depends(authenticate)):
    """Get all field activities"""
    return df_activities.to_dict(orient="records")

@app.get("/visits", response_model=List[Visit])
def get_visits(username: str = Depends(authenticate)):
    """Get all visits and internships"""
    return df_visits.to_dict(orient="records")

@app.get("/press", response_model=List[PressArticle])
def get_press(username: str = Depends(authenticate)):
    """Get all press reviews"""
    return df_press.to_dict(orient="records")

@app.get("/stats")
def get_stats(username: str = Depends(authenticate)):
    """Get global statistics"""
    return {
        "total_activities": len(df_activities),
        "total_visits": int(df_visits['Nombre'].sum()) if not df_visits.empty else 0,
        "total_press_articles": len(df_press),
        "last_updated": pd.Timestamp.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
