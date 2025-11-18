
# In calendar_tools.py

from langchain_core.tools import tool
from googleapiclient.errors import HttpError
from typing import Dict, Any
from datetime import datetime  # <--- Use this specific import
class CalendarTools:
    
    # 1. The class is initialized with the 'service' object
    def __init__(self, service):
        self.service = service

    # 2. The @tool decorator is applied to the *method*
    @tool
    def add_google_calendar_event(self, details: Dict[str, Any]) -> str:
        """
        Use this tool to create a new event in a Google Calendar.
        
        The 'details' argument must be a dictionary... (etc.)
        """
        
        # 3. The tool now uses 'self.service'
        if not self.service:
            return "Error: Google Calendar service is not initialized."

        try:
            event_body = {
                'summary': details['summary'],
                'start': {
                    'dateTime': details['start_datetime'],
                    'timeZone': details.get('time_zone', 'UTC'),
                },
                'end': {
                    'dateTime': details['end_datetime'],
                    'timeZone': details.get('time_zone', 'UTC'),
                },
                'location': details.get('location'),
                'description': details.get('description'),
                'attendees': details.get('attendees', []),
            }
            
            event_body = {k: v for k, v in event_body.items() if v is not None}
            calendar_id = details.get('calendarId', 'primary')
            
            # Use self.service to make the API call
            event = self.service.events().insert(
                calendarId=calendar_id, 
                body=event_body
            ).execute()
            
            return f"Event created successfully: {event.get('htmlLink')}"
            
        except HttpError as error:
            return f"An error occurred: {error}"
        except KeyError as e:
            return f"Error: Missing required detail: {e}."
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    # --- You could add more tools here ---
    # @tool
    # def list_google_calendar_events(self, ...):
    #     ...
    #     result = self.service.events().list(...).execute()
    #     ...
    
    @tool
    def get_current_date() -> str:
        """
        Returns the current date, day of the week, and time.
        """
        # Using a very clear format helps the model parse it
        return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
