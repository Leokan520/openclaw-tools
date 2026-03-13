#!/usr/bin/env python3
"""自动剪辑视频 - MoviePy版"""

from moviepy import VideoFileClip, concatenate_videoclips
import os

INPUT_DIR = r"D:\video\pexels"
OUTPUT_DIR = r"D:\video\output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def auto_concat():
    """自动拼接素材"""
    
    # 找所有处理好的素材
    clips = []
    for f in os.listdir(INPUT_DIR):
        if f.startswith("c") and f.endswith(".mp4"):
            path = os.path.join(INPUT_DIR, f)
            print(f"添加: {f}")
            clip = VideoFileClip(path)
            clips.append(clip)
    
    if not clips:
        print("没有找到素材!")
        return
    
    # 拼接
    print(f"拼接 {len(clips)} 个视频...")
    final = concatenate_videoclips(clips, method="compose")
    
    # 输出
    output_path = os.path.join(OUTPUT_DIR, "auto_concat.mp4")
    final.write_videofile(output_path, fps=30, codec="libx264")
    print(f"完成: {output_path}")

if __name__ == "__main__":
    auto_concat()
