#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pip install groq
#pip install elevenlabs
#pip install python-dotenv


# In[33]:


from groq import Groq
import os
from dotenv import load_dotenv
from io import BytesIO
import requests
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import speech_recognition as sr


# ### LLM CODE

# In[25]:


client = Groq(
    api_key="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",
)


# In[15]:


base_prompt="CONTEXT: You are a therapist who has 20+ years of experience in all kinds of therapy for example Cognitive behavioral therapy, Dialectical Behavior Therapy, Addiction therapy, grief counselling, child and youth therapy and family therapy. You are great at initiating conversations and making people feel comfortable. You are also great at storytelling, and use this in your therapy ONLY WHEN NECESSARY. You should also give them space to answer in between if they interrupt you. OUTPUT: The output will be fed to eleven labs for text to speech, avoid special characters BUT INCLUDE THEM IF THEY CHANGE THE MEANING OF THE SENTENCE. Make it sound like you are answering to your patient."


# In[27]:


completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "user",
        "content":full_prompt
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


# ### Speech to text Code

# In[9]:


# Import the play function here

load_dotenv()

elevenlabs = ElevenLabs(
 api_key='sk_0d6dc1870a89c44687c0b4f7734bb11017508f03241e8f18',
)

local_audio_path = "yatharth.mp3"

with open(local_audio_path, "rb") as f:
   audio_data = BytesIO(f.read())

transcription = elevenlabs.speech_to_text.convert(
   file=audio_data,
   model_id="scribe_v1",
   tag_audio_events=True,
   language_code="eng",
   diarize=True,
)

print(transcription.text)


# In[19]:


textuser=transcription.text


# In[21]:


full_prompt=base_prompt+" User prompt is:"+textuser


# ### Text to Speech Code

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


# In[31]:


with open("output.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)

