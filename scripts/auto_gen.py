#!/usr/bin/env python3
"""自动生成短视频 - 非交互版本"""

import requests
import os

PEXELS_KEY = "RuMVXWENzbZTZFDZzH3l7XhG3p3bfSXbgh02PSWCx9O7yGqKJzPPycFF"
OUTPUT_DIR = r"D:\video\auto"
os.makedirs(OUTPUT_DIR, exist_ok=True)

headers = {"Authorization": PEXELS_KEY}

# 情感主题素材
keywords = [
    "dark city rain",
    "lonely person walking", 
    "shadow silhouette",
    "foggy street",
    "night city timelapse"
]

print("=== 自动生成视频素材 ===")

for kw in keywords:
    print(f"\n搜索: {kw}")
    
    resp = requests.get(
        "https://api.pexels.com/videos/search",
        headers=headers,
        params={"query": kw, "per_page": 2, "orientation": "portrait"}
    )
    data = resp.json()
    
    count = 0
    for v in data.get("videos", [])[:2]:
        for f in v.get("video_files", []):
            if f.get("width", 0) >= 720:
                url = f["link"]
                safe_kw = kw.replace(" ", "_")
                filename = f"auto_{safe_kw}_{v['id']}.mp4"
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                print(f"  下载: {filename}...")
                
                r = requests.get(url, timeout=120, stream=True)
                with open(filepath, "wb") as fp:
                    for chunk in r.iter_content(8192):
                        fp.write(chunk)
                
                size = os.path.getsize(filepath) / 1024 / 1024
                print(f"  完成! {size:.1f}MB")
                count += 1
                break
    
    if count == 0:
        print(f"  没找到合适素材")

print(f"\n=== 完成! 素材保存在 {OUTPUT_DIR} ===")
