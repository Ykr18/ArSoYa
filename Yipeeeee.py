#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pip install groq
#pip install elevenlabs
#pip install python-dotenv


# In[13]:


from groq import Groq
import os
from dotenv import load_dotenv
from io import BytesIO
import requests
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import streamlit as st
import speech_recognition as sr



# In[1]:


client = Groq(
    api_key="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",
)


# In[ ]:


base_prompt="CONTEXT: You are a therapist who has 20+ years of experience in all kinds of therapy for example Cognitive behavioral therapy, Dialectical Behavior Therapy, Addiction therapy, grief counselling, child and youth therapy and family therapy. You are great at initiating conversations and making people feel comfortable. You are also great at storytelling, and use this in your therapy ONLY WHEN NECESSARY. You should also give them space to answer in between if they interrupt you. OUTPUT: The output will be fed to eleven labs for text to speech, avoid special characters BUT INCLUDE THEM IF THEY CHANGE THE MEANING OF THE SENTENCE. Make it sound like you are answering to your patient."


# In[23]:


completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "user",
        "content":"Talk in french. How are you"
        #"content": "Act as a therapist who has a lot of experience dealing with trauma. I am sufferring from addictions and if i stop drinking i feel sad. summarize in 100 words or less and make it sound like you are answering to your patient"
      }
    ],
    temperature=0.8,
    max_completion_tokens=1500,
    top_p=0.95,
    reasoning_effort="high",
    stream=True,
    stop=None
)
textllm = ""
for chunk in completion:
    content = chunk.choices[0].delta.content or ""
    print(content, end="")
    textllm += content


# In[27]:


# Import the play function here

load_dotenv()

elevenlabs = ElevenLabs(
 api_key='sk_0d6dc1870a89c44687c0b4f7734bb11017508f03241e8f18',
)

# audio_url = (
#     "https://storage.googleapis.com/eleven-public-cdn/audio/marketing/nicole.mp3"
# )
# response = requests.get(audio_url)
# audio_data = BytesIO(response.content)

# transcription = elevenlabs.speech_to_text.convert(
#     file=audio_data,
#     model_id="scribe_v1", # Model to use, for now only "scribe_v1" is supported
#     tag_audio_events=True, # Tag audio events like laughter, applause, etc.
#     language_code="eng", # Language of the audio file. If set to None, the model will detect the language automatically.
#     diarize=True, # Whether to annotate who is speaking
# )

# print(transcription)


# In[29]:


audio = elevenlabs.text_to_speech.convert(
    text=textllm,
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)
#play(audio)


# In[31]:


audio


# In[35]:


with open("output.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)


# In[8]:


#pip install SpeechRecognition


# In[11]:


#%pip install streamlit


# In[1]:


#%pip install pyaudio


# In[15]:


st.set_page_config(page_title="Voice Bot", layout="centered")

# Initialize session state
if "recording" not in st.session_state:
    st.session_state.recording = False

# Blob animation
st.markdown("""
<style>
.blob {
    margin: auto;
    width: 120px;
    height: 120px;
    background: #4CAF50;
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { transform: scale(1); opacity: 0.7; }
    50% { transform: scale(1.2); opacity: 1; }
    100% { transform: scale(1); opacity: 0.7; }
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="blob"></div>', unsafe_allow_html=True)
st.title("🎙️ Voice Bot")

# Toggle button
if st.button("🎤 Start/Stop Recording"):
    st.session_state.recording = not st.session_state.recording

# Recording logic
if st.session_state.recording:
    st.info("Recording... Speak now!")

    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        st.success("Recording stopped!")

    # Save audio
    filename = "input.wav"
    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())
    st.audio(filename)

    # You can now send `input.wav` to Eleven Labs STT
    st.session_state.recording = False  # Reset toggle


# In[ ]:




