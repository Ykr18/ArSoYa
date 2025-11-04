#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import sounddevice as sd
import numpy as np
import scipy.io.wavfile
import ffmpeg
import os

# Page config
st.set_page_config(page_title="ArSoYa Therapy Bot", layout="centered")

# Initialize session state
if "is_recording" not in st.session_state:
    st.session_state.is_recording = False

# Title and header
st.markdown("<h1 style='text-align: center;'>🌟 ArSoYa Therapy Bot</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-bottom: 60px;'>Welcome to your interactive therapy space</h3>", unsafe_allow_html=True)

# Irregular animated blob using CSS
blob_html = """
<style>
.irregular-blob {
  width: 220px;
  height: 220px;
  background: #00f0ff;
  border-radius: 60% 40% 55% 45% / 50% 60% 40% 50%;
  animation: morph 4s infinite ease-in-out;
  margin: auto;
  box-shadow: 0 0 30px #00f0ff;
}
@keyframes morph {
  0% { border-radius: 60% 40% 55% 45% / 50% 60% 40% 50%; }
  50% { border-radius: 50% 60% 40% 60% / 60% 40% 60% 40%; }
  100% { border-radius: 60% 40% 55% 45% / 50% 60% 40% 50%; }
}
</style>
<div class="irregular-blob"></div>
"""
st.markdown(blob_html, unsafe_allow_html=True)

# Recording logic
duration = 5
sample_rate = 44100
channels = 1
wav_file = "temp.wav"
mp3_file = "output.mp3"
ffmpeg_path = r"C:\Users\Yatharth\Desktop\Sem 3\DATA 606\ffmpeg-8.0-essentials_build\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe"

# UI feedback
if st.session_state.is_recording:
    st.markdown("<p style='text-align: center; color: red; font-size: 18px;'>🔴 Recording in progress...</p>", unsafe_allow_html=True)

# Toggle button
if st.button("🎙️ Start/Stop Recording"):
    if not st.session_state.is_recording:
        st.session_state.is_recording = True
        with st.spinner("Recording..."):
            audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='int16')
            sd.wait()
            scipy.io.wavfile.write(wav_file, sample_rate, audio)
            ffmpeg.input(wav_file).output(mp3_file, format='mp3').run(cmd=ffmpeg_path)
        st.success(f"Recording complete. Saved as {mp3_file}")
        st.session_state.is_recording = False
    else:
        st.session_state.is_recording = False

