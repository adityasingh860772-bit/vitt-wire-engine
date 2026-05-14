import os, requests, time

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
IG_USER_ID = "17841425798197564"

def start_engine(video_file, caption):
    print("--- Phase 6: Uploading to Catbox Bridge ---")
    with open(video_file, 'rb') as f:
        public_url = requests.post('https://catbox.moe/user/api.php', data={'reqtype': 'fileupload'}, files={'fileToUpload': f}).text.strip()
    
    print(f"Meta Fetch Link: {public_url}")
    
    url = f"https://graph.facebook.com/v22.0/{IG_USER_ID}/media"
    payload = {'media_type': 'REELS', 'video_url': public_url, 'caption': caption, 'access_token': ACCESS_TOKEN}
    res = requests.post(url, data=payload).json()
    c_id = res.get('id')
    
    if not c_id:
        print(f"Meta Container Failed: {res}")
        return

    print("Meta is rendering the Reel... Waiting 60s.")
    time.sleep(60)

    pub_url = f"https://graph.facebook.com/v22.0/{IG_USER_ID}/media_publish"
    final = requests.post(pub_url, data={'creation_id': c_id, 'access_token': ACCESS_TOKEN}).json()
    
    if final.get('id'):
        print(f"BROADCAST LIVE ON INSTAGRAM! ID: {final.get('id')}")
    else:
        print(f"Publishing Failed: {final}")

if __name__ == "__main__":
    if os.path.exists("meta.txt"):
        with open("meta.txt", "r") as f:
            v, c = f.read().split("|")
            start_engine(v, c)
