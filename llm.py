#here we will creat the llm that will be used by the agent
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings
from langchain.agents import create_agent
from langchain_core.messages import AIMessage

import os



def create_llm():
    load_dotenv()
    os.environ["NVIDIA_API_KEY"] = os.getenv("NVIDIA_API_KEY")
    instruct_llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct") #meta/llama-3.1-8b-instruct meta/llama-3.1-70b-instruct qwen/qwen3-next-80b-a3b-thinking
    return instruct_llm

def create_agent_llm(system_prompt,tools=None):
    llm = create_llm()
    agent= create_agent(model=llm, tools=tools, system_prompt=system_prompt)
    return agent
    
def get_final_answer(chunk):
    ai_message=chunk['messages'][-1]
    if isinstance(ai_message, AIMessage):
        return ai_message.content
    else:
        print('error parsing results')
        return chunk


def list_available_models():
    load_dotenv()
    os.environ["NVIDIA_API_KEY"] = os.getenv("NVIDIA_API_KEY")
    # Fetch the list of available models
    available_models = ChatNVIDIA.get_available_models()

    # Print the ID and type for each model
    for model in available_models:
        if model.model_type == 'chat':
            print(f"ID: {model.id}, Type: {model.model_type}")
