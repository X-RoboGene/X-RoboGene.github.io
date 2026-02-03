import os
import subprocess

# --- 配置区 ---
# 视频源文件夹 (存放你的 .mov 或原视频)
input_folder = './static/videos/tga/' 
# 封面图存放路径
poster_folder = './static/images/posters/' 

if not os.path.exists(poster_folder):
    os.makedirs(poster_folder)

# 支持的格式
valid_extensions = ('.mov', '.mp4', '.MOV')

print("🚀 开始一键全自动处理（转码 + 压缩 + 封面）...")

for filename in os.listdir(input_folder):
    if filename.lower().endswith(valid_extensions):
        # 如果已经是转码后的文件，跳过，避免重复处理
        if filename.endswith('_web.mp4'): continue
        
        input_path = os.path.join(input_folder, filename)
        base_name = os.path.splitext(filename)[0]
        output_video = os.path.join(input_folder, f"{base_name}_web.mp4")
        output_poster = os.path.join(poster_folder, f"{base_name}.jpg")

        print(f"\n📦 正在处理: {filename}")

        # --- 步骤 1: 压缩并转码为 Web 友好格式 ---
        # -vcodec libx264: 使用 H.264 编码
        # -crf 23: 视觉无损压缩（23 是平衡点，数值越大体积越小，18-28 均可）
        # -preset faster: 转码速度
        # -pix_fmt yuv420p: 确保在所有浏览器（尤其是苹果）能播
        compress_cmd = [
            'ffmpeg', '-i', input_path,
            '-vcodec', 'libx264',
            '-crf', '23', 
            '-preset', 'faster',
            '-pix_fmt', 'yuv420p',
            '-y', output_video
        ]
        
        # --- 步骤 2: 提取封面图 ---
        poster_cmd = [
            'ffmpeg', '-i', input_path,
            '-ss', '00:00:00.500', 
            '-vframes', '1',
            '-y', output_poster
        ]

        try:
            # 执行转码
            subprocess.run(compress_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print(f"  ✅ 视频转码完成: {output_video}")
            
            # 执行截图
            subprocess.run(poster_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print(f"  ✅ 封面提取完成: {output_poster}")
            
        except subprocess.CalledProcessError as e:
            print(f"  ❌ 处理出错: {filename}, 错误信息: {e.stderr.decode()}")

print("\n✨ 全部任务已完成！")
print("⚠️ 提示：请记得在 HTML 中将视频文件名修改为带有 '_web.mp4' 后缀的文件名。")
