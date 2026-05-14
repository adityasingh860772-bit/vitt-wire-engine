import os
import sys
from moviepy.editor import ImageClip, AudioFileClip

# ======================================================
# VITT WIRE: MASTERMIND VOICE ACTIVATION (9:00 AM IST)
# ======================================================

def assemble_broadcast():
    """Combines research visuals with Aditya's Voice DNA."""
    
    # EXACT FILENAMES FROM YOUR REPOSITORY
    voice_sample = "aditya_voice.wav"
    visual_input = "output_reels.png"
    final_output = "vitt_wire_live.mp4"

    print("--- STARTING FINAL ASSEMBLY ---")

    # 1. VALIDATE VOICE DNA
    if not os.path.exists(voice_sample):
        print(f"CRITICAL ERROR: {voice_sample} is missing from the repository.")
        sys.exit(1)
    else:
        print(f"SUCCESS: {voice_sample} detected.")

    # 2. VALIDATE VISUALS
    # Fallback to your reference image if the engine output isn't ready
    if not os.path.exists(visual_input):
        print(f"WARNING: {visual_input} not found. Using fallback asset.")
        visual_input = "face_ref.jpg.jpg"

    try:
        # 3. SYNC AUDIO & IMAGE
        audio = AudioFileClip(voice_sample)
        image = ImageClip(visual_input).set_duration(audio.duration)
        
        # 4. EXPORT BROADCAST
        video = image.set_audio(audio)
        video.write_videofile(final_output, fps=24, codec="libx264", audio_codec="aac")
        
        print(f"--- BROADCAST LOCKED: {final_output} is ready ---")

    except Exception as e:
        print(f"ASSEMBLY FAILED: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    assemble_broadcast()
