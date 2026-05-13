import random
import os
import urllib.request
import json

# 1. THE PERMANENT IDENTITY LINK
# This is your specific 1,500-step training DNA
my_lora_url = "https://v3b.fal.media/files/b/0a9a022b/T273k6pzmg9oY5UFynuqx_pytorch_lora_weights.safetensors"

# 2. PRODUCTION SETTINGS
anchor_studio = "a premium, minimalist modern glass office in Mumbai with a clean white desk and a soft-focus city skyline"

# 3. THE MASTER PROMPT
# Uses your trigger word 'AdityaSinghAI' to lock in your likeness
prompt = f"Professional studio portrait of AdityaSinghAI wearing a tailored navy blue three-piece suit, sitting at {anchor_studio}. High-end broadcast lighting, 8k photorealistic."

# 4. THE FLUX LORA ENGINE
fal_key = os.getenv("FAL_KEY")

if fal_key:
    # Cleaned payload: removed 'model_name' to fix the HTTP 422 error
    payload = {
        "prompt": prompt,
        "loras": [{"path": my_lora_url, "scale": 1.0}],
        "image_size": "landscape_16_9",
        "enable_safety_checker": True
    }
    
    req = urllib.request.Request(
        "https://fal.run/fal-ai/flux-lora",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Key {fal_key}",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            final_url = result.get("images", [{}])[0].get("url")
            print(f"IMAGE_READY: {final_url}")
    except Exception as e:
        print(f"Production Error: {e}")
else:
    print("Error: FAL_KEY not found in environment secrets.")
