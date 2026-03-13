#!/usr/bin/env python3
"""
自动生成短视频脚本
功能：文案 -> 素材 -> 合成 -> 视频
"""

import requests
import os
import json
from datetime import datetime

# 配置
PEXELS_KEY = "RuMVXWENzbZTZFDZzH3l7XhG3p3bfSXbgh02PSWCx9O7yGqKJzPPycFF"
OUTPUT_DIR = "D:\\video\\auto"

# 主题配置（可以扩展）
THEMES = {
    "情感": {
        "keywords": ["dark city rain", "lonely person walking", "shadow silhouette"],
        "color": "dark"
    },
    "励志": {
        "keywords": ["sunrise mountain", "running motivation", "city timelapse"],
        "color": "bright"
    },
    "夜景": {
        "keywords": ["night city", "neon lights", "rain city"],
        "color": "neon"
    }
}

class VideoGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {"Authorization": api_key}
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    def search_videos(self, keyword, per_page=3):
        """搜索视频素材"""
        url = "https://api.pexels.com/videos/search"
        params = {"query": keyword, "per_page": per_page, "orientation": "portrait"}
        
        resp = requests.get(url, headers=self.headers, params=params)
        data = resp.json()
        
        videos = []
        for v in data.get("videos", []):
            # 找合适的下载链接
            for f in v.get("video_files", []):
                if f.get("width", 0) >= 720:
                    videos.append({
                        "url": f["link"],
                        "duration": v["duration"],
                        "id": v["id"]
                    })
                    break
        return videos
    
    def download_video(self, url, filename):
        """下载视频"""
        print(f"下载: {filename}...")
        resp = requests.get(url, timeout=120, stream=True)
        
        path = os.path.join(OUTPUT_DIR, filename)
        with open(path, "wb") as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
        print(f"完成: {path}")
        return path
    
    def generate_from_theme(self, theme_name):
        """根据主题生成视频"""
        if theme_name not in THEMES:
            print(f"未知主题: {theme_name}")
            print(f"可用主题: {list(THEMES.keys())}")
            return
        
        theme = THEMES[theme_name]
        print(f"\n=== 生成主题: {theme_name} ===")
        
        all_clips = []
        
        # 搜索素材
        for kw in theme["keywords"]:
            print(f"\n搜索: {kw}")
            videos = self.search_videos(kw, per_page=2)
            for i, v in enumerate(videos):
                filename = f"{theme_name}_{kw.replace(' ', '_')}_{v['id']}.mp4"
                path = self.download_video(v["url"], filename)
                all_clips.append(path)
        
        print(f"\n共下载 {len(all_clips)} 个素材")
        return all_clips

def main():
    gen = VideoGenerator(PEXELS_KEY)
    
    # 选择主题
    print("可用主题:", list(THEMES.keys()))
    theme = input("选择主题: ").strip()
    
    # 生成
    clips = gen.generate_from_theme(theme)
    
    if clips:
        print(f"\n素材已保存到: {OUTPUT_DIR}")
        print("下一步：用 FFmpeg 拼接")

if __name__ == "__main__":
    main()
