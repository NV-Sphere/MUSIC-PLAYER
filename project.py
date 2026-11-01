import streamlit as st
import os

# 1. UI aur Theme (Streamlit automatically phone ke hisaab se set kar leta hai)
st.title("🎶 My Calm Vibes Playlist 💜")
st.write("Built with pure Python by [Her Name]")
st.markdown("---")

# 2. Playlist Database (Lists)
my_playlist = ["Music_4.mp3", "MUSIC_1.mp3", "Music_2.mp3", "Music_3.mp3"]  # <-- Yeh uska FAVOURITE gaana hai (True)

# 3. Dropdown Menu (Gaana select karne ke liye)
selected_song = st.selectbox("Select a song to play:", my_playlist)

# 4. The Audio Player (Inbuilt in Streamlit)
if os.path.exists(selected_song):
    audio_file = open(selected_song, 'rb')
    audio_bytes = audio_file.read()
    
    st.write(f"Now Playing: **{selected_song}**")
    st.audio(audio_bytes, format='audio/mp3') # Yeh phone par proper play/pause button dega!
else:
    st.error("Song file not found! Please upload it.")