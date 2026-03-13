import requests
import os

PEXELS_KEY = "RuMVXWENzbZTZFDZzH3l7XhG3p3bfSXbgh02PSWCx9O7yGqKJzPPycFF"
OUTPUT_DIR = r"D:\video\story"
os.makedirs(OUTPUT_DIR, exist_ok=True)

headers = {"Authorization": PEXELS_KEY}

# 根据场景搜索
scenes = [
    ("morning_run", "morning running late person"),
    ("hospital", "hospital room interior"),
    ("garden", "garden park trees"),
    ("cat", "black cat mysterious"),
    ("crowd_chaos", "people running chaotic"),
]

for scene_id, kw in scenes:
    print(f"\n搜索: {kw}")
    
    resp = requests.get(
        "https://api.pexels.com/videos/search",
        headers=headers,
        params={"query": kw, "per_page": 2, "orientation": "portrait"}
    )
    data = resp.json()
    
    for v in data.get("videos", [])[:1]:
        for f in v.get("video_files", []):
            if f.get("width", 0) >= 720:
                url = f["link"]
                filename = f"{scene_id}.mp4"
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                print(f"  下载: {filename}...")
                
                r = requests.get(url, timeout=120, stream=True)
                with open(filepath, "wb") as fp:
                    for chunk in r.iter_content(8192):
                        fp.write(chunk)
                
                size = os.path.getsize(filepath) / 1024 / 1024
                print(f"  完成! {size:.1f}MB")
                break

print(f"\n=== 场景素材下载完成 ===")
print(f"保存在: {OUTPUT_DIR}")
