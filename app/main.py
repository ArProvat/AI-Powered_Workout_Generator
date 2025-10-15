
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ai_component.chains.generate_daily_workout import get_daily_workout_chain
from ai_component.chains.genarate_motivation import get_motivation_chain
from pydantic import BaseModel, Field, ConfigDict
from fastapi.responses import StreamingResponse
from typing import List, Optional
from enum import Enum
import datetime

import os
import json
 
import datetime

current_date = datetime.date.today()
day_name = current_date.strftime("%A")



# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered Workout Generator",
    version="1.0.0",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
    )

# Enums for input validation

class Mission(str, Enum):
    lose_fat = "Lose Fat"
    build_strength = "Build Strength"
    move_pain_free = "Move Pain-Free"
    tactical_readiness = "Tactical Readiness"

class TimeCommitment(str, Enum):
    ten_min = "10 min"
    twenty_thirty_min = "20–30 min"
    forty_five_plus_min = "45+ min"

class Gear(str, Enum):
    bodyweight = "Bodyweight"
    sandbag = "Sandbag"
    dumbbells = "Dumbbells"
    full_gym = "Full Gym"

class Squad(str, Enum):
    lone_wolf = "Lone Wolf"
    guardian = "Guardian"
    warrior = "Warrior"
    rebuilder = "Rebuilder"
    
# Request Models
class WorkoutRequest(BaseModel):
    mission: Mission = Field(..., description="User's fitness mission")
    time_commitment: TimeCommitment = Field(..., description="Time available for workout")
    gear: Gear = Field(..., description="Available equipment")
    squad: Squad = Field(..., description="User's squad type")
    
    class Config:
        schema_extra = {
            "example": {
                "mission": "Build Strength",
                "time_commitment": "20–30 min",
                "gear": "Dumbbells",
                "squad": "Warrior"
            }}
        
class DailyWorkout(BaseModel):
    day: int
    workout_plan: List[dict]
    motivational_text: str



# Endpoints
@app.get("/")
def root():
    return {
        "message": "Welcome to AI-Powered Workout Generator",
        "docs": "/docs",
        "endpoints": {
            "generate_workout": "/generate-workout (POST)",
            "health": "/health (GET)"
        }
    }
@app.post("/generate-workout-stream")
async def generate_workout_stream_post(request: WorkoutRequest):
    """
    Stream 30 days of workout plans progressively.
    This is the approach for SSE with complex data.
    """
    async def event_stream():
        user_profile = {
            "mission": request.mission.value,
            "time_commitment": request.time_commitment.value,
            "gear": request.gear.value,
            "squad": request.squad.value    
        }
        
        for day in range(1, 3):
            try:
                day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][(day - 1) % 7]
                week = (day - 1) // 7 + 1
                
                user_input = {
                    "day": day,
                    "week": week,
                    "day_of_week": day_of_week,
                    **user_profile
                }
                
                # Generate workout and motivation
                workout_response = get_daily_workout_chain(user_input, session_id="stream_user")
                motivational_text = get_motivation_chain(user_input)
                
                # Parse workout response
                try:
                    workout_plan = json.loads(workout_response)
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error for day {day}: {e}")
                    workout_plan = {"error": "Failed to parse workout plan"}
                
                day_json = {
                    "day": day,
                    "workout_plan": workout_plan,
                    "motivational_text": motivational_text
                }

                # Send progress update
                yield f"data: {json.dumps(day_json)}\n\n"

            except Exception as e:
                print(f"Error generating workout for day {day}: {e}")
                yield f"data: {json.dumps({'day': day, 'error': str(e)})}\n\n"
        
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  
        }
    )

@app.post("/generate_daily_workout", response_model=DailyWorkout)
async def generate_daily_workout(request: WorkoutRequest,day: int = 1,):
    """    Generate a single day's workout plan."""
    try:
        user_profile = {
            "mission": request.mission.value,
            "time_commitment": request.time_commitment.value,
            "gear": request.gear.value,
            "squad": request.squad.value    
        }
         
        session_id = "user_1"
         
        day = day
        day_of_week = day_name
        week = (day - 1) // 7 + 1
        
        user_input = {
            "day": day,
            "week": week,
            "day_of_week": day_of_week,
            **user_profile
        }
        print(f"User Input: {user_input}")
        # Generate daily workout plan
        workout_response = get_daily_workout_chain(user_input, session_id=session_id)
        workout_plan = json.loads(workout_response)
        
        # Generate motivational text
        motivational_text = get_motivation_chain(user_input)
        
        daily_workout = DailyWorkout(
            day=day,
            workout_plan=workout_plan,
            motivational_text=motivational_text
        )
        
        return daily_workout
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating daily workout: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


