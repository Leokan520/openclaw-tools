import requests
import os

PEXELS_KEY = "RuMVXWENzbZTZFDZzH3l7XhG3p3bfSXbgh02PSWCx9O7yGqKJzPPycFF"

# 搜索多个主题的视频
themes = [
    "dark city rain",
    "lonely person walking", 
    "shadow silhouette",
    "foggy street",
    "night city timelapse"
]

headers = {"Authorization": PEXELS_KEY}
url = "https://api.pexels.com/videos/search"

all_videos = []

for theme in themes:
    params = {"query": theme, "per_page": 2, "orientation": "portrait"}
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()
    
    print(f"主题 '{theme}': 找到 {data.get('total_results', 0)} 个")
    
    for video in data.get("videos", []):
        # 找合适的下载链接
        for f in video.get("video_files", []):
            if f["width"] >= 720 and "mp4" in f.get("file_type", ""):
                all_videos.append({
                    "theme": theme,
                    "url": f["link"],
                    "duration": video["duration"]
                })
                break

print(f"\n共收集 {len(all_videos)} 个视频")

# 下载到本地
os.makedirs("D:\\video\\pexels", exist_ok=True)

for i, v in enumerate(all_videos):
    filename = f"D:\\video\\pexels\\clip_{i+1}_{v['theme'].replace(' ', '_')}.mp4"
    print(f"下载: {v['theme']} -> {filename}")
    
    r = requests.get(v["url"], timeout=120)
    with open(filename, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
    
    print(f"  完成! 大小: {len(r.content)/1024/1024:.1f}MB")

print("\n全部下载完成!")
