import streamlit as st
import streamlit_extras.stateful_button as stx
from streamlit_js_eval import streamlit_js_eval
import requests
import pandas as pd
import json
import openai
import inspect
import time
from scipy.io import wavfile
import azure.cognitiveservices.speech as speechsdk

st.set_page_config(layout="wide")

with open('config_full.json') as f:
    config = json.load(f)

aoai_endpoint = config['AOAIEndpoint']
aoai_api_key = config['AOAIKey']
deployment_name = config['AOAIDeploymentName']
speech_key = config['SpeechKey']
speech_region = config['SpeechRegion']


### Exercise 05: Provide live audio transcription
def create_transcription_request(audio_file, speech_key, speech_region, speech_recognition_language="en-US"):
    # Create an instance of a speech config with specified subscription key and service region.
    # speech_config = ...
    # TODO: set speech recognition language

    # Prepare audio settings for the wave stream
    channels = 1
    bits_per_sample = 16
    samples_per_second = 16000

    # TODO: Create audio configuration using the push stream
    # wave_format = ...
    # stream = ...
    # audio_config = ...

    # TODO: use the ConversationTranscriber class to create a transcriber object
    # transcriber = ...

    all_results = []
    done = False

    # Callback events for transcribed and stopped/cancelled states
    def handle_final_result(evt):
        all_results.append(evt.result.text)

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done= True

    # Subscribe to the events fired by the conversation transcriber
    # TODO: add event handlers for transcribed, session_started, session_stopped, and canceled events

    # Begin the transcription process
    # transcriber.start_transcribing_async()

    # Read the whole wave files at once and stream it to sdk
    _, wav_data = wavfile.read(audio_file)
    # TODO: write the stream to bytes and close it when done
    while not done:
        time.sleep(.5)

    # transcriber.stop_transcribing_async()
    return all_results

def create_live_transcription_request(speech_key, speech_region, speech_recognition_language="en-US"):
    # Create an instance of a speech config with specified subscription key and service region.
    # speech_config = ...
    # TODO: set speech recognition language
    # TODO: use the ConversationTranscriber class to create a transcriber object
    # transcriber = ...

    all_results = []
    done = False

    # Callback events for transcribed and stopped/cancelled states
    def handle_final_result(evt):
        all_results.append(evt.result.text)
        print(evt.result.text)

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous transcription upon receiving an event `evt`"""
        print('CLOSING {}'.format(evt))
        nonlocal done
        done = True

    # Subscribe to the events fired by the conversation transcriber
    # TODO: add event handlers for transcribed, session_started, session_stopped, and canceled events

    # Begin the transcription process
    # transcriber.start_transcribing_async()

    # Streamlit refreshes the page on each interaction,
    # so a clean start and stop isn't really possible with button presses.
    # Instead, we're constantly updating transcription results, so that way,
    # when the user clicks the button to stop, we can just stop updating the results.
    # This might not capture the final message, however, if the user stops before
    # we receive the message--we won't be able to call the stop event.
    while not done:
        st.session_state.transcription_results = all_results
        time.sleep(1)

    return


def is_call_in_compliance():
    # Check whether a call meets compliance requirements
    # Call with a person includes recording message
    # Call is about an appropriate topic for a hotel and resort chain -- should not be off-topic
    raise NotImplementedError

def create_named_entity_extraction_request(endpoint, key, region, text):
    # Create a named entity extraction client
    #client = speechsdk.TextAnalyticsClient(
    #    endpoint=endpoint,
    #    credential=speechsdk.AzureKeyCredential(key)
    #)
    #return client.recognize_entities(documents=[text])
    raise NotImplementedError

def make_compliance_chat_request(system, call_contents):
    # Create an Azure OpenAI client.

    # Create and return a new chat completion request
    # There should be two messages, one from role=system with the system prompt,
    # and one from role=user with the call contents.
    raise NotImplementedError

def is_call_in_compliance(call_contents, include_recording_message, is_relevant_to_topic):
    # call_contents comes in as a list of strings, so join them together with spaces
    # If the user has checked the include_recording_message or is_relevant_to_topic boxes,
    # add the appropriate prompt:
        # "2. Was the caller aware that the call was being recorded?"
        # "3. Was the call relevant to the hotel and resort industry?"

    system = f"""
        You are an automated analysis system for Contoso Suites. Contoso Suites is a luxury hotel and resort chain with locations
        in a variety of Caribbean nations and territories.
        
        You are analyzing a call for relevance and compliance.

        You will only answer the following questions based on the call contents:
        1. Was there vulgarity on the call?
        TODO: finish this based on the prompts above!
    """

    # Call make_compliance_chat_request
    # Return the message content for the response's first choice
    raise NotImplementedError


### Exercise 06: Generate call summary


def main():
    st.write(
    """
    # Call Center

    This Streamlit dashboard is intended to replicate some of the functionality of a call center monitoring solution. It is not intended to be a production-ready application.
    """
    )

    st.write("## Simulate a call")

    # TODO: Add a file uploader to the Streamlit app
    # TODO: Add a conditional based on:
    #    - If there is an uploaded file
    #    - And either 'file_transcription' is not in st.session_state or st.session_state.file_transcription is False
    # If so:
        # TODO: Add an st.audio() element to the Streamlit app to play the audio back
        # TODO: Use st.spinner() to wrap the transcription
        # TODO: Call the create_transcription_request() function and save its results to session state as file_transcription_results
        # TODO: Set file_transcription to True in session state
        # TODO: If there is an uploaded file, call st.success() to indicate that the transcription is complete

    if 'file_transcription_results' in st.session_state:
        st.write(st.session_state.file_transcription_results)
        
    st.write("## Perform a Live Call")

    # TODO: Add a Streamlit Extras button called start_recording and whose label is Record.
    # Streamlit Extras buttons also need a key, which you can name something like "recording_in_progress".
    # TODO: If the button is clicked, create a spinner and then call create_live_transcription_request().

    if 'transcription_results' in st.session_state:
        st.write(st.session_state.transcription_results)

    st.write("""## Clear Messages between Calls
        Select this button to clear out session state and refresh the page.
        Do this before loading a new audio file or recording a new call.
        This will ensure that transcription and compliance checks will happen correctly.
    """)

    if st.button("Clear messages"):
        if 'file_transcription_results' in st.session_state:
            del st.session_state.file_transcription_results
        if 'transcription_results' in st.session_state:
            del st.session_state.transcription_results
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

    st.write("## Is Your Call in Compliance?")

    include_recording_message = st.checkbox("Call needs an indicator we are recording it")
    is_relevant_to_topic = st.checkbox("Call is relevant to the hotel and resort industry")

    # TODO: Add a Streamlit button to check for compliance. If the button is clicked:
       # TODO: Use st.spinner() to wrap the compliance check
       # TODO: Set call_contents to either file_transcription_results or transcription_results, depending on
       # which has content. If neither has content, write out an error message for the user.
       # TODO: Make a call to is_call_in_compliance and write out the results using st.write()
       # TODO: Call st.success() to indicate that the compliance check is complete

if __name__ == "__main__":
    main()
