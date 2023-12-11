import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import openai
import inspect
import pytz
from datetime import datetime

st.set_page_config(layout="wide")

with open('config.json') as f:
    config = json.load(f)

aoai_endpoint = config['AOAIEndpoint']
aoai_api_key = config['AOAIKey']
deployment_name = config['AOAIDeploymentName']

### Exercise 02: Chat with customer data
def create_chat_completion(deployment_name, messages, endpoint, key, index_name):
    # Create an Azure OpenAI client. We create it in here because each exercise will
    # require at a minimum different base URLs.

    #client = openai.AzureOpenAI(
    #    base_url=f"{aoai_endpoint}/openai/deployments/{deployment_name}/extensions/",
    #    TODO: fill in rest of parameters
    #)
    
    # Create and return a new chat completion request
    # Be sure to include the "extra_body" parameter to use Azure AI Search as the data source

    #return client.chat.completions.create(
    #    model=deployment_name,
    #    messages=[
    #        {"role": m["role"], "content": m["content"]}
    #        for m in messages
    #    ],
    #    stream=True,
    #    TODO: fill in rest of function call
    #)
    
    raise NotImplementedError

def handle_chat_prompt(prompt):
    # Echo the user's prompt to the chat window
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send the user's prompt to Azure OpenAI and display the response
    # The call to Azure OpenAI is handled in create_chat_completion()
    # This function loops through the responses and displays them as they come in.
    # It also appends the full response to the chat history.

    #with st.chat_message("assistant"):
    #    message_placeholder = st.empty()
    #    full_response = ""
    #    for response in ... TODO: finish call
    #st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    raise NotImplementedError

### Exercise 03: Function calls
def get_customers(search_criterion, search_value):
    # Set up the API request
    full_server_url = f"TODO: fill this in"
    r = requests.get(
        full_server_url,
        headers={"Content-Type": "application/json"}
    )
    if r.status_code == 200:
        return st.write(pd.read_json(r.content.decode("utf-8")))
    else:
        return f"Failure to find any customers with {search_criterion} {search_value}."

functions = [
    {
        "name": "get_customers",
        "description": "Get a list of customers based on some search criterion.",
        "parameters": {
            "type": "object",
            "properties": {
                "search_criterion": {"type": "string", "enum": ["CustomerName", "LoyaltyTier", "DateOfMostRecentStay"]},
                "search_value": {"type": "string"},
            },
            "required": ["search_criterion", "search_value"],
        },
    }
]

available_functions = {
    "get_customers": get_customers,
}

def create_chat_completion_with_functions(deployment_name, messages):
    # Create an Azure OpenAI client. We create it in here because each exercise will
    # require at a minimum different base URLs.
    
    #client = openai.AzureOpenAI(
    #    base_url=f"{aoai_endpoint}/openai/deployments/{deployment_name}/",
    #    TODO: fill in rest of parameters
    #)
    
    # Create and return a new chat completion request
    # Be sure to include the "functions" parameter and set "function_call"

    #return client.chat.completions.create(
    #    model=deployment_name,
    #    messages=[
    #        {"role": m["role"], "content": m["content"]}
    #        for m in messages
    #    ],
    #    TODO: fill in rest of function call
    #)
    
    raise NotImplementedError

def handle_chat_prompt_with_functions(prompt):
    # Echo the user's prompt to the chat window
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send the user's prompt to Azure OpenAI and display the response
    # The call to Azure OpenAI is handled in create_chat_completion()
    # This function loops through the responses and displays them as they come in.
    # It also appends the full response to the chat history.

    #with st.chat_message("assistant"):
    #    message_placeholder = st.empty()
    #    full_response = ""
    #    response = TODO: finish call and extract message as response_message
    #
    #    # Check if GPT returned a function call
    #    if response_message.function_call:
    #        # Get the function name and arguments
    #        
    #        # Verify the function
    #        if function_name not in available_functions:
    #            full_response = f"Sorry, I don't know how to call the function `{function_name}`."
    #        else:
    #            function_to_call = available_functions[function_name]
    #            # Verify the function has the correct number of arguments
    #            function_args = json.loads(response_message.function_call.arguments)
    #            if check_args(function_to_call, function_args) is False:
    #                full_response = f"Sorry, I don't know how to call the function `{function_name}` with those arguments."
    #            else:
    #                # Call the function
    #                full_response = function_to_call(**function_args)
    #message_placeholder.markdown(full_response)
    #st.session_state.messages.append({"role": "assistant", "content": full_response})

    raise NotImplementedError

# helper method used to check if the correct arguments are provided to a function
def check_args(function, args):
    sig = inspect.signature(function)
    params = sig.parameters

    # Check if there are extra arguments
    for name in args:
        if name not in params:
            return False
    # Check if the required arguments are provided 
    for name, param in params.items():
        if param.default is param.empty and name not in args:
            return False

    return True


### All Exercises
def generate_chat(chat_option):
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Await a user message and handle the chat prompt when it comes in.
    if prompt := st.chat_input("Enter a message:"):
        if chat_option == "Chat with Data":
            handle_chat_prompt(prompt)
        elif chat_option == "Function Calls":
            handle_chat_prompt_with_functions(prompt)
        else:
            st.write("Please select a tab before calling the chatbot.")

def main():
    st.write(
    """
    # Contoso Suites Example Page

    This Streamlit dashboard is intended to serve as a proof of concept of Azure OpenAI functionality for Contoso Suites employees.  It is not intended to be a production-ready application.
    """
    )

    chat_option = st.radio(label="Choose the chat option you want to try:", options=["Chat with Data", "Function Calls"])

    generate_chat(chat_option)

if __name__ == "__main__":
    main()
