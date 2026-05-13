import random

# 1. THE FIXED ANCHOR STUDIO (Signature Set)
anchor_studio = "a premium, minimalist modern glass office in Mumbai with a clean white desk and a soft-focus city skyline in the background"

# 2. THE DYNAMIC PROPS (Subtle changes for authenticity)
props = [
    "a thin silver laptop positioned on the left side of the desk",
    "a stack of three leather-bound finance books on the right corner",
    "a silver laptop centered on the desk with a small coffee mug nearby",
    "a clean desk with just a black smartphone placed near the edge",
    "a tablet propped up on a stand next to a neat pile of documents"
]

# 3. THE VIRTUAL WARDROBE (Rotating costumes)
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
# Maintains signature hair volume and broadcast lighting
prompt = f"Professional studio portrait of AdityaSinghAI wearing {selected_costume}. He is sitting at {anchor_studio}. On the desk, there is {selected_prop}. High-end broadcast lighting, thick professional studio-styled hair with excellent volume, 8k photorealistic."

print(f"Today's Look: {selected_costume}")
print(f"Studio Note: {selected_prop}")
