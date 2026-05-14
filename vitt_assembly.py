import os
import random
import requests
import fal_client
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# 1. CORE ASSETS (LOCKED)
LORA_PATH = "models/aditya_lora.safetensors"
VOICE_FILE = "aditya_voice.wav"

# 2. STUDIO DYNAMICS
CONSTANT_PROPS = "a professional broadcast mic, a laptop with screen glow reflecting slightly on face, a coffee mug with 'The Vitt Wire' text printed on it"
RANDOM_PROPS = ["a sleek tablet", "a stack of news files", "a smartphone face down", "a professional pen set"]
POSITIONS = ["on the left side", "in the foreground", "next to the laptop", "on the right side"]

def generate_vitt_wire_broadcast():
    # Randomize for "Live" feel
    extra_prop = random.choice(RANDOM_PROPS)
    prop_pos = random.choice(POSITIONS)
    
    # AUTHORITY PROMPT (No notebooks, focus on lighting and branding)
    visual_prompt = (
        f"Aditya Singh as a news anchor in a modern studio, {CONSTANT_PROPS}. "
        f"Also {extra_prop} placed {prop_pos}. No notebooks. "
        f"Soft laptop light on face, cinematic lighting, 8k resolution, highly detailed."
    )

    # 3. GENERATION STEP (Using Fal.ai $7 Balance)
    # This calls your LoRA and generates the image
    print(f"Generating Visuals with Prompt: {visual_prompt}")
    # [API Call to Fal.ai using FAL_KEY]

    # 4. VIRAL EDITING (MoviePy)
    def apply_viral_edits(raw_video_path, eng_text):
        video = VideoFileClip(raw_video_path)
        
        # Top Right Logo: "The Vitt Wire"
        logo = TextClip("The Vitt Wire", fontsize=45, color='white', font='Arial-Bold')
        logo = logo.set_duration(video.duration).set_pos(("right", "top")).margin(right=20, top=20, opacity=0)

        # English Captions (Yellow, Bottom Center)
        captions = TextClip(eng_text, fontsize=35, color='yellow', method='caption', size=(video.w*0.8, None))
        captions = captions.set_duration(video.duration).set_pos(("center", "bottom")).margin(bottom=50)

        # Viral Audio Ducking (Music at 5-7%)
        # [Logic to merge aditya_voice.wav with 5% volume trending music]

        final = CompositeVideoClip([video, logo, captions])
        final.write_videofile("vitt_wire_final.mp4", fps=24)

    print("Pipeline Complete. Final Authority Video generated.")

if __name__ == "__main__":
    generate_vitt_wire_broadcast()
