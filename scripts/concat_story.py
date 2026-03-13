from moviepy import VideoFileClip, concatenate_videoclips

clips = []
for f in [r'D:\video\story\garden.mp4', r'D:\video\story\hospital.mp4', r'D:\video\story\cat.mp4', r'D:\video\story\crowd.mp4']:
    print(f"处理: {f}")
    clip = VideoFileClip(f)
    # 统一分辨率
    clip = clip.resized((720, 1280))
    clips.append(clip)

print(f"拼接 {len(clips)} 个视频...")
final = concatenate_videoclips(clips, method="compose")
final.write_videofile(r"D:\video\output\story_v2.mp4", fps=30, codec="libx264")
print("完成!")
