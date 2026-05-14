import os, requests, time

# Verified Keys
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
IG_USER_ID = "17841425798197564"

def start_engine(video_file, caption):
    # Step 1: Create Public Bridge
    print("Uploading to bridge for Meta Fetch...")
    with open(video_file, 'rb') as f:
        public_url = requests.post('https://file.io', files={'file': f}).json()['link']
    
    # Step 2: Create Media Container
    print("Sending fetch command to Meta...")
    url = f"https://graph.facebook.com/v22.0/{IG_USER_ID}/media"
    payload = {'media_type': 'REELS', 'video_url': public_url, 'caption': caption, 'access_token': ACCESS_TOKEN}
    res = requests.post(url, data=payload).json()
    creation_id = res.get('id')
    
    if not creation_id:
        print(f"FAILED: {res}")
        return

    # Step 3: Wait for Processing
    print("Meta is processing... Waiting 50s.")
    time.sleep(50)

    # Step 4: Final Publish
    publish_url = f"https://graph.facebook.com/v22.0/{IG_USER_ID}/media_publish"
    final = requests.post(publish_url, data={'creation_id': creation_id, 'access_token': ACCESS_TOKEN}).json()
    print(f"Broadcast Live! Post ID: {final.get('id')}")

if __name__ == "__main__":
    if os.path.exists("meta.txt"):
        with open("meta.txt", "r") as f:
            v_name, v_cap = f.read().split("|")
            start_engine(v_name, v_cap)
