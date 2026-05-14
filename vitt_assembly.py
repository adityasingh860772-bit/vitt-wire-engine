import os
import random
import requests
import datetime
import subprocess
import sys
import builtins

# ==========================================
# 0. TELEMETRY OVERRIDE (LIVE LOGS FORCE FLUSH)
# ==========================================
def print(*args, **kwargs):
    kwargs['flush'] = True
    builtins.print(*args, **kwargs)

print("Engine Initializing... Telemetry Active!")
import fal_client
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

WARDROBE = [
    "wearing a sharp navy blue blazer over a crisp white formal shirt",
    "wearing a professional charcoal grey Nehru jacket over a light blue formal shirt",
    "wearing a premium solid black polo T-shirt",
    "wearing a sleek olive green full-sleeve crew neck T-shirt",
    "wearing a professional beige linen shirt"
]

CONSTANT_PROPS = "a professional broadcast mic, a laptop with subtle screen glow reflecting on face, a coffee mug with 'The Vitt Wire' text printed on it"
RANDOM_PROPS = ["a sleek tablet", "a stack of financial files", "a smartphone face down"]
POSITIONS = ["on the left", "in the foreground", "next to the mic"]

# ==========================================
# 3. AUTOPILOT MODULES (WITH BULLETPROOF FAILSAFES)
# ==========================================

def generate_daily_script():
    print("Executing Tactical Override: Installing modern SDKs & gTTS...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai", "pydantic", "gTTS", "-q"])
    
    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    edition = "Morning Briefing" if ist_now.hour < 15 else "Evening Wrap-Up"
    
    prompt = (
        f"Act as a Financial Analyst for 'The Vitt Wire'. Edition: {edition}. "
        "Focus: Latest Global Crypto/AI news and its IMPACT on the Indian Market/Investors. "
        "Tone: Energetic, Professional, Hinglish. MANDATORY: Script exactly 50-60 words. "
        "Format: SCRIPT: [text] CAPTION: [caption with hashtags]"
    )
    
    try:
        from google import genai
        print("Connecting to Secure GenAI Nodes...")
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        response = gemini_client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
        )
        raw_text = response.text.replace('*', '').strip()
        script_part = raw_text.split("CAPTION:")[0].replace("SCRIPT:", "").strip()
        caption_part = raw_text.split("CAPTION:")[1].strip() if "CAPTION:" in raw_text else "#TheVittWire"
        print("Script Generated Successfully!")
        return script_part, caption_part
        
    except Exception as e:
        print(f"GenAI Node Failed ({e}). Engaging Emergency Backup Script...")
        fallback_script = f"Namaste India! The Vitt Wire ke {edition} mein aapka swagat hai. Global crypto market mein aaj heavy volatility dekhne ko mil rahi hai. AI aur tech stocks naye highs touch kar rahe hain. Indian investors ko abhi ek cautious aur balanced approach rakhni chahiye. Apne portfolio ko diversify karein aur trends watch karein. Stay tuned!"
        fallback_caption = "#CryptoIndia #ShareMarket #TheVittWire #FinanceNews #Investing"
        return fallback_script, fallback_caption

def generate_visuals():
    print("Selecting Daily Outfit & Generating Avatar...")
    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    outfit_index = (ist_now.toordinal()) % 5 
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
    print("Visuals Generated successfully!")
    return img_path

def clone_voice(text):
    # THE SURGICAL BYPASS: Dropping PlayHT, using Local Server TTS to prevent Hangs
    print("Bypassing hanging PlayHT Node... Engaging Local gTTS Engine...")
    from gtts import gTTS
    # Generating Indian English/Hindi accented voice locally
    tts = gTTS(text, lang='hi', tld='co.in') 
    audio_path = "voice.wav"
    tts.save(audio_path)
    print("Emergency Voice Generated Successfully!")
    return audio_path

def animate_and_edit(image, audio, script):
    print("Animating Avatar & Burning Subtitles (This takes 3-5 mins)...")
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
    print("Video Animation Complete!")
    return final_v

def publish(video, caption):
    print("Automated Publishing to Meta Ecosystem... (Check Phone for Login Approvals)")
    cl = Client()
    cl.request_timeout = 60 
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
