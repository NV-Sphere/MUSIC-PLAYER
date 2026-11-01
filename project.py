# ============================================================
#  CALM VIBES MUSIC PLAYER (Tkinter Desktop + Streamlit Web)
#  Made by: [Her Name]  |  6-Task Python Mini Project
# ============================================================
import os, shutil

# ---------- TASK 1: SAFE IMPORTS (Crash-Proof Setup) ----------
try:
    import tkinter as tk
    from tkinter import filedialog, simpledialog
    from pygame import mixer
except Exception:
    tk = None
try:
    import streamlit as st
except Exception:
    st = None

# ---------- TASK 2: SHARED SONG LOGIC (Lists & Strings) ----------
FAV = "my_voice.mp3"  # Uski khud ki recording ya sabse favourite gaana

def get_playlist():
    # Folder mein jitni bhi .mp3 files hain, unki sorted List banao
    return sorted([f for f in os.listdir() if f.endswith(".mp3")])

def clean(file_name):
    # String Methods: ".mp3" aur "_" hata kar sundar naam banao
    return file_name.replace(".mp3", "").replace("_", " ").title()

# ---------- TASK 3: CALM DARK THEME (Same colors for Both Apps) ----------
BG, CARD, TEXT = "#1E1B2E", "#2B2640", "#F3E8FF"
PINK, BLUE, PURPLE = "#FF8FD6", "#8FD9FF", "#C9A0FF"

# ---------- TASK 4: TKINTER DESKTOP APP (Syllabus GUI + Upload) ----------
def run_tkinter_app():
    try: mixer.init()
    except Exception: pass

    window = tk.Tk()
    window.title("Calm Vibes Music Player")
    window.geometry("360x480")
    window.configure(bg=BG)

    tk.Label(window, text="🎶 My Calm Vibes Playlist 💜", bg=BG, fg=PURPLE, font=("Helvetica", 15, "bold")).pack(pady=12)
    box = tk.Listbox(window, bg=CARD, fg=TEXT, font=("Helvetica", 12), selectbackground=BLUE, width=30, height=8, bd=0)
    box.pack(pady=8)
    status = tk.Label(window, text="Select a song and press Play", bg=BG, fg=TEXT, font=("Helvetica", 10))
    status.pack(pady=6)

    def refresh():
        # For Loop se saare gaane screen ke box mein daalo
        box.delete(0, tk.END)
        for s in get_playlist():
            box.insert(tk.END, ("⭐ " if s == FAV else "🎵 ") + clean(s))

    def play():
        if not box.curselection():
            return status.config(text="Pehle ek gaana select karo!", fg=PINK)
        song = get_playlist()[box.curselection()[0]]
        try:
            mixer.music.load(song)
            mixer.music.play()
            status.config(text="Playing: " + clean(song) + " 💜", fg=PINK if song == FAV else BLUE)
        except Exception:
            status.config(text="Audio driver issue ya corrupt file!", fg=PINK)

    def add_song():
        # Laptop se naya MP3 select karke naye naam se project mein save karo
        path = filedialog.askopenfilename(title="Select MP3", filetypes=[("MP3 Files", "*.mp3")])
        name = simpledialog.askstring("Song Name", "Is gaane ka kya naam rakhna hai?") if path else None
        if path and name:
            new_file = name.strip().replace(" ", "_").lower() + ".mp3"
            shutil.copy(path, new_file)
            refresh()
            status.config(text="Added: " + clean(new_file) + " ✨", fg=PINK)

    refresh()
    row = tk.Frame(window, bg=BG)
    row.pack(pady=8)
    tk.Button(row, text="▶ Play", command=play, bg=BLUE, width=6, font=("Arial", 10, "bold")).grid(row=0, column=0, padx=3)
    tk.Button(row, text="⏸ Pause", command=lambda: mixer.get_init() and mixer.music.pause(), bg=PINK, width=6, font=("Arial", 10, "bold")).grid(row=0, column=1, padx=3)
    tk.Button(row, text="⏯ Resume", command=lambda: mixer.get_init() and mixer.music.unpause(), bg=BLUE, width=7, font=("Arial", 10, "bold")).grid(row=0, column=2, padx=3)
    tk.Button(row, text="⏹ Stop", command=lambda: mixer.get_init() and mixer.music.stop(), bg=PURPLE, width=6, font=("Arial", 10, "bold")).grid(row=0, column=3, padx=3)

    tk.Button(window, text="➕ Add & Save New Song", command=add_song, bg=PINK, width=25, font=("Arial", 10, "bold")).pack(pady=8)
    tk.Label(window, text="Made with Python by [Her Name]", bg=BG, fg=PURPLE, font=("Helvetica", 9, "italic")).pack(side="bottom", pady=8)
    window.mainloop()

# ---------- TASK 5: STREAMLIT WEB APP (Live Domain + Upload) ----------
def run_streamlit_app():
    st.set_page_config(page_title="Calm Vibes Playlist", page_icon="💜")
    st.markdown(f"<style>.stApp{{background:{BG};color:{TEXT};}} h1,h2,h3,p,label{{color:{PURPLE}!important;}}</style>", unsafe_allow_html=True)
    st.title("🎶 My Calm Vibes Playlist 💜")
    st.caption("Built with Pure Python (Tkinter + Streamlit) by [Her Name]")

    playlist = get_playlist()
    if playlist:
        labels = [("⭐ " if s == FAV else "🎵 ") + clean(s) for s in playlist]
        idx = st.selectbox("Select a song to play:", range(len(playlist)), format_func=lambda i: labels[i])
        st.success("Now Playing: " + labels[idx])
        with open(playlist[idx], "rb") as f:
            st.audio(f.read(), format="audio/mp3")
    else:
        st.warning("Abhi koi gaana nahi hai. Niche se apna pehla gaana add karo!")

    st.markdown("---")
    st.subheader("➕ Add & Save New Song")
    up_file = st.file_uploader("Choose an MP3 song or voice recording:", type=["mp3"])
    up_name = st.text_input("Give this song a name (e.g., My Favourite Song):")
    if st.button("💾 Save Song to Playlist") and up_file and up_name.strip():
        new_file = up_name.strip().replace(" ", "_").lower() + ".mp3"
        with open(new_file, "wb") as f:
            f.write(up_file.getbuffer())
        st.success(clean(new_file) + " playlist mein jud gaya! 💜")
        st.rerun()

# ---------- TASK 6: AUTO-SWITCH (Laptop -> Tkinter, Web -> Streamlit) ----------
if st and st.runtime.exists():
    run_streamlit_app()
else:
    run_tkinter_app()
