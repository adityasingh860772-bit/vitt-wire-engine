import os, random, requests, datetime, sys, builtins
import pytz 
import fal_client
from moviepy.editor import *

def print(*args, **kwargs):
    kwargs['flush'] = True
    builtins.print(*args, **kwargs)

os.environ["COQUI_TOS_AGREED"] = "1"

# --- SECRETS & DNA ---
LORA_URL = "https://github.com/adityasingh860772-bit/vitt-wire-engine/releases/download/v1.0.0/T2Z3k6pzmg9oY6UFynuqx_pytorch_lora_weights.safetensors"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
FAL_KEY = os.environ.get("FAL_KEY")

WARDROBE = [
    "sharp navy blue blazer, white formal shirt", "charcoal grey Nehru jacket", "premium solid black polo", 
    "sleek olive green crew neck", "professional beige linen shirt", "royal blue shirt, silver tie", 
    "light grey blazer over black tee", "maroon shirt, folded sleeves", "white shirt with black waistcoat", 
    "dark forest green blazer", "sky blue shirt, navy tie", "tan leather jacket", 
    "classic black suit, white shirt", "grey textured blazer", "off-white premium Nehru jacket"
]

def get_verified_script(hour):
    print("--- Phase 1: Fetching LIVE Verified Global News ---")
    edition = "Morning Briefing" if hour < 15 else "Evening Wrap-Up"
    focus = "Pre-market opening, global cues, verified indices" if hour < 15 else "Closing market data, top gainers/losers, global wrap"
    
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        prompt = f"Act as Financial Analyst Aditya Singh for 'The Vitt Wire'. Edition: {edition}. Focus: {focus}. Base script on REAL-TIME VERIFIED GOOGLE SEARCH results from today. High-level Hinglish. Keep it crisp 55 words. Format: SCRIPT: [text] CAPTION: [caption with hashtags]"
        
        # FIX: Reverted to standard model name for better SDK compatibility
        res = client.models.generate_content(
            model='gemini-1.5-flash', 
            contents=prompt,
            config=types.GenerateContentConfig(tools=[types.Tool(google_search_retrieval=types.GoogleSearchRetrieval())])
        )
        
        raw = res.text.replace('*', '').strip()
        script = raw.split("CAPTION:")[0].replace("SCRIPT:", "").strip()
        caption = raw.split("CAPTION:")[1].strip() if "CAPTION:" in raw else "#TheVittWire #FinanceNews"
        return script, caption
    except Exception as e:
        print(f"Gemini Exception: {e}")
        return "Namaste India! Market updates ke liye bane rahein The Vitt Wire par.", "#TheVittWire"

def generate_aditya_voice(text):
    print("--- Phase 3: XTTS-v2 Voice Cloning (Using aditya_voice.wav) ---")
    if not os.path.exists("aditya_voice.wav"):
        print("ERROR: aditya_voice.wav NOT FOUND!")
        sys.exit(1)
    try:
        from TTS.api import TTS
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
        tts.tts_to_file(text=text, file_path="v.wav", speaker_wav="aditya_voice.wav", language="hi")
    except Exception as e:
        print(f"CRITICAL ERROR in Voice generation: {e}")
        sys.exit(1)

def assembly_line():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(ist)
    script, caption = get_verified_script(now.hour)
    
    outfit = WARDROBE[now.toordinal() % 15]
    prop = random.choice(["sleek tablet", "financial files", "smartphone"])
    
    print(f"--- Phase 2: Flux Visual Generation ---")
    img_prompt = f"Aditya Singh wearing {outfit}, sitting in a financial studio. He has thick hair volume, professional stylish groomed hair. Cinematic lighting, subtle laptop screen glow on face, broadcast mic, branded coffee mug, {prop} on desk, 8k photorealistic."
    
    img_res = fal_client.subscribe("fal-ai/flux-lora", arguments={"prompt": img_prompt, "image_size": "portrait_16_9", "loras": [{"path": LORA_URL, "scale": 1.0}]})
    flux_url = img_res['images'][0]['url']
    
    generate_aditya_voice(script)
    
    print("--- Phase 4: Avatar Lip-Sync ---")
    anim = fal_client.subscribe("fal-ai/sadtalker", arguments={
        "source_image_url": flux_url, "driven_audio_url": fal_client.upload_file("v.wav"),
        "still_mode": True, "preprocess": "full", "enhancer": "gfpgan"
    })
    v_url = anim.get("video_url") or anim.get("url") or anim["video"]["url"]
    with open("raw.mp4", 'wb') as f: f.write(requests.get(v_url).content)

    print("--- Phase 5: Post-Production ---")
    clip = VideoFileClip("raw.mp4")
    safe_zone_y = clip.h - 450
    
    words = script.split()
    chunks = [" ".join(words[i:i+5]) for i in range(0, len(words), 5)]
    dur = clip.duration / len(chunks)
    
    subs = [TextClip(c, fontsize=42, color='yellow', font='DejaVu-Sans-Bold', stroke_color='black', stroke_width=2, method='caption', size=(clip.w*0.8, None)).set_start(i*dur).set_duration(dur).set_position(("center", safe_zone_y + 20)) for i, c in enumerate(chunks)]
    
    bar = ColorClip(size=(clip.w, 180), color=(0,0,0)).set_opacity(0.6).set_duration(clip.duration).set_position(("center", safe_zone_y))
    name = TextClip("ADITYA SINGH | THE VITT WIRE", fontsize=28, color='white', font='DejaVu-Sans-Bold').set_duration(clip.duration).set_position((50, 50))
    logo = TextClip("LIVE 🔴", fontsize=25, color='red', font='DejaVu-Sans-Bold').set_duration(clip.duration).set_position((clip.w-150, 50))

    final_clip = CompositeVideoClip([clip, bar, name, logo] + subs)
    
    final_audio = clip.audio
    if os.path.exists("bgm.mp3"):
        bgm = AudioFileClip("bgm.mp3").volumex(0.12).set_duration(clip.duration)
        final_audio = CompositeAudioClip([clip.audio, bgm])

    final_audio = final_audio.audio_fadeout(0.5)
    final_clip = final_clip.set_audio(final_audio)

    final_clip.write_videofile("The_Vitt_Wire_Final.mp4", fps=24, codec="libx264")
    with open("meta.txt", "w") as f: f.write(f"The_Vitt_Wire_Final.mp4|{caption}")

if __name__ == "__main__":
    assembly_line()
