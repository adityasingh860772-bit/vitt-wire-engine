import os
import urllib.request
import urllib.error
import json

# 1. THE PERMANENT IDENTITY LINK
my_lora_url = "https://v3b.fal.media/files/b/0a9a022b/T273k6pzmg9oY5UFynuqx_pytorch_lora_weights.safetensors"

# 2. PRODUCTION SETTINGS
anchor_studio = "a premium, minimalist modern glass office in Mumbai with a clean white desk and a soft-focus city skyline"

# 3. THE MASTER PROMPT
prompt = f"Professional studio portrait of AdityaSinghAI wearing a tailored navy blue three-piece suit, sitting at {anchor_studio}. High-end broadcast lighting, 8k photorealistic."

# 4. THE FLUX LORA ENGINE
fal_key = os.getenv("FAL_KEY")

if fal_key:
    # HARDENED PAYLOAD: Uses exact dimensions and removes optional flags to prevent 422 errors
    payload = {
        "prompt": prompt,
        "loras": [{"path": my_lora_url, "scale": 1.0}],
        "image_size": {"width": 1280, "height": 720}
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
    except urllib.error.HTTPError as e:
        # DETAILED ERROR CATCHER: Prints the exact reason for the 422 error
        error_details = e.read().decode("utf-8")
        print(f"Production Error (Server Details): {error_details}")
    except Exception as e:
        print(f"System Error: {e}")
else:
    print("Error: FAL_KEY not found in environment secrets.")
