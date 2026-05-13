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
# This targets your verified LoRA weights from the public v1.0.0 release.
my_lora_url = "https://github.com/adityasingh860772-bit/vitt-wire-engine/releases/download/v1.0.0/T2Z3k6pzmg9oY6UFynuqx_pytorch_lora_weights.safetensors"

# 2. THE DYNAMIC ASSET VAULT
# These pools ensure the AI persona changes clothes and moves props daily.
outfits = [
    "a tailored navy blue three-piece suit with a silk tie",
    "a charcoal grey double-breasted suit with a white pocket square",
    "a sophisticated black blazer over a crisp white dress shirt",
    "a premium maroon velvet suit jacket with a black turtleneck",
    "a professional dark forest green Italian-cut suit"
]

prop_arrangements = [
    "a professional black condenser mic on a silver boom arm on the right, an open Space Gray laptop in the center, and a leather-bound diary with a metal pen on the left",
    "a sleek laptop positioned on the far right, a studio microphone pulled directly to the center, and a stack of three thick cinematography books on the left",
    "the laptop is centered and open, with a professional mic slightly to the left, and an open notebook with handwritten notes and a black pen on the right",
    "a minimal setup with the laptop on the left, the studio mic on the right, and a premium metal pen resting on a closed hardback diary in the foreground"
]

# 3. PRODUCTION ENGINE
def generate_broadcast_image():
    # Credentials Check
    fal_key = os.getenv("FAL_KEY")
    if not fal_key:
        print("CRITICAL ERROR: FAL_KEY missing in GitHub Secrets.")
        return

    # Randomizing Today's Configuration
    daily_outfit = random.choice(outfits)
    daily_props = random.choice(prop_arrangements)

    # BRAND STYLE LOCK: Fixed Identity & Environment
    hair_style = "highly voluminous, thick professional textured hair with significant height and sharp styling"
    studio_env = "a high-end glass office in Mumbai with a soft-focus twilight skyline and cinematic softbox lighting"

    # CONSTRUCT THE MASTER PROMPT
    prompt = (
        f"Professional hyper-realistic studio portrait of AdityaSinghAI with {hair_style}. "
        f"He is wearing {daily_outfit}. He is sitting at a large professional wooden desk. "
        f"Set Dressing: {daily_props}. "
        f"Environment: {studio_env}. "
        f"Details: 8k UHD, visible skin pores, realistic fabric texture, shallow depth of field, sharp focus on the subject."
    )

    payload = {
        "prompt": prompt,
        "loras": [{"path": my_lora_url.strip(), "scale": 1.15}], # 1.15 scale locks your specific features
        "image_size": {"width": 1280, "height": 720},
        "num_inference_steps": 40 # High density for realistic micro-textures
    }
    
    req = urllib.request.Request(
        "https://fal.run/fal-ai/flux-lora",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Key {fal_key}",
            "Content-Type": "application/json"
        }
    )
    
    # 3-Attempt Fail-safe for Indian Standard Time (IST) Launch
    for attempt in range(3):
        try:
            print(f"Executing Daily Broadcast Production (Attempt {attempt + 1}/3)...")
            print(f"Wardrobe: {daily_outfit}")
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                image_url = result.get("images", [{}])[0].get("url")
                print(f"IMAGE_READY: {image_url}")
                return image_url
        except Exception as e:
            print(f"Production stall. Retrying in 10 seconds... Error: {e}")
            time.sleep(10)
            
    print("FATAL ERROR: Automated production failed after 3 attempts.")

# THE CRITICAL GATE: MANDATORY DOUBLE UNDERSCORES (__)
if __name__ == "__main__":
    generate_broadcast_image()
