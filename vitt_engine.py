import os, requests, time

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
IG_USER_ID = "17841425798197564"

def start_engine(video_file, caption):
    print("--- Phase 6: Uploading to Catbox Bridge ---")
    with open(video_file, 'rb') as f:
        public_url = requests.post('https://catbox.moe/user/api.php', data={'reqtype': 'fileupload'}, files={'fileToUpload': f}).text.strip()
    
    print(f"Meta Fetch Link: {public_url}")
    
    # Create Container
    url = f"https://graph.facebook.com/v22.0/{IG_USER_ID}/media"
    payload = {'media_type': 'REELS', 'video_url': public_url, 'caption': caption, 'access_token': ACCESS_TOKEN}
    res = requests.post(url, data=payload).json()
    c_id = res.get('id')
    
    if not c_id:
        print(f"Meta Container Creation Failed: {res}")
        return

    # THE MASTERMIND IMPROVEMENT: Polling Status
    print(f"Container ID: {c_id}. Waiting for Meta to finish rendering...")
    
    status_url = f"https://graph.facebook.com/v22.0/{c_id}"
    params = {'fields': 'status_code', 'access_token': ACCESS_TOKEN}
    
    for attempt in range(20): # Try for 10 minutes max
        check = requests.get(status_url, params=params).json()
        status = check.get('status_code')
        print(f"Current Status: {status}")
        
        if status == 'FINISHED':
            print("Video Finished Rendering. Publishing now!")
            break
        elif status == 'ERROR':
            print(f"Meta Rendering Error: {check}")
            return
        
        time.sleep(30) # Check every 30 seconds
    else:
        print("Timeout: Meta took too long to render.")
        return

    # Final Publish
    pub_url = f"https://graph.facebook.com/v22.0/{IG_USER_ID}/media_publish"
    final = requests.post(pub_url, data={'creation_id': c_id, 'access_token': ACCESS_TOKEN}).json()
    
    if final.get('id'):
        print(f"SUCCESS! THE VITT WIRE IS LIVE! Reel ID: {final.get('id')}")
    else:
        print(f"Publishing Failed at Final Step: {final}")

if __name__ == "__main__":
    if os.path.exists("meta.txt"):
        with open("meta.txt", "r") as f:
            content = f.read().split("|")
            if len(content) == 2:
                v, c = content
                start_engine(v, c)
