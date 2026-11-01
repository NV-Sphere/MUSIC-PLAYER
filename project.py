# ============================================================
#  CALM VIBES MUSIC PLAYER (2-in-1: Tkinter GUI + Streamlit Web)
#  Made by: [Her Name]  |  Python + DSA Mini Project
# ============================================================

import os

# Safe Imports: Taaki laptop aur cloud server dono par bina error ke chale
try:
    import tkinter as tk
    from pygame import mixer
except Exception:
    tk = None
    mixer = None

try:
    import streamlit as st
except Exception:
    st = None


# ============================================================
# TASK 1: COMMON SONG DATABASE (Lists, Tuples & Sets - Day 9, 11, 12)
# ============================================================
# Har gaana ek Tuple hai: (file_name, is_favourite)
my_playlist = [
    ("MUSIC_1.mp3", False),
    ("Music_2.mp3", False),
    ("Music_3.mp3", True),    # <-- Uska FAVOURITE gaana / khud ki recording
    ("Music_4.mp3", False),
]

# Set: Already-played gaano ko track karega (duplicates automatically hat jayenge)
played_songs = set()


# ============================================================
# TASK 2: COMMON HELPER FUNCTION (Strings & Functions - Day 5, 6)
# ============================================================
def clean_name(file_name):
    # String methods: ".mp3" hatao, "_" ko space se badlo, pehla letter capital karo
    name = file_name.replace(".mp3", "")
    name = name.replace("_", " ")
    return name.title()


# ============================================================
# TASK 3: TKINTER DESKTOP PLAYER (Syllabus GUI Topic)
# ============================================================
def run_tkinter_desktop_app():
    audio_ready = True
    try:
        mixer.init()
    except Exception:
        audio_ready = False

    def update_status(message, color="#4B0082"):
        status_label.config(text=message, fg=color)

    def play_music():
        if not audio_ready:
            update_status("Is computer ka audio ready nahi hai.")
            return

        index = playlist_box.curselection()
        if not index:
            update_status("Pehle ek gaana select karo!")
            return

        file_name, is_favourite = my_playlist[index[0]]

        if not os.path.exists(file_name):
            update_status(file_name + " folder mein nahi mili!")
            return

        mixer.music.load(file_name)
        mixer.music.play()

        already_played = file_name in played_songs
        played_songs.add(file_name)

        if is_favourite:
            update_status("Playing your FAVOURITE: " + clean_name(file_name) + " 💜", color="#B8005C")
        elif already_played:
            update_status("Playing again: " + clean_name(file_name))
        else:
            update_status("Playing: " + clean_name(file_name))

    def pause_music():
        if audio_ready:
            mixer.music.pause()
        update_status("Paused.")

    def resume_music():
        if audio_ready:
            mixer.music.unpause()
        update_status("Resumed.")

    def stop_music():
        if audio_ready:
            mixer.music.stop()
        update_status("Stopped.")

    def show_history():
        if len(played_songs) == 0:
            update_status("Abhi tak koi gaana play nahi hua.")
        else:
            names = [clean_name(s) for s in played_songs]  # List Comprehension
            update_status("Played so far: " + ", ".join(names))

    # --- Tkinter Window & Theme Setup ---
    window = tk.Tk()
    window.title("Calm Vibes Music Player")
    window.geometry("380x480")
    window.configure(bg="#E6E6FA")  # Calm Lavender/Purple

    title_label = tk.Label(window, text="My Calm Vibes Playlist",
                           bg="#E6E6FA", fg="#4B0082",
                           font=("Helvetica", 16, "bold"))
    title_label.pack(pady=15)

    # --- Playlist Box (For Loop) ---
    playlist_box = tk.Listbox(window, bg="#FFD6EC", fg="#333333",
                              font=("Helvetica", 12), width=32, height=8,
                              selectbackground="#ADD8E6")
    playlist_box.pack(pady=10)

    for song_file, favourite in my_playlist:
        display_name = clean_name(song_file)
        if favourite:
            display_name = "⭐ " + display_name
        playlist_box.insert(tk.END, display_name)

    for i in range(len(my_playlist)):
        if my_playlist[i][1] is True:
            playlist_box.itemconfig(i, fg="#B8005C")

    # --- Status Label ---
    status_label = tk.Label(window, text="Select a song and press Play.",
                            bg="#E6E6FA", fg="#4B0082",
                            font=("Helvetica", 10), wraplength=320)
    status_label.pack(pady=10)

    # --- Control Buttons ---
    button_frame = tk.Frame(window, bg="#E6E6FA")
    button_frame.pack(pady=15)

    tk.Button(button_frame, text="Play", command=play_music,
              bg="#ADD8E6", font=("Arial", 10, "bold"), width=7).grid(row=0, column=0, padx=4, pady=4)
    tk.Button(button_frame, text="Pause", command=pause_music,
              bg="#FFB6C1", font=("Arial", 10, "bold"), width=7).grid(row=0, column=1, padx=4, pady=4)
    tk.Button(button_frame, text="Resume", command=resume_music,
              bg="#ADD8E6", font=("Arial", 10, "bold"), width=7).grid(row=1, column=0, padx=4, pady=4)
    tk.Button(button_frame, text="Stop", command=stop_music,
              bg="#FFB6C1", font=("Arial", 10, "bold"), width=7).grid(row=1, column=1, padx=4, pady=4)

    tk.Button(window, text="Show Play History", command=show_history,
              bg="#C9A0FF", font=("Arial", 10, "bold"), width=20).pack(pady=10)

    footer = tk.Label(window, text="Made with Python by [Her Name]",
                      bg="#E6E6FA", fg="#8A2BE2", font=("Helvetica", 9, "italic"))
    footer.pack(side="bottom", pady=10)

    window.mainloop()


# ============================================================
# TASK 4: STREAMLIT WEB PLAYER (Live Mobile Domain Mode)
# ============================================================
def run_streamlit_web_app():
    st.set_page_config(page_title="My Calm Vibes Playlist", page_icon="💜")

    st.title("🎶 My Calm Vibes Playlist 💜")
    st.write("Built with pure Python (Tkinter + Streamlit) by [Her Name]")
    st.markdown("---")

    # Dropdown list taiyar karna (For Loop + Conditionals)
    display_options = []
    for song_file, favourite in my_playlist:
        label = clean_name(song_file)
        if favourite:
            label = "⭐ " + label + " (Favourite 💜)"
        display_options.append(label)

    # Song select karne ka box
    selected_index = st.selectbox(
        "Select a song to play:",
        range(len(display_options)),
        format_func=lambda i: display_options[i]
    )

    selected_file, is_fav = my_playlist[selected_index]

    # Audio Player chalana
    if os.path.exists(selected_file):
        if is_fav:
            st.success(f"Playing your FAVOURITE: **{clean_name(selected_file)}** 💜")
        else:
            st.info(f"Now Playing: **{clean_name(selected_file)}**")

        with open(selected_file, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")
    else:
        st.error(f"Song file '{selected_file}' folder mein nahi mili! Please GitHub par upload karein.")

    st.markdown("---")
    st.caption("Made with Python, Tkinter & Streamlit 💜")


# ============================================================
# TASK 5: THE SMART SWITCH (Auto-Detects Laptop vs Web Domain)
# ============================================================
def is_running_on_streamlit():
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        return get_script_run_ctx() is not None
    except Exception:
        return False

if is_running_on_streamlit():
    # Jab Streamlit Cloud (Domain) par chalega, toh Web Player khulega:
    run_streamlit_web_app()
else:
    # Jab VS Code / PyCharm mein Run ▶️ dabayenge, toh Tkinter GUI khulega:
    run_tkinter_desktop_app()
