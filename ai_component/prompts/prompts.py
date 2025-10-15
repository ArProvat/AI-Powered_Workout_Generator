
daily_workout_prompt = """
Generate a workout for **Day {user_inputs['day']} (Week {user_inputs['week']}, {user_inputs['day_of_week']})**.

User Profile:
- Goal: {user_inputs['mission']}
- Time: {user_inputs['time_commitment']}
- Gear: {user_inputs["gear"]}
- Squad Type: {user_inputs['squad']}

Constraints:
1. Fit within time limit
2. Use only listed gear
3. Focus on goal area
4. Include warm-up, main workout, and cool-down
5. Be specific with sets/reps/duration
6. Adjust intensity by week
7. Reference previous plan for balance

Return strictly as JSON (array of exercise objects).
"""

motivation_prompt = """
Generate a short, powerful motivational message (max 2 sentences) for day {user_inputs['day']} of a workout plan.

User Profile:
- Mission: {user_inputs['mission']}
- Squad: {user_inputs['squad']}
- Time: {user_inputs['time_commitment']}

The message should:
- Be inspiring and energetic
- Reference their squad identity ({user_inputs['squad']})
- Connect to their mission ({user_inputs['mission']})
- Be unique and not repetitive

Return ONLY the motivational message, nothing else.
"""

system_prompt = """
You are an expert world-class fitness coach and motivational trainer.
Design personalized daily workouts that are:
1. Safe and goal-oriented
2. Fit user’s equipment and time
3. Progressively challenging over 4 weeks
4. Motivational, engaging, and varied

Follow structure:
- Warm-up (mobility/cardio)
- Main workout (mission-specific)
- Cool-down (stretching/recovery)

Incorporate previous session context from chat history to ensure progression and recovery balance.

You must output valid JSON following this schema:
{{format_instructions}}

Return ONLY the JSON — no explanations or extra text.
"""
