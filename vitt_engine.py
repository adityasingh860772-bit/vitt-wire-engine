import os, requests, time

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
IG_USER_ID = "17841425798197564"

def upload_to_bridge(video_file):
    print("--- Phase 6: Uploading to Secure Bridge (tmpfiles) ---")
    try:
        with open(video_file, 'rb') as f:
            res = requests.post("https://tmpfiles.org/api/v1/upload", files={"file": f}).json()
            
        original_url = res['data']['url']
        direct_url = original_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
        return direct_url
    except Exception as e:
        print(f"Bridge Upload Failed: {e}")
        return None

def start_engine(video_file, caption):
    public_url = upload_to_bridge(video_file)
    
    if not public_url or "Invalid" in public_url:
        print("CRITICAL ERROR: Failed to get a valid public URL for the video.")
        return
    
    print(f"Meta Fetch Link: {public_url}")
    print(f"Caption to post: {caption}")
    
    url = f"https://graph.facebook.com/v22.0/{IG_USER_ID}/media"
    payload = {'media_type': 'REELS', 'video_url': public_url, 'caption': caption, 'access_token': ACCESS_TOKEN}
    res = requests.post(url, data=payload).json()
    c_id = res.get('id')
    
    if not c_id:
        print(f"Meta Container Failed: {res}")
        return

    print(f"Container ID: {c_id}. Waiting for Meta to finish rendering...")
    
    status_url = f"https://graph.facebook.com/v22.0/{c_id}"
    params = {'fields': 'status_code', 'access_token': ACCESS_TOKEN}
    
    for attempt in range(20): 
        check = requests.get(status_url, params=params).json()
        status = check.get('status_code')
        print(f"Current Status: {status}")
        
        if status == 'FINISHED':
            print("Video Finished Rendering. Publishing now!")
            break
        elif status == 'ERROR':
            print(f"Meta Rendering Error: {check}")
            return
        
        time.sleep(30)
    else:
        print("Timeout: Meta took too long to render.")
        return

    pub_url = f"https://graph.facebook.com/v22.0/{IG_USER_ID}/media_publish"
    final = requests.post(pub_url, data={'creation_id': c_id, 'access_token': ACCESS_TOKEN}).json()
    
    if final.get('id'):
        print(f"SUCCESS! THE VITT WIRE IS LIVE! Reel ID: {final.get('id')}")
    else:
        print(f"Publishing Failed at final step: {final}")

if __name__ == "__main__":
    if os.path.exists("meta.txt"):
        # MASTERMIND FIX: Safe reading with utf-8
        with open("meta.txt", "r", encoding="utf-8") as f:
            data = f.read()
            if "|" in data:
                parts = data.split("|", 1) # Splits only on the first pipe
                v = parts[0]
                c = parts[1]
                start_engine(v, c)
