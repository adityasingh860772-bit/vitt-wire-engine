import random
import os
import urllib.request
import json

# 1. THE FIXED ANCHOR STUDIO
anchor_studio = "a premium, minimalist modern glass office in Mumbai with a clean white desk and a soft-focus city skyline in the background"

# 2. THE DYNAMIC PROPS (Subtle changes for authenticity)
props = [
    "a thin silver laptop positioned on the left side of the desk",
    "a stack of three leather-bound finance books on the right corner",
    "a silver laptop centered on the desk with a small coffee mug nearby",
    "a clean desk with just a black smartphone placed near the edge",
    "a tablet propped up on a stand next to a neat pile of documents"
]

# 3. THE VIRTUAL WARDROBE
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
prompt = f"Professional studio portrait of AdityaSinghAI wearing {selected_costume}. He is sitting at {anchor_studio}. On the desk, there is {selected_prop}. High-end broadcast lighting, thick professional studio-styled hair with excellent volume, 8k photorealistic."

print(f"Today's Look: {selected_costume}")
print(f"Studio Note: {selected_prop}")

# 4. THE RENDERING ENGINE (Connecting to your balance)
fal_key = os.getenv("FAL_KEY")

if fal_key:
    req = urllib.request.Request(
        "https://fal.run/fal-ai/fast-lightning-sdxl",
        data=json.dumps({"prompt": prompt}).encode("utf-8"),
        headers={"Authorization": f"Key {fal_key}", "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            image_url = result.get("images", [{}])[0].get("url")
            print(f"IMAGE_READY: {image_url}")
    except Exception as e:
        print(f"Production Error: {e}")
else:
    print("Security Alert: FAL_KEY not found.")
