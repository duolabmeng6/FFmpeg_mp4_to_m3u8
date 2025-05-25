# MP4 转 M3U8 FFmpeg 命令生成器

这是一个基于 Streamlit 开发的 Web 应用程序，用于生成将 MP4 视频转换为 HLS (M3U8) 格式的 FFmpeg 命令。该工具提供了直观的用户界面，让用户可以轻松配置转换参数，无需记忆复杂的 FFmpeg 命令行参数。

在线使用 https://mp4tom3u8.streamlit.app/

## 🌟 主要特性

- 📹 支持多种视频编码选项：
  - 直接复制（无重编码）
  - H.264 软件编码 (CPU)
  - NVIDIA GPU 加速编码 (NVENC)
  - Intel 核显加速编码 (QSV)
  - Mac 硬件加速编码 (VideoToolbox)

- 🎵 灵活的音频处理：
  - 支持直接复制或 AAC 重编码
  - 可调节音频码率（64k-192k）

- 🔒 内容保护：
  - 支持 AES-128 加密
  - 可配置密钥轮换周期
  - 自动生成密钥文件

- 🎛️ 自定义转换参数：
  - 可选输出分辨率（360p 至 4K）
  - 可调节视频码率
  - 自定义分片时长
  - 灵活的输出目录配置

## 📋 系统要求

- Python 3.7 或更高版本
- FFmpeg（需要预先安装）
- 操作系统：Windows/macOS/Linux

## 🚀 安装步骤

1. 克隆仓库：
```bash
git clone [仓库地址]
cd mp4_to_m3u8
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 确保已安装 FFmpeg：
```bash
# macOS (使用 Homebrew)
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# 请从 FFmpeg 官网下载并添加到系统环境变量
```

## 💻 使用方法

1. 启动应用：
```bash
streamlit run main2.py
```

2. 在浏览器中打开显示的地址（通常是 http://localhost:8501）

3. 在界面中配置转换参数：
   - 设置输入文件路径和输出目录
   - 选择视频和音频编码选项
   - 配置分辨率和码率
   - 设置分片参数和加密选项

4. 复制生成的 FFmpeg 命令并在终端中执行

## 📝 注意事项

- 使用硬件加速编码时，请确保系统支持相应的编码器
- 启用加密功能时，请妥善保管生成的密钥文件
- 建议使用 HTTPS 服务器托管密钥文件
- 输出目录会自动创建（如果不存在）

## 🔧 常见问题

1. **如何选择合适的编码器？**
   - 如果原视频已是 H.264 编码，可以使用"直接复制"模式
   - 有 NVIDIA 显卡的用户建议使用 NVENC
   - Mac 用户可以使用 VideoToolbox 获得硬件加速
   - 其他情况下使用 libx264 最稳定

2. **如何选择合适的码率？**
   - 4K (2160p): 12-30 Mbps
   - 2K (1440p): 6-15 Mbps
   - 1080p: 3-8 Mbps
   - 720p: 2-4 Mbps
   - 480p: 1-2.5 Mbps
   - 360p: 0.5-1.5 Mbps

## �� 许可证

MIT License 
