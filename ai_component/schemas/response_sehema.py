from langchain.output_parsers import StructuredOutputParser, ResponseSchema

# Define the response schema for the workout plan

response_schemas = [
    ResponseSchema(name="section", description="Workout section: Warm-up, Main Workout, or Cool-down"),
    ResponseSchema(name="exercise", description="Name of the exercise"),
    ResponseSchema(name="sets", description="Number of sets (integer or null if not applicable)"),
    ResponseSchema(name="reps", description="Number of reps per set (integer or null if not applicable)"),
    ResponseSchema(name="duration", description="Duration or time spent on this exercise, e.g., '3 minutes'"),
]

parser = StructuredOutputParser.from_response_schemas(response_schemas)
# Get the format instructions for the LLM
format_instructions = parser.get_format_instructions()