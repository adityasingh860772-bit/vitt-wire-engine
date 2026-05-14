import os, random, requests, datetime, subprocess, sys, builtins
import pytz # IST logic ke liye
import fal_client
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip

def print(*args, **kwargs):
    kwargs['flush'] = True
    builtins.print(*args, **kwargs)

# 1. Identity & Secrets
LORA_URL = "https://github.com/adityasingh860772-bit/vitt-wire-engine/releases/download/v1.0.0/T2Z3k6pzmg9oY6UFynuqx_pytorch_lora_weights.safetensors"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
FAL_KEY = os.environ.get("FAL_KEY")

# 15-DAY PROFESSIONAL WARDROBE
WARDROBE = [
    "sharp navy blue blazer, white formal shirt", "charcoal grey Nehru jacket",
    "premium solid black polo", "sleek olive green crew neck",
    "professional beige linen shirt", "royal blue shirt, silver tie",
    "light grey blazer over black tee", "maroon shirt, folded sleeves",
    "white shirt with black waistcoat", "dark forest green blazer",
    "sky blue shirt, navy tie", "tan leather jacket, black turtleneck",
    "classic black suit, white shirt", "grey textured blazer",
    "off-white premium Nehru jacket"
]

CONSTANT_PROPS = "professional broadcast mic, laptop with screen glow, 'The Vitt Wire' coffee mug"
RANDOM_PROPS = ["a sleek tablet", "a stack of financial files", "a smartphone face down"]
POSITIONS = ["on the left", "in the foreground", "next to the mic"]

def get_vitt_script():
    print("Triggering Gemini 1.5 Flash (Stage-Ready Vocabulary)...")
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(ist)
    edition = "Morning Briefing" if now.hour < 15 else "Evening Wrap-Up"
    
    # Emergency Fallback
    fb_s = f"Namaste India! The Vitt Wire ke {edition} mein swagat hai. Global market volatility ke beech AI stocks naye highs par hain. Indian investors ko abhi cautious rehna chahiye. Stay tuned!"
    fb_c = "#TheVittWire #FinanceNews #Investing #AI"

    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = f"Act as Financial Analyst Aditya Singh. Edition: {edition}. Tone: Professional, High-level Hinglish. 50 words. Format: SCRIPT: [text] CAPTION: [caption]"
        res = client.models.generate_content(model='gemini-1.5-flash', contents=prompt)
        raw = res.text.replace('*', '').strip()
        s = raw.split("CAPTION:")[0].replace("SCRIPT:", "").strip()
        c = raw.split("CAPTION:")[1].strip() if "CAPTION:" in raw else fb_c
        return s, c
    except:
        return fb_s, fb_c

def assembly_line():
    script, caption = get_vitt_script()
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(ist)
    
    # 15-Day Wardrobe & Random Props Logic
    day_idx = now.toordinal() % 15
    outfit = WARDROBE[day_idx]
    prop = f"{random.choice(RANDOM_PROPS)} {random.choice(POSITIONS)}"
    
    # 2. Flux Visual (Direct URL to Save Time)
    print(f"Generating Visual (Day {day_idx+1}): {outfit}...")
    img_prompt = f"Aditya Singh {outfit}, sitting in studio, {CONSTANT_PROPS}, {prop}, 8k photorealistic."
    img_res = fal_client.subscribe("fal-ai/flux-lora", arguments={"prompt": img_prompt, "loras": [{"path": LORA_URL, "scale": 1.0}]})
    
    # 3. Voice & SadTalker (Face Enhancer ON)
    from gtts import gTTS
    gTTS(script, lang='hi', tld='co.in').save("v.wav")
    print("Animating Avatar (High-Quality Enhancer)...")
    anim = fal_client.subscribe("fal-ai/sadtalker", arguments={
        "source_image_url": img_res['images'][0]['url'],
        "driven_audio_url": fal_client.upload_file("v.wav"),
        "still_mode": True,
        "preprocess": "full",
        "enhancer": "gfpgan"
    })
    
    v_url = anim.get("video_url") or anim.get("url")
    with open("raw.mp4", 'wb') as f: f.write(requests.get(v_url).content)

    # 4. Final Edit: Table Props & 5-word Subtitles
    clip = VideoFileClip("raw.mp4")
    bar = ColorClip(size=(clip.w, 160), color=(0,0,0)).set_opacity(0.7).set_duration(clip.duration).set_position(("center", "bottom"))
    
    words = script.split()
    chunks = [" ".join(words[i:i+5]) for i in range(0, len(words), 5)]
    dur = clip.duration / len(chunks)
    subs = [TextClip(c, fontsize=40, color='yellow', font='DejaVu-Sans-Bold', method='caption', size=(clip.w*0.8, None)).set_start(i*dur).set_duration(dur).set_position(("center", "bottom")).margin(bottom=75) for i, c in enumerate(chunks)]
    
    # Name Plate
    name = TextClip("ADITYA SINGH | THE VITT WIRE", fontsize=25, color='white', font='DejaVu-Sans-Bold').set_duration(clip.duration).set_position((50, 50))

    final_v = "The_Vitt_Wire_Final.mp4"
    CompositeVideoClip([clip, bar, name] + subs).write_videofile(final_v, fps=24, codec="libx264")
    with open("meta.txt", "w") as f: f.write(f"{final_v}|{caption}")

if __name__ == "__main__":
    assembly_line()
