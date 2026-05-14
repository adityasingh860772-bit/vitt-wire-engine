import os
import random
import requests
import datetime
import fal_client
import google.generativeai as genai
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from instagrapi import Client

# ==========================================
# 1. BRAIN, IDENTITY & SECRETS
# ==========================================
LORA_URL = "https://github.com/adityasingh860772-bit/vitt-wire-engine/releases/download/v1.0.0/T2Z3k6pzmg9oY6UFynuqx_pytorch_lora_weights.safetensors"
VOICE_DNA = "aditya_voice.wav"

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
FAL_KEY = os.environ.get("FAL_KEY")
IG_USERNAME = os.environ.get("IG_USERNAME")
IG_PASSWORD = os.environ.get("IG_PASSWORD")

genai.configure(api_key=GEMINI_API_KEY)

# ==========================================
# 2. STUDIO DYNAMICS
# ==========================================
CONSTANT_PROPS = "a professional broadcast mic, a laptop with subtle screen glow reflecting on face, a coffee mug with 'The Vitt Wire' text printed on it"
RANDOM_PROPS = ["a sleek tablet", "a stack of financial files", "a smartphone face down"]
POSITIONS = ["on the left", "in the foreground", "next to the mic"]

# ==========================================
# 3. AUTOPILOT MODULES
# ==========================================

def generate_daily_script():
    print("Writing Crypto/Business script...")
    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    edition = "Morning Briefing" if ist_now.hour < 15 else "Evening Wrap-Up"
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = (
        f"Act as a Financial Analyst for 'The Vitt Wire'. Edition: {edition}. "
        "Create content about Latest Global Crypto/AI news and its IMPACT on the Indian Market. "
        "MANDATORY: Script must be 50-60 words in Hinglish. "
        "Format: SCRIPT: [text] CAPTION: [engaging caption with hashtags]"
    )
    
    response = model.generate_content(prompt)
    raw_text = response.text.replace('*', '').strip()
    script_part = raw_text.split("CAPTION:")[0].replace("SCRIPT:", "").strip()
    caption_part = raw_text.split("CAPTION:")[1].strip() if "CAPTION:" in raw_text else "#TheVittWire"
    return script_part, caption_part

def clone_voice(text):
    print("Cloning Voice...")
    voice_url = fal_client.upload_file(VOICE_DNA)
    result = fal_client.subscribe("fal-ai/playht/tts/v3", arguments={
        "text": text, "voice_engine": "PlayHT2.0", "cloned_voice_url": voice_url
    })
    audio_path = "voice.wav"
    with open(audio_path, 'wb') as f: f.write(requests.get(result["audio_url"]).content)
    return audio_path

def generate_visuals():
    print("Generating Avatar Visual...")
    prompt = (f"Aditya Singh as a news anchor, {CONSTANT_PROPS}, "
              f"{random.choice(RANDOM_PROPS)} {random.choice(POSITIONS)}. "
              "STRICTLY NO NOTEBOOKS. Cinematic studio lighting, 8k.")
    result = fal_client.subscribe("fal-ai/flux-lora", arguments={
        "prompt": prompt, "image_size": "portrait_16_9", 
        "loras": [{"path": LORA_URL, "scale": 1.0}]
    })
    img_path = "visual.jpg"
    with open(img_path, 'wb') as f: f.write(requests.get(result['images'][0]['url']).content)
    return img_path

def animate_and_edit(image, audio, script):
    print("Animating & Adding Subtitles...")
    res = fal_client.subscribe("fal-ai/sadtalker", arguments={
        "source_image_url": fal_client.upload_file(image),
        "driven_audio_url": fal_client.upload_file(audio), "still_mode": True
    })
    raw_video = "raw.mp4"
    with open(raw_video, 'wb') as f: f.write(requests.get(res["video_url"]).content)
    
    video = VideoFileClip(raw_video)
    # Dynamic Subtitles (5-word chunks)
    words = script.split()
    chunks = [" ".join(words[i:i+5]) for i in range(0, len(words), 5)]
    dur = video.duration / len(chunks)
    
    subtitle_clips = []
    for i, chunk in enumerate(chunks):
        txt = TextClip(chunk, fontsize=40, color='yellow', font='DejaVu-Sans-Bold', 
                       stroke_color='black', stroke_width=2, method='caption', size=(video.w*0.8, None))
        txt = txt.set_start(i*dur).set_duration(dur).set_position(("center", "bottom")).margin(bottom=60)
        subtitle_clips.append(txt)
        
    final_v = "Final_Reel.mp4"
    CompositeVideoClip([video] + subtitle_clips).write_videofile(final_v, fps=24, codec="libx264")
    return final_v

def publish(video, caption):
    print("Publishing to Instagram/Facebook...")
    cl = Client()
    cl.login(IG_USERNAME, IG_PASSWORD)
    cl.clip_upload(video, caption)

if __name__ == "__main__":
    s, c = generate_daily_script()
    v_audio = clone_voice(s)
    v_image = generate_visuals()
    v_raw = animate_and_edit(v_image, v_audio, s)
    publish(v_raw, c)
