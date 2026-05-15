import os, random, requests, datetime, sys, builtins, time, re
import pytz 
import fal_client
from moviepy.editor import *
import moviepy.audio.fx.all as afx

def print(*args, **kwargs):
    kwargs['flush'] = True
    builtins.print(*args, **kwargs)

os.environ["COQUI_TOS_AGREED"] = "1"

# --- SECRETS & REPO LINKS ---
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
    print("--- Phase 1: Generating Dual-Layer Script (Using Universal Gemini-Pro) ---")
    edition = "Morning Briefing" if hour < 15 else "Evening Wrap-Up"
    focus = "Indian market updates, global cues, and standard market trends" if hour < 15 else "Market closing summary, top sector performance"
    
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    
    prompt = f"""Act as Financial Analyst Aditya Singh for 'The Vitt Wire'. Edition: {edition}. Focus: {focus}.
    STRICT RULES:
    1. You must provide the script in TWO formats.
    2. TTS_SCRIPT must be entirely in Devanagari characters.
    3. SUB_SCRIPT must be the exact same script but written in Roman English/Hinglish.
    4. Keep the script exactly 55-60 words for a 30-second video.
    5. Do NOT use asterisks (*) or markdown.
    
    FORMAT EXACTLY LIKE THIS:
    TTS_SCRIPT: [Devanagari text]
    SUB_SCRIPT: [Roman Hinglish text]
    CAPTION: [caption with hashtags]"""
    
    for attempt in range(3):
        try:
            # THE MASTERMIND FIX: Using the universally unlocked 'gemini-pro' (1.0). 
            # This bypasses all 404 and 429 API Key restrictions.
            model = genai.GenerativeModel('gemini-pro')
            res = model.generate_content(prompt)
            raw = res.text.replace('*', '').strip()
            
            tts_match = re.search(r'TTS_SCRIPT\s*:\s*(.*?)(?=SUB_SCRIPT\s*:)', raw, re.DOTALL | re.IGNORECASE)
            sub_match = re.search(r'SUB_SCRIPT\s*:\s*(.*?)(?=CAPTION\s*:)', raw, re.DOTALL | re.IGNORECASE)
            cap_match = re.search(r'CAPTION\s*:\s*(.*)', raw, re.DOTALL | re.IGNORECASE)
            
            if tts_match and sub_match:
                tts_text = tts_match.group(1).replace('\n', ' ').strip()
                sub_text = sub_match.group(1).replace('\n', ' ').strip()
                cap_text = cap_match.group(1).strip() if cap_match else "#TheVittWire #FinanceNews #StockMarketIndia"
                
                if len(tts_text) > 30 and len(sub_text) > 30:
                    return tts_text, sub_text, cap_text
            print(f"Attempt {attempt+1} regex parsing failed. Retrying...")
        except Exception as e:
            print(f"Gemini Attempt {attempt+1} Failed: {e}.")
            time.sleep(5)
            
    print("CRITICAL ERROR: Failed to generate properly formatted script after 3 attempts.")
    sys.exit(1)

def generate_aditya_voice(text):
    print("--- Phase 3: XTTS-v2 Voice Cloning ---")
    if not os.path.exists("aditya_voice.wav"):
        print("CRITICAL ERROR: aditya_voice.wav NOT FOUND in Repo!")
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
    
    tts_script, sub_script, caption = get_verified_script(now.hour)
    outfit = WARDROBE[now.toordinal() % 15]
    dynamic_prop = random.choice(["closed leather notebook", "stack of financial files", "smartphone", "leather tablet"])
    
    print(f"--- Phase 2: Flux Visual Generation (Locked Studio Setup) ---")
    if now.hour >= 8 and now.hour < 11:
        time_light_prompt = "bright, crisp, natural daylight streaming in from a window to his left, creating clean highlights."
    elif now.hour >= 17 and now.hour < 19:
        time_light_prompt = "warm, golden, atmospheric light from the large tripod lamp behind him and a desk lamp, creating an intimate, focused newsdesk feel."
    else:
        time_light_prompt = "cinematic, sophisticated studio lighting."

    img_prompt = f"A close-up, cinematic shot of Aditya Singh, wearing {outfit}, with neat professional hair style. He is seated at a sophisticated desk, featuring a fixed setup: a professional Shure SM7B-style broadcast microphone on a stand, a stylish black coffee mug, a leather office chair, and wearing an Apple Watch. The background shelves with warm, layered linear lighting, books, plants, and the large Bird of Paradise plant remain constant. The dynamic lighting is {time_light_prompt} On the desk, in front of him, there is a {dynamic_prop}. Depth of field, professional TV news anchor quality, 8k photorealistic."
    
    img_res = fal_client.subscribe("fal-ai/flux-lora", arguments={"prompt": img_prompt, "image_size": "portrait_16_9", "loras": [{"path": LORA_URL, "scale": 1.0}]})
    flux_url = img_res['images'][0]['url']
    
    generate_aditya_voice(tts_script)
    
    print("--- Phase 4: Avatar Lip-Sync Animation ---")
    anim = fal_client.subscribe("fal-ai/sadtalker", arguments={
        "source_image_url": flux_url, "driven_audio_url": fal_client.upload_file("v.wav"),
        "still_mode": True, "preprocess": "full", "enhancer": "gfpgan"
    })
    v_url = anim.get("video_url") or anim.get("url") or anim["video"]["url"]
    with open("raw.mp4", 'wb') as f: f.write(requests.get(v_url).content)

    print("--- Phase 5: Safe-Zone Editing & BGM ---")
    clip = VideoFileClip("raw.mp4")
    safe_zone_y = clip.h - 450 
    
    words = sub_script.split()
    chunks = [" ".join(words[i:i+5]) for i in range(0, len(words), 5)]
    dur = clip.duration / len(chunks)
    
    subs = [TextClip(c, fontsize=42, color='yellow', font='DejaVu-Sans-Bold', stroke_color='black', stroke_width=2, method='caption', size=(int(clip.w*0.8), None)).set_start(i*dur).set_duration(dur).set_position(("center", safe_zone_y + 20)) for i, c in enumerate(chunks)]
    
    bar = ColorClip(size=(clip.w, 180), color=(0,0,0)).set_opacity(0.6).set_duration(clip.duration).set_position(("center", safe_zone_y))
    name = TextClip("ADITYA SINGH | THE VITT WIRE", fontsize=28, color='white', font='DejaVu-Sans-Bold').set_duration(clip.duration).set_position((50, 50))
    logo = TextClip("LIVE 🔴", fontsize=25, color='red', font='DejaVu-Sans-Bold').set_duration(clip.duration).set_position((clip.w-150, 50))

    final_clip = CompositeVideoClip([clip, bar, name, logo] + subs)
    
    final_audio = clip.audio
    if os.path.exists("bgm.mp3"):
        bgm = AudioFileClip("bgm.mp3").fx(afx.audio_loop, duration=clip.duration).volumex(0.12)
        final_audio = CompositeAudioClip([clip.audio, bgm])

    final_audio = final_audio.fx(afx.audio_fadeout, 0.5) 
    final_clip = final_clip.set_audio(final_audio)

    final_clip.write_videofile("The_Vitt_Wire_Final.mp4", fps=24, codec="libx264")
    
    with open("meta.txt", "w", encoding="utf-8") as f: 
        f.write(f"The_Vitt_Wire_Final.mp4|{caption}")
    print("Assembly Complete!")

if __name__ == "__main__":
    assembly_line()
