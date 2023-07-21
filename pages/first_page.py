import streamlit as st
import assemblyai as aai

from clarifai.auth.helper import ClarifaiAuthHelper
from clarifai.client import create_stub
from clarifai_utils.modules.css import ClarifaiStreamlitCSS
from clarifai.listing.lister import ClarifaiResourceLister
from clarifai.modules.css import ClarifaiStreamlitCSS

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)

# This must be within the display() function.
auth = ClarifaiAuthHelper.from_streamlit(st)
stub = create_stub(auth)
userDataObject = auth.get_user_app_id_proto()
lister = ClarifaiResourceLister(stub, auth.user_id, auth.app_id, page_size=16)

st.title("🎙️ Audio Transcription using the Conformer-2 Model from Assemblyai")

st.sidebar.markdown("Made with UI Modules, a streamlit integration from [Clarifai](https://clarifai.com/) that helps you create and deploy beautiful AI web apps.")
st.sidebar.image("https://clarifai.com/favicon.svg", width=100)


# set the API key
with st.sidebar:
    api_key = st.text_input("AssemblyAI API Key", type="password")
    aai.settings.api_key = f"{api_key}"

def transcribe(audio):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio, config=aai.TranscriptionConfig(summarization=True))
    st.info(transcript.text)


with st.form("my_form"):
    audio = st.text_area("Enter Audio File that you want to transcribe & summarize:", "https://example.org/audio.mp3")
    submitted = st.form_submit_button("Submit")
    if not api_key:
        st.info("Please add your AssemblyAI API key to continue.")
    elif submitted:
        transcribe(audio)
