import os
import random
import requests
import datetime
import textwrap
import fal_client
import google.generativeai as genai
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
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
RANDOM_PROPS = ["a sleek tablet", "a stack of news files", "a smartphone face down", "a professional pen set"]
POSITIONS = ["on the left side", "in the foreground", "next to the laptop", "on the right side"]

# ==========================================
# 3. AUTOPILOT MODULES
# ==========================================

def generate_daily_script():
    print("Writing 30s Crypto/Business script for IG & FB Reels...")
    # IST Time conversion for accurate scheduling
    ist_now = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    current_hour = ist_now.hour
    
    if current_hour < 15:
        edition = "Morning Briefing"
        focus = "Latest Global AI news, Crypto (Bitcoin/Altcoins) movements, and their IMPACT on the Indian Stock Market opening."
        vibe = "urgent, energetic, and financial-focused."
    else:
        edition = "Evening Wrap-Up"
        focus = "Deep analysis of a major Crypto/Business trend and how it affects Indian investors and the local economy."
        vibe = "analytical, educational, and calm."

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = (
        f"Act as a Top Financial Analyst for 'The Vitt Wire'. Create {edition} content. "
        f"Topic: {focus}. Tone: {vibe} Hinglish. "
        f"MANDATORY: Script must be exactly 50-60 words. Explain Indian market impact. "
        f"Format:\nSCRIPT: [Start with 'Welcome to The Vitt Wire {edition}.']\n"
        f"CAPTION: [Write a highly engaging caption optimized for BOTH Instagram and Facebook Reels. Include 3 IG-specific hashtags and 3 Broad FB-friendly hashtags.]"
    )
    
    response = model.generate_content(prompt)
    raw_text = response.text.replace('*', '').strip()
    
    script_part = raw_text.split("CAPTION:")[0].replace("SCRIPT:", "").strip()
    try:
        caption_part = raw_text.split("CAPTION:")[1].strip()
    except:
        caption_part = "Market analysis for India! #TheVittWire #CryptoIndia #FinanceTips #ReelsFB"
        
    return script_part, caption_part

def clone_voice_xtts(text):
    print("Securely Cloning Voice DNA...")
    voice_url = fal_client.upload_file(VOICE_DNA)
    result = fal_client.subscribe(
        "fal-ai/playht/tts/v3",
        arguments={"text": text, "voice_engine": "PlayHT2.0", "cloned_voice_url": voice_url}
    )
    audio_path = "generated_voice.wav"
    with open(audio_path, 'wb') as f: f.write(requests.get(result.get("audio_url")).content)
    return audio_path

def generate_visual_avatar():
    print("Building 9:16 Studio Visuals...")
    visual_prompt = (f"Aditya Singh as a news anchor in a modern studio, {CONSTANT_PROPS}. "
                     f"Also {random.choice(RANDOM_PROPS)} placed {random.choice(POSITIONS)}. "
                     f"STRICTLY NO NOTEBOOKS. Soft laptop light on face, cinematic lighting, 8k resolution.")
    
    result = fal_client.subscribe(
        "fal-ai/flux-lora",
        arguments={"prompt": visual_prompt, "image_size": "portrait_16_9", "loras": [{"path": LORA_URL, "scale": 1.0}]}
    )
    image_path = "anchor_visual.jpg"
    with open(image_path, 'wb') as f: f.write(requests.get(result['images'][0]['url']).content)
    return image_path

def animate_sadtalker(image_path, audio_path):
    print("Animating Avatar (Lip-Sync)...")
    result = fal_client.subscribe(
        "fal-ai/sadtalker",
        arguments={"source_image_url": fal_client.upload_file(image_path), "driven_audio_url": fal_client.upload_file(audio_path), "still_mode": True}
    )
    video_path = "raw_anchor_video.mp4"
    with open(video_path, 'wb') as f: f.write(requests.get(result.get("video_url")).content)
    return video_path

def auto_fetch_trending_audio():
    viral_pool = ["https://cdn.pixabay.com/download/audio/2022/03/15/audio_27cecb5a85.mp3", "https://cdn.pixabay.com/download/audio/2022/10/25/audio_2d0fa50cc7.mp3"]
    audio_path = "auto_trending.mp3"
    with open(audio_path, 'wb') as f: f.write(requests.get(random.choice(viral_pool)).content)
    return audio_path

def assemble_final_reel(raw_video_path, script_text):
    print("Final Edit: Dynamic Captions & Mixing...")
    video = VideoFileClip(raw_video_path)
    
    # Static Logo
    logo = TextClip("The Vitt Wire", fontsize=40, color='white', font='DejaVu-Sans-Bold').set_duration(video.duration).set_pos(("right", "top")).margin(right=15, top=15, opacity=0.9)

    # Dynamic Subtitle Chunking (5 words at a time)
    words = script_text.split()
    chunk_size = 5
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    duration_per_chunk = video.duration / len(chunks)
    
    subtitle_clips = []
    for i, chunk in enumerate(chunks):
        txt_clip = TextClip(chunk, fontsize=35, color='yellow', font='DejaVu-Sans-Bold', stroke_color='black', stroke_width=2, method='caption', size=(video.w*0.8, None))
        txt_clip = txt_clip.set_position(("center", "bottom")).margin(bottom=50).set_start(i * duration_per_chunk).set_duration(duration_per_chunk)
        subtitle_clips.append(txt_clip)

    # Audio Ducking
    bg_music = AudioFileClip(auto_fetch_trending_audio()).volumex(0.05)
    if bg_music.duration < video.duration:
        from moviepy.audio.fx.all import audio_loop
        bg_music = audio_loop(bg_music, duration=video.duration)
    else:
        bg_music = bg_music.subclip(0, video.duration)
        
    video = video.set_audio(CompositeAudioClip([video.audio, bg_music]))

    output_filename = "Vitt_Wire_Autopilot_Final.mp4"
    CompositeVideoClip([video, logo] + subtitle_clips).write_videofile(output_filename, fps=24, codec="libx264", audio_codec="aac")
    return output_filename

def auto_publish_to_instagram(video_path, caption_text):
    print("ZERO-TOUCH: Safe Meta Upload (IG -> Auto FB Cross-Post)...")
    cl = Client()
    
    # Safe Login with Session Saving to avoid IP Bans
    session_file = "ig_session.json"
    try:
        if os.path.exists(session_file):
            cl.load_settings(session_file)
            cl.login(IG_USERNAME, IG_PASSWORD)
        else:
            cl.login(IG_USERNAME, IG_PASSWORD)
            cl.dump_settings(session_file)
            
        cl.clip_upload(video_path, caption_text)
        print("MISSION SUCCESS: Reel is safely live on Instagram (and syndicating to Facebook Page).")
    except Exception as e:
        print(f"IG Upload Error (Check login credentials or approval): {e}")

# ==========================================
# 4. EXECUTION
# ==========================================
if __name__ == "__main__":
    try:
        script, caption = generate_daily_script()
        voice = clone_voice_xtts(script)
        image = generate_visual_avatar()
        raw_v = animate_sadtalker(image, voice)
        final_v = assemble_final_reel(raw_v, script)
        auto_publish_to_instagram(final_v, caption)
    except Exception as e:
        print(f"System Crash: {e}")
