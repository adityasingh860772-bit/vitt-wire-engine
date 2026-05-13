import random
import os
import urllib.request
import json
import base64

# 1. THE STUDIO CONFIGURATION
# This maintains the high-end Mumbai brand identity we established
anchor_studio = "a premium, minimalist modern glass office in Mumbai with a clean white desk and a soft-focus city skyline in the background"

# 2. DYNAMIC BROADCAST ELEMENTS (Subliminal Realism)
props = [
    "a thin silver laptop positioned on the left side of the desk",
    "a stack of three leather-bound finance books on the right corner",
    "a silver laptop centered on the desk with a small coffee mug nearby",
    "a clean desk with just a black smartphone placed near the edge",
    "a tablet propped up on a stand next to a neat pile of documents"
]

costumes = [
    "a tailored navy blue three-piece suit",
    "a charcoal grey slim-fit blazer with a white shirt",
    "a professional black Nehru jacket",
    "a light grey textured blazer",
    "a dark maroon formal blazer"
]

selected_prop = random.choice(props)
selected_costume = random.choice(costumes)

# THE MASTER PROMPT
# Note: We generate a generic professional base first, which we then swap with your face
prompt = f"Professional studio portrait of a man wearing {selected_costume}. He is sitting at {anchor_studio}. On the desk, there is {selected_prop}. High-end broadcast lighting, 8k photorealistic."

print(f"Today's Look: {selected_costume}")
print(f"Studio Note: {selected_prop}")

# 3. THE PRODUCTION ENGINE (Executing the Face Swap)
fal_key = os.getenv("FAL_KEY")

if fal_key:
    try:
        # STEP A: Generate the high-fidelity base studio shot
        req_base = urllib.request.Request(
            "https://fal.run/fal-ai/fast-lightning-sdxl",
            data=json.dumps({"prompt": prompt}).encode("utf-8"),
            headers={"Authorization": f"Key {fal_key}", "Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req_base) as response:
            result_base = json.loads(response.read().decode("utf-8"))
            generic_image_url = result_base.get("images", [{}])[0].get("url")
            print(f"Base Studio Shot Created: {generic_image_url}")

        # STEP B: Map your real face (face_ref.jpg) onto the base shot
        # This ensures 100% likeness consistency for 'The Vitt Wire'
        if os.path.exists("face_ref.jpg"):
            with open("face_ref.jpg", "rb") as f:
                face_data = f.read()

            req_swap = urllib.request.Request(
                "https://fal.run/fal-ai/face-swap",
                data=json.dumps({
                    "base_image_url": generic_image_url,
                    "swap_image_base64": base64.b64encode(face_data).decode("utf-8")
                }).encode("utf-8"),
                headers={"Authorization": f"Key {fal_key}", "Content-Type": "application/json"}
            )
            
            with urllib.request.urlopen(req_swap) as response_swap:
                result_swap = json.loads(response_swap.read().decode("utf-8"))
                final_image_url = result_swap.get("image", {}).get("url")
                print(f"IMAGE_READY: {final_image_url}")
        else:
            print("Production Error: 'face_ref.jpg' missing. Upload your blueprint to GitHub.")

    except Exception as e:
        print(f"Production Error: {e}")
else:
    print("Security Alert: FAL_KEY not found in environment.")
