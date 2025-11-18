from llm import create_llm, create_agent_llm
from langchain_core.messages import AIMessageChunk
import json






def test_llm():
    llm=create_llm()
    # A simple prompt to test the LLM
    prompt = "Tell me a short joke about programming."
    result = llm.invoke(prompt)
    print("Prompt:")
    print(prompt)
    print("LLM Response:")
    print(result.content)


def test_agent_invoke():
    print("\n--- Testing Agent with invoke() ---")
    system_prompt="You are a helpful assistant that manages Google Calendar events. If no mention of calender event answer the question to the best of your ability."
    agent=create_agent_llm(system_prompt)
    
    inputs = {"messages": [{"role": "user", "content": "what's 1+2?"}]}
    for chunk in agent.stream(inputs, stream_mode="updates"):
        print(chunk)
    # The invoke method runs the agent and returns the final result directly.
    result = agent.invoke(inputs)
    
    latest_message = chunk["messages"][-1]
    if latest_message.content:
        cleaned_answer=latest_message.content
    else:
        cleaned_answer='error getting the value'    
    print(f"Input: {inputs['messages'][-1]['content']}")
    print(f"Cleaned Answer: {cleaned_answer}")



def test_agent_stream():
    print("\n--- Testing Agent with stream() ---")
    system_prompt="You are a helpful assistant that manages Google Calendar events. If no mention of calender event answer the question to the best of your ability."
    agent=create_agent_llm(system_prompt)
    
    inputs = {"messages": [{"role": "user", "content": "what's 1+2?"}]}
    final_answer = ""
    print(f"Input: {inputs['messages'][-1]['content']}")
    print("Streaming Response: ", end="", flush=True)
    for chunk in agent.stream(inputs):
        if "output" in chunk:
            final_answer += chunk["output"]
            print(chunk["output"], end="", flush=True)
    print("\n-------------------------")

test_agent_invoke()
#test_agent_stream()