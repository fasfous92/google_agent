import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from calendar_tools import CalendarTools
from llm import create_agent_llm, get_final_answer

# --- Initializing the scopes and credentials because our agents cannot work without it ---

# Define the scope you need
# IMPORTANT: Use 'calendar.events' to read AND write events
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

def get_calendar_service():
    """Authenticates and returns a Google Calendar service object."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        print("here")
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                print(f"we will proceed with a new intiailization of the credentials")
                flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
                # This is the line that requires human interaction
                print("Please authorize in the browser that opens...")
                creds = flow.run_local_server(port=0)
            # print("here 1")

            # creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            # This is the line that requires human interaction
            print("Please authorize in the browser that opens...")
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
            
    return build("calendar", "v3", credentials=creds)

# --- Initialize Service and Agent ---

# 2. Authenticate and get the service object *once*
try:
    service = get_calendar_service()
    print("Google Calendar service initialized.")

    # 3. Create an *instance* of your tool class, passing the service to it
    calendar_tool_kit = CalendarTools(service=service)

    # 4. Get the list of tools *from that instance*
    tools = [
        calendar_tool_kit.add_google_calendar_event,
        # calendar_tool_kit.list_google_calendar_events, # if you added more
    ]

    # 5. Now, build your agent with this list of tools
    agent= create_agent_llm(
        tools=tools,
        system_prompt="You are a helpful assistant that manages Google Calendar events."
    )
    
    print("Agent is ready.")
    
    inputs = {"messages": [{"role": "user", "content": "what's 1+2?"}]}
    # for chunk in agent.stream(inputs, stream_mode="updates"):
    #     print(chunk)

    
    response = agent.invoke({"input": "what's 1+2?"})
    final_answer=get_final_answer(response)
    print(final_answer)
    # print(response['output'])

except Exception as e:
    print(f"Failed to initialize: {e}")