from langchain_core.output_parsers import JsonOutputParser
from typing import List, Optional
from pydantic import BaseModel, Field

class WorkoutStep(BaseModel):
    """A single step or exercise in the daily workout plan."""
    
    section: str = Field(
        description="The section of the workout: 'Warm-up', 'Main Workout', or 'Cool-down'."
    )
    exercise: str = Field(
        description="The name of the exercise (e.g., 'Jumping Jacks', 'Bench Press', 'Shoulder Stretch')."
    )
    sets: Optional[int] = Field(
        description="Number of sets (e.g., 3). Use 'null' if not applicable (e.g., for stretching or static holds)."
    )
    reps: Optional[int] = Field(
        description="Number of repetitions per set (e.g., 10). Use 'null' if not applicable (e.g., for duration-based exercises)."
    )
    rest: Optional[str] = Field(
        description="Rest time between sets (e.g., '60 seconds'). Use 'null' if not applicable."
    )
    duration: Optional[str] = Field(
        description="Duration or time spent on this exercise, e.g., '3 minutes', '30 seconds', or 'Until failure'. Use 'null' if sets and reps are provided."
    )

class WorkoutPlan(BaseModel):
    """The complete list of steps for the daily workout plan."""
    
    plan: List[WorkoutStep] = Field(
        description="A list containing all the individual exercises, steps, and their details in sequential order."
    )

parser = JsonOutputParser(pydantic_object=WorkoutPlan)
format_instructions = parser.get_format_instructions()