import os
import urllib.request
import urllib.error
import json
import time
import random

# ==========================================
# THE VITT WIRE: DYNAMIC PRODUCTION ENGINE
# ==========================================

# 1. PERMANENT IDENTITY LINK
my_lora_url = "https://github.com/adityasingh860772-bit/vitt-wire-engine/releases/download/v1.0.0/T2Z3k6pzmg9oY6UFynuqx_pytorch_lora_weights.safetensors"

# 2. DYNAMIC ASSET POOLS
# These lists ensure that every broadcast looks fresh and authentic
outfits = [
    "a charcoal grey double-breasted suit with a subtle pinstripe",
    "a tailored midnight black tuxedo with a crisp white shirt",
    "a professional navy blue three-piece suit with a silk tie",
    "a premium maroon velvet blazer over a black turtleneck",
    "a sophisticated olive green Italian-cut suit"
]

prop_placements = [
    "the Space Gray laptop is open and angled slightly to the left, with the studio mic positioned near the center",
    "the laptop is closed on the right side of the desk, while the studio mic is pulled close to the subject",
    "the studio mic is on a boom arm hanging from above, with the laptop centered and active on the desk",
    "the desk is clean with the laptop pushed to the far edge, and the microphone set to the right side"
]

lighting_moods = [
    "warm golden hour light streaming through the glass",
    "cool blue twilight tones with sharp rim lighting",
    "clean high-key midday office lighting",
    "moody cinematic shadows with a soft purple neon accent from the city"
]

# 3. PRODUCTION ENGINE
def generate_broadcast_image():
    fal_key = os.getenv("FAL_KEY")
    if not fal_key:
        print("CRITICAL ERROR: FAL_KEY missing in GitHub Secrets.")
        return

    # Randomly select the day's look and set arrangement
    current_outfit = random.choice(outfits)
    current_props = random.choice(prop_placements)
    current_lighting = random.choice(lighting_moods)

    # BRAND STYLE LOCK: Fixed Environment, Dynamic Details
    hair_style = "highly voluminous, thick professional textured hair with significant height and sharp styling"
    base_studio = "a premium, minimalist modern glass office in Mumbai with a soft-focus city skyline"

    # CONSTRUCT THE MASTER PROMPT
    prompt = (
        f"Professional studio portrait of AdityaSinghAI with {hair_style}. "
        f"He is wearing {current_outfit}. He is sitting at a large professional desk where {current_props}. "
        f"The setting is {base_studio}. Lighting is {current_lighting}. "
        f"8k photorealistic, hyper-detailed textures, shallow depth of field, sharp focus on subject."
    )

    payload = {
        "prompt": prompt,
        "loras": [{"path": my_lora_url.strip(), "scale": 1.15}], 
        "image_size": {"width": 1280, "height": 720},
        "num_inference_steps": 40 
    }
    
    req = urllib.request.Request(
        "https://fal.run/fal-ai/flux-lora",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Key {fal_key}", "Content-Type": "application/json"}
    )
    
    for attempt in range(3):
        try:
            print(f"Starting Production (Attempt {attempt + 1}/3)...")
            print(f"Today's Configuration: {current_outfit} | {current_lighting}")
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                image_url = result.get("images", [{}])[0].get("url")
                print(f"IMAGE_READY: {image_url}")
                return image_url
        except Exception as e:
            print(f"Attempt failed. Retrying... Error: {e}")
            time.sleep(10)
            
    print("FATAL ERROR: Automated production failed.")

# THE CRITICAL GATE: DOUBLE UNDERSCORES (__) SECURED
if __name__ == "__main__":
    generate_broadcast_image()
