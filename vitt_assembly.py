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
# 2. THE 15-DAY NO-REPEAT WARDROBE
# ==========================================
WARDROBE = [
    "wearing a sharp navy blue blazer over a crisp white formal shirt",
    "wearing a professional charcoal grey Nehru jacket over a light blue formal shirt",
    "wearing a premium solid black polo T-shirt",
    "wearing a sleek olive green full-sleeve crew neck T-shirt",
    "wearing a professional beige linen shirt",
    "wearing a classic sky blue Oxford button-down shirt",
    "wearing a maroon Nehru jacket over a white mandarin collar shirt",
    "wearing a minimalist dark grey mandarin collar shirt",
    "wearing a light blue striped formal shirt with a slim black silk tie",
    "wearing a khaki tan safari-style utility shirt",
    "wearing a burgundy Henley-neck full-sleeve T-shirt",
    "wearing an all-black power look with a black shirt under a sharp black blazer",
    "wearing a dark indigo denim shirt over a plain white inner T-shirt",
    "wearing a royal blue textured polo shirt",
    "wearing a light brown waistcoat over a plain white formal shirt"
]

CONSTANT_PROPS = "a professional broadcast mic, a laptop with subtle screen glow reflecting on face, a coffee mug with 'The Vitt Wire' text printed on it"
RANDOM_PROPS = ["a sleek tablet", "a stack of financial files", "a smartphone face down"]
POSITIONS = ["on the left", "in the foreground", "next to the mic"]

# ==========================================
# 3. AUTOPILOT MODULES
# ==========================================

def generate_daily_script():
    print("Writing Crypto/Business script for The Vitt Wire...")
    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    edition = "Morning Briefing" if ist_now.hour < 15 else "Evening Wrap-Up"
    
    # FIXED: Standard model name without 'models/' prefix
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = (
        f"Act as a Financial Analyst for 'The Vitt Wire'. Edition: {edition}. "
        "Focus: Latest Global Crypto/AI news and its IMPACT on the Indian Market/Investors."
        "Tone: Energetic, Professional, Hinglish. MANDATORY: Script exactly 50-60 words. "
        "Format: SCRIPT: [text] CAPTION: [caption with hashtags]"
    )
    
    response = model.generate_content(prompt)
    raw_text = response.text.replace('*', '').strip()
    script_part = raw_text.split("CAPTION:")[0].replace("SCRIPT:", "").strip()
    caption_part = raw_text.split("CAPTION:")[1].strip() if "CAPTION:" in raw_text else "#TheVittWire"
    return script_part, caption_part

def generate_visuals():
    print("Selecting Daily Outfit & Generating Avatar...")
    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    outfit_index = (ist_now.toordinal()) % 15 
    daily_outfit = WARDROBE[outfit_index]
    
    prompt = (f"Aditya Singh {daily_outfit}, sitting in a modern financial news studio, {CONSTANT_PROPS}. "
              f"{random.choice(RANDOM_PROPS)} {random.choice(POSITIONS)}. "
              "STRICTLY NO NOTEBOOKS. Cinematic studio lighting, 8k, photorealistic.")
    
    result = fal_client.subscribe("fal-ai/flux-lora", arguments={
        "prompt": prompt, "image_size": "portrait_16_9", 
        "loras": [{"path": LORA_URL, "scale": 1.0}]
    })
    img_path = "visual.jpg"
    with open(img_path, 'wb') as f: f.write(requests.get(result['images'][0]['url']).content)
    return img_path

def clone_voice(text):
    print("Cloning Voice DNA...")
    voice_url = fal_client.upload_file(VOICE_DNA)
    result = fal_client.subscribe("fal-ai/playht/tts/v3", arguments={
        "text": text, "voice_engine": "PlayHT2.0", "cloned_voice_url": voice_url
    })
    audio_path = "voice.wav"
    with open(audio_path, 'wb') as f: f.write(requests.get(result["audio_url"]).content)
    return audio_path

def animate_and_edit(image, audio, script):
    print("Animating Avatar & Burning Subtitles...")
    res = fal_client.subscribe("fal-ai/sadtalker", arguments={
        "source_image_url": fal_client.upload_file(image),
        "driven_audio_url": fal_client.upload_file(audio), "still_mode": True
    })
    raw_video = "raw.mp4"
    with open(raw_video, 'wb') as f: f.write(requests.get(res["video_url"]).content)
    
    video = VideoFileClip(raw_video)
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
    print("Automated Publishing to Meta Ecosystem...")
    cl = Client()
    session_file = "ig_session.json"
    if os.path.exists(session_file):
        cl.load_settings(session_file)
    cl.login(IG_USERNAME, IG_PASSWORD)
    if not os.path.exists(session_file):
        cl.dump_settings(session_file)
        
    cl.clip_upload(video, caption)
    print("Broadcast Successful!")

if __name__ == "__main__":
    try:
        s, c = generate_daily_script()
        v_img = generate_visuals()
        v_aud = clone_voice(s)
        v_final = animate_and_edit(v_img, v_aud, s)
        publish(v_final, c)
    except Exception as e:
        print(f"System Offline Error: {e}")
