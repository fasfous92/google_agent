from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# 1. Define the Strict Schema
class GoogleEventSchema(BaseModel):
    summary: str = Field(description="The title of the event.")
    start_time: str = Field(description="Start time in ISO 8601 format (YYYY-MM-DDTHH:MM:SS).")
    end_time: str = Field(description="End time in ISO 8601 format.")
    location: str = Field(default="Dubai Office", description="Location.")
    description: str = Field(default="", description="Description.")
    attendees: List[str] = Field(default=[], description="List of emails.")
    timezone: str = Field(default="Asia/Dubai", description="Timezone.")

# 2. Define the "Mock" Tool
# This tool DOES NOT connect to Google. It just returns the data to YOU.
@tool(args_schema=GoogleEventSchema)
def generate_event_json(
    summary: str, 
    start_time: str, 
    end_time: str, 
    location: str, 
    description: str, 
    attendees: List[str], 
    timezone: str
):
    """
    Call this tool when you have all the details to create an event. 
    It will return the structured JSON for the user to execute locally.
    """
    # We simply return the arguments as a dictionary.
    # This is the "JSON" you are looking for.
    return {
        "summary": summary,
        "start": {
            "dateTime": start_time,
            "timeZone": timezone
        },
        "end": {
            "dateTime": end_time,
            "timeZone": timezone
        },
        "location": location,
        "description": description,
        "attendees": [{"email": email} for email in attendees]
    }
    
@tool
def get_current_date() -> str:
    """
    Returns the current date, day of the week, and time.
    """
    # Using a very clear format helps the model parse it
    return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")