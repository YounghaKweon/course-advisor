import google.generativeai as genai
from google.generativeai.protos import Part # This import is correct
import json
import os
from dotenv import load_dotenv
from course_tools import find_sections_by_department, find_sections_by_level, find_sections_by_time

# --- 1. Setup Environment ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY not found in .env file.")
    exit()

genai.configure(api_key=api_key)
MODEL = "gemini-2.5-flash"

# --- 2. Define Tools and System Prompt ---
available_tools = {
    "find_sections_by_department": find_sections_by_department,
    "find_sections_by_level": find_sections_by_level,
    "find_sections_by_time": find_sections_by_time,
}

SYSTEM_PROMPT = "You are a helpful and friendly course advisor for Calvin University. Use the available tools to search the course catalog. Ask clarifying questions if the request is vague."

# --- 3. Main Conversation Loop ---
try:
    model = genai.GenerativeModel(model_name=MODEL, system_instruction=SYSTEM_PROMPT, tools=available_tools.values())
    chat = model.start_chat()
except Exception as e:
    print(f"❌ Error initializing Gemini model: {e}")
    exit()


print("🤖 Course Advisor Bot (Gemini) is ready. Type 'exit' to end.")
log_file = "conversations_gemini.jsonl"

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Advisor: Goodbye! 👋")
        break
    
    try:
        response = chat.send_message(user_input)
        
        # Check if the model decided to call a function
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            function_name = function_call.name
            function_args = {key: value for key, value in function_call.args.items()}
            
            print(f"🤖 Calling tool: {function_name}({', '.join(f'{k}={v}' for k, v in function_args.items())})")
            
            # Call the actual Python function
            function_to_call = available_tools[function_name]
            function_response = function_to_call(**function_args)
            
            # Send the tool's output back to the model
            response = chat.send_message(
                Part(function_response={
                    "name": function_name,
                    "response": {
                        "result": function_response
                    }
                })
            )
            
            final_message = response.text
            log_entry = {"user_input": user_input, "agent_response": final_message, "tool_calls": [function_name]}
        else:
            # If no tool was called, the response is the final message
            final_message = response.text
            log_entry = {"user_input": user_input, "agent_response": final_message, "tool_calls": []}

        print(f"Advisor: {final_message}")
        
        # Write the interaction to the log file
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
            
    except Exception as e:
        print(f"An error occurred: {e}")