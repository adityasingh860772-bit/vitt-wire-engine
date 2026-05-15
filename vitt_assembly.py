import os, random, requests, datetime, sys, builtins, time
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
FAL_KEY = os.environ.get("FAL_KEY")

WARDROBE = [
    "sharp navy blue blazer, white formal shirt", "charcoal grey Nehru jacket", "premium solid black polo", 
    "sleek olive green crew neck", "professional beige linen shirt", "royal blue shirt, silver tie", 
    "light grey blazer over black tee", "maroon shirt, folded sleeves", "white shirt with black waistcoat", 
    "dark forest green blazer", "sky blue shirt, navy tie", "tan leather jacket", 
    "classic black suit, white shirt", "grey textured blazer", "off-white premium Nehru jacket"
]

def get_verified_script():
    print("--- Phase 1: Gemini API Bypassed. Using Mastermind's Hardcoded Script ---")
    
    # THE FIX: Directly supplying the dual-layer script. API Key completely ignored.
    tts_text = "नमस्कार! द विट वायर में आपका स्वागत है। आज भारतीय शेयर बाजार में भारी उछाल देखा गया। बैंकिंग और आईटी सेक्टर में सबसे ज्यादा खरीदारी रही। ग्लोबल मार्केट से भी पॉजिटिव संकेत मिल रहे हैं। कल के मार्केट ओपनिंग पर नजर बनाए रखें।"
    
    sub_text = "Namaskar! The Vitt Wire mein aapka swagat hai. Aaj Indian stock market mein bhari uchhaal dekha gaya. Banking aur IT sector mein sabse zyada buying rahi. Global market se bhi positive signals mil rahe hain. Kal ki market opening par nazar banaye rakhein."
    
    cap_text = "Indian Market hits new highs! 🚀 Banking and IT sectors lead the rally. Stay tuned for tomorrow's opening bell. #TheVittWire #StockMarketIndia #Sensex #Nifty50"
    
    return tts_text, sub_text, cap_text

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
    
    tts_script, sub_script, caption = get_verified_script()
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
