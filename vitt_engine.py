import os
import urllib.request
import urllib.error
import json
import time

# ==========================================
# THE VITT WIRE: FINAL PRODUCTION ENGINE
# ==========================================

# 1. PERMANENT IDENTITY LINK
# Verified asset link from your v1.0.0 public release
my_lora_url = "https://github.com/adityasingh860772-bit/vitt-wire-engine/releases/download/v1.0.0/T2Z3k6pzmg9oY6UFynuqx_pytorch_lora_weights.safetensors"

# 2. BRAND STYLE LOCK 
# Surgical hair volume fix: High-priority anchors + 1.15 Scale
hair_style = "highly voluminous, thick professional textured hair with significant height and sharp styling"
anchor_studio = "a premium, minimalist modern glass office in Mumbai with a clean white desk and a soft-focus city skyline"

# 3. THE MASTER PROMPT
prompt = f"Professional studio portrait of AdityaSinghAI with {hair_style}. He is wearing a tailored navy blue three-piece suit, sitting at {anchor_studio}. High-end broadcast lighting, 8k photorealistic, sharp focus."

# 4. AUTO-RETRY PRODUCTION ENGINE
def generate_broadcast_image():
    # Verification of Credentials
    fal_key = os.getenv("FAL_KEY")
    if not fal_key:
        print("CRITICAL ERROR: FAL_KEY missing in GitHub Secrets.")
        return

    # Payload Construction
    payload = {
        "prompt": prompt,
        "loras": [{"path": my_lora_url.strip(), "scale": 1.15}], 
        "image_size": {"width": 1280, "height": 720},
        "num_inference_steps": 30
    }
    
    req = urllib.request.Request(
        "https://fal.run/fal-ai/flux-lora",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Key {fal_key}",
            "Content-Type": "application/json"
        }
    )
    
    # 3-Attempt Fail-safe for Broadcast Reliability
    for attempt in range(3):
        try:
            print(f"Starting Production (Attempt {attempt + 1}/3)...")
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                image_url = result.get("images", [{}])[0].get("url")
                print(f"IMAGE_READY: {image_url}")
                return image_url
        except Exception as e:
            print(f"Attempt {attempt + 1} failed. Retrying in 10 seconds... Error: {e}")
            time.sleep(10)
            
    print("FATAL ERROR: Automated production failed after 3 attempts.")

# THE CRITICAL FIX: DOUBLE UNDERSCORES (__) ARE MANDATORY
if _name_ == "_main_":
    generate_broadcast_image()
