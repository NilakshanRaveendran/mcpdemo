"""
Simplasyncio.runple using MCPAGENT with built-in conversation memory.
This example demonstrates how to set up a chat MCPAgent that maintains context across multiple interactions.

Special thanks to, "https://github.com/microsoft/playwright-mcp"
"""

import asyncio

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient

import os

async def run_memory_chat():
    """Run a chat session with conversation memory using MCPAgent."""
    load_dotenv()  # Load environment variables from .env file
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    # Specify the configuration file for the MCP client
    config_file = "browser_mcp.json"

    print("Starting chat with memory...")

    #create MCP client and agent with memory
    client = MCPClient.from_config_file(config_file)
    llm = ChatGroq(model="llama-3.1-8b-instant")

    #create MCPAgent with conversation memory enabled
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True
    )

    print("\n=============Interactive MCP Agent Chat with Memory=============\n")
    print("You can start chatting with the agent now. Type 'exit' to quit.\n")
    print("Type 'clear' to clear the conversation memory.\n")
    print("===============================================================\n")


    try:
        while True:
            # Get user input
            user_input = input("\nYou: ")


            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting chat. Goodbye!")
                break

            #check for clear memory command
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation memory cleared.")
                continue

            print("\nAssistant: ", end="", flush=True)

            try:
                # Get agent response
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"Error: {e}")

    finally:
        # Ensure the client is properly closed
        

        if client and client.sessions:
            await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(run_memory_chat())