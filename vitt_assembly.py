import os
import builtins
from instagrapi import Client
from moviepy.editor import ColorClip

def print(*args, **kwargs):
    kwargs['flush'] = True
    builtins.print(*args, **kwargs)

IG_USERNAME = os.environ.get("IG_USERNAME")
IG_PASSWORD = os.environ.get("IG_PASSWORD")

def create_dummy_video():
    print("Creating ZERO-COST dummy video for Meta testing...")
    clip = ColorClip(size=(720, 1280), color=(0, 0, 0), duration=3)
    clip.write_videofile("dummy.mp4", fps=24, codec="libx264")
    return "dummy.mp4"

def publish(video, caption):
    print("Attempting to breach Meta Security Gates...")
    cl = Client()
    cl.request_timeout = 60
    session_file = "ig_session.json"
    
    if os.path.exists(session_file):
        cl.load_settings(session_file)
    
    cl.login(IG_USERNAME, IG_PASSWORD)
    
    if not os.path.exists(session_file):
        cl.dump_settings(session_file)
        
    cl.clip_upload(video, caption)
    print("Meta Breach Successful! Video Uploaded!")

if __name__ == "__main__":
    try:
        print("Initiating Zero-Burn Strategy...")
        v = create_dummy_video()
        publish(v, "Testing Meta Security Gateway bypass. #TheVittWire")
    except Exception as e:
        print(f"System Offline Error: {e}")
