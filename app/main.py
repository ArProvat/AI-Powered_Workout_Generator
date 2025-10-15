
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ai_component.chains.generate_daily_workout import get_daily_workout_chain
from ai_component.chains.genarate_motivation import get_motivation_chain
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from enum import Enum

import os
import json

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

class MonthlyWorkoutResponse(BaseModel):
    user_profile: dict
    monthly_plan: List[DailyWorkout]
    summary: str


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
@app.post("/generate-workout", response_model=MonthlyWorkoutResponse)
async def generate_workout(request: WorkoutRequest):
    try:
        user_profile = {
            "mission": request.mission.value,
            "time_commitment": request.time_commitment.value,
            "gear": request.gear.value,
            "squad": request.squad.value    
        }
        monthly_plan = []
        summary = ""
        
        for day in range(1,31):
            try:
                day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][(day - 1) % 7]
                week = (day - 1) // 7 + 1
                
                user_input = {
                    "day": day,
                    "week": week,
                    "day_of_week": day_of_week,
                    **user_profile
                }
                
                # Generate daily workout plan
                workout_response = get_daily_workout_chain(user_input, session_id="user_1")
                workout_plan = json.loads(workout_response)
                
                # Generate motivational text
                motivational_text = get_motivation_chain(user_input)
                
                daily_workout = DailyWorkout(
                    day=day,
                    workout_plan=workout_plan,
                    motivational_text=motivational_text
                )
                monthly_plan.append(daily_workout)
            except Exception as e:
                monthly_plan.append(DailyWorkout(
                    day=day,
                    workout_plan=[
                        f"Warm-up: Dynamic stretching - 5 mins",
                        f"Main workout: Focus on {request.mission.value}",
                        f"Cool-down: Static stretching - 5 mins"
                    ],
                    motivational_text=f"Day {day}: Stay committed to your journey!"
                ))
        
        summary = f"Generated a 30-day workout plan focused on {request.mission.value} with {request.gear.value} equipment."
        return MonthlyWorkoutResponse(
            user_profile=user_profile,
            monthly_plan=monthly_plan,
            summary=summary
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating workout plan: {str(e)}")

@app.post("/generate-workout-debug", response_model=DailyWorkout)
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
        day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][(day - 1) % 7]
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


