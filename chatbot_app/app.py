# app5.py
from llm_interface import get_llm_response
from tool_handler import process_tool_call, tools
from config import SYSTEM_PROMPT
from conversation_manager import ConversationManager
from response_formatter import extract_reply

def simple_chat():
    conversation = ConversationManager()
    
    print("Welcome to TechNova Customer Support! How can I assist you today?")
    while True:
        user_message = input("\nUser: ")
        if user_message.lower() in ['exit', 'quit', 'bye']:
            print("Thank you for using TechNova Customer Support. Goodbye!")
            break

        conversation.add_message("user", user_message)
        
        while True:
            response = get_llm_response(conversation.get_messages(), SYSTEM_PROMPT, tools)
            
            if response.stop_reason == "tool_use":
                tool_use = response.content[-1]
                tool_name = tool_use.name
                tool_input = tool_use.input
                print(f"======Claude wants to use the {tool_name} tool======")

                tool_result = process_tool_call(tool_name, tool_input)
                conversation.add_message("assistant", response.content)
                conversation.add_tool_result(tool_use.id, tool_result)
            else:
                reply = response.content[0].text
                extracted_reply = extract_reply(reply)
                print("\nTechNova Support: " + extracted_reply)
                conversation.add_message("assistant", reply)
                break

if __name__ == "__main__":
    simple_chat()