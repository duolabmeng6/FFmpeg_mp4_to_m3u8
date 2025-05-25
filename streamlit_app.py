import streamlit as st
import os

def main():
    st.set_page_config(
        page_title="MP4转M3U8 FFmpeg命令生成器",
        page_icon="🎬",
        layout="wide"
    )
    
    st.title("🎬 MP4转M3U8 FFmpeg命令生成器")
    st.markdown("---")
    
    # 文件设置
    st.header("📁 文件设置")
    col1, col2 = st.columns(2)
    with col1:
        input_file = st.text_input(
            "输入文件路径",
            value="input.mp4",
            help="要转换的MP4视频文件路径",
            key="input_file"
        )
    with col2:
        output_dir = st.text_input(
            "输出目录",
            value="output",
            help="M3U8文件和分片的输出目录",
            key="output_dir"
        )
        output_name = st.text_input(
            "输出文件名",
            value="playlist",
            help="输出的M3U8播放列表文件名（不含扩展名）",
            key="output_name"
        )

    # 编码设置
    st.header("🎯 编码设置")
    col1, col2 = st.columns(2)
    
    # 视频设置
    with col1:
        st.subheader("📹 视频设置")
        video_encoder = st.selectbox(
            "视频编码器",
            options=[
                "copy",
                "libx264",
                "h264_nvenc",
                "h264_qsv",
                "h264_videotoolbox"
            ],
            index=0,
            help="""
            选择视频处理方式：
            * 直接复制：不对视频进行重新编码，保持原始质量，速度最快
            * H.264软件编码：使用CPU进行编码，兼容性最好，但速度较慢
            * NVIDIA硬件加速：使用NVIDIA显卡加速编码，需要N卡
            * Intel硬件加速：使用Intel核显加速编码，需要Intel CPU
            * Mac硬件加速：使用Mac系统硬件加速，仅支持Mac
            """,
            key="video_encoder",
            format_func=lambda x: {
                "copy": "直接复制 (保持原始视频流，不重新编码)",
                "libx264": "H.264软件编码 (CPU编码，兼容性最好)",
                "h264_nvenc": "H.264 NVIDIA硬件加速 (N卡加速)",
                "h264_qsv": "H.264 Intel硬件加速 (Intel核显加速)",
                "h264_videotoolbox": "H.264 Mac硬件加速 (Mac系统加速)"
            }[x]
        )

        # 添加编码器说明
        if video_encoder == "copy":
            st.info("""
            ℹ️ 您选择了直接复制模式：
            * 不会重新编码视频，保持原始视频质量
            * 转换速度最快，不会占用CPU/GPU
            * 适用于：原视频已经是H.264编码，只需要切片
            * 注意：如果原视频编码不兼容，可能需要选择重新编码
            """)
        else:
            st.info("""
            ℹ️ 您选择了重新编码模式：
            * 会对视频进行重新编码，可以调整分辨率和码率
            * 转换时间取决于视频大小和编码设置
            * 适用于：需要调整视频质量或确保兼容性
            * 建议：优先选择硬件加速，可大幅提升转换速度
            """)

        if video_encoder != "copy":
            resolution = st.selectbox(
                "分辨率",
                options=[
                    "原始分辨率",
                    "3840x2160",
                    "2560x1440",
                    "1920x1080",
                    "1280x720", 
                    "854x480",
                    "640x360"
                ],
                index=0,
                help="输出视频分辨率",
                key="resolution",
                format_func=lambda x: {
                    "原始分辨率": "保持原始分辨率",
                    "3840x2160": "4K",
                    "2560x1440": "2K",
                    "1920x1080": "1080p",
                    "1280x720": "720p",
                    "854x480": "480p",
                    "640x360": "360p"
                }[x]
            )

            # 根据分辨率设置码率选项
            bitrate_settings = {
                "3840x2160": {
                    "options": ["30000k", "20000k", "15000k", "12000k"],
                    "help": "4K视频推荐码率：12-30 Mbps"
                },
                "2560x1440": {
                    "options": ["15000k", "12000k", "9000k", "6000k"],
                    "help": "2K视频推荐码率：6-15 Mbps"
                },
                "1920x1080": {
                    "options": ["8000k", "6000k", "4500k", "3000k"],
                    "help": "1080p视频推荐码率：3-8 Mbps"
                },
                "1280x720": {
                    "options": ["4000k", "3000k", "2500k", "2000k"],
                    "help": "720p视频推荐码率：2-4 Mbps"
                },
                "854x480": {
                    "options": ["2500k", "2000k", "1500k", "1000k"],
                    "help": "480p视频推荐码率：1-2.5 Mbps"
                },
                "640x360": {
                    "options": ["1500k", "1000k", "800k", "500k"],
                    "help": "360p视频推荐码率：0.5-1.5 Mbps"
                },
                "原始分辨率": {
                    "options": ["8000k", "6000k", "4000k", "2000k"],
                    "help": "请根据实际分辨率选择合适的码率"
                }
            }

            video_bitrate = st.selectbox(
                "视频码率",
                options=bitrate_settings[resolution]["options"],
                index=1,
                help=bitrate_settings[resolution]["help"],
                key="video_bitrate"
            )
            st.info(f"当前视频设置：{resolution} @ {video_bitrate}/s")

    # 音频设置
    with col2:
        st.subheader("🔊 音频设置")
        audio_encoder = st.selectbox(
            "音频编码器",
            options=["copy", "aac"],
            index=0,
            help="""
            选择音频处理方式：
            * 直接复制：不对音频进行重新编码，保持原始音质
            * AAC编码：使用AAC编码器重新编码，可调整码率
            
            说明：
            * 直接复制模式：速度最快，无音质损失
            * AAC编码模式：可以压缩音频，减小文件体积
            * AAC编码广泛支持：iOS、Android、Web浏览器都能很好支持
            """,
            key="audio_encoder",
            format_func=lambda x: {
                "copy": "直接复制 (保持原始音频流，不重新编码)",
                "aac": "AAC编码 (通用格式，可调整音质)"
            }[x]
        )

        # 添加音频编码器说明
        if audio_encoder == "copy":
            st.info("""
            ℹ️ 您选择了音频直接复制模式：
            * 不会重新编码音频，保持原始音质
            * 转换速度最快，不会占用额外资源
            * 适用于：原音频质量合适，只需要切片
            * 注意：如果原音频编码不兼容，可能需要选择AAC编码
            """)
        else:
            st.info("""
            ℹ️ 您选择了AAC音频编码：
            * 会对音频进行重新编码，可以调整码率
            * AAC是目前最通用的音频编码格式
            * 建议码率：
                - 192k：适合高质量音乐
                - 128k：适合标准音质
                - 96k：适合中等音质
                - 64k：适合语音质量
                
            * 更高码率 = 更好音质，但文件更大
            """)

        if audio_encoder != "copy":
            audio_bitrate = st.selectbox(
                "音频码率",
                options=["192k", "128k", "96k", "64k"],
                index=1,
                help="""
                选择音频码率：
                * 192k：高质量音乐
                * 128k：标准音质（推荐）
                * 96k：中等音质
                * 64k：语音质量
                
                说明：码率越高，音质越好，文件也越大
                """,
                key="audio_bitrate"
            )
            st.info(f"当前音频设置：{audio_encoder.upper()} @ {audio_bitrate}/s")

    # HLS设置
    st.header("📺 HLS设置")
    col1, col2 = st.columns(2)
    
    with col1:
        segment_time = st.slider(
            "分片时长(秒)",
            min_value=1,
            max_value=10,
            value=10,
            help="每个TS分片的时长，建议2-10秒",
            key="segment_time"
        )
        
        playlist_type = 'vod'

    with col2:
        encryption_enabled = st.checkbox(
            "启用加密",
            value=False,
            help="""
            是否启用HLS内容加密：
            * 使用AES-128加密算法保护视频内容
            * 加密后的视频需要密钥才能播放
            * 适用于需要内容保护的场景
            * 支持密钥轮换机制增强安全性
            
            说明：
            * 加密会自动生成密钥文件(enc.key)
            * 密钥信息文件(enc.keyinfo)包含密钥获取地址
            * 播放器需要能访问密钥文件才能播放
            * 建议将密钥文件部署在HTTPS服务器上
            """,
            key="encryption_enabled"
        )

        if encryption_enabled:
            key_rotation_period = st.number_input(
                "密钥轮换周期(分片数)",
                min_value=0,
                max_value=100,
                value=0,
                help="""
                设置密钥自动轮换的周期：
                * 0：禁用密钥轮换，使用固定密钥
                * 1-100：每隔指定数量的分片更换一次密钥
                
                说明：
                * 密钥轮换可以提高安全性
                * 轮换周期越短，安全性越高
                * 但过于频繁的轮换会增加服务器负载
                * 建议根据实际安全需求选择合适的周期
                """,
                key="key_rotation"
            )
            
            st.info("""
            ℹ️ 加密相关说明：
            * 启用加密后会在输出目录生成以下文件：
                - enc.key：加密密钥文件
                - enc.keyinfo：密钥信息文件
                - *.ts：加密后的视频分片
                - *.m3u8：包含密钥信息的播放列表
            
            * 部署注意事项：
                - 确保播放器能访问密钥文件
                - 建议使用HTTPS传输密钥
                - 可以通过访问控制限制密钥获取
                - 密钥文件请妥善保管
            """)

    # 命令生成
    st.header("🔧 生成的FFmpeg命令")
    
    # 构建FFmpeg命令
    command_parts = ["ffmpeg", "-y", "-i", f'\"{input_file}\"']
    
    # 视频编码参数
    command_parts.extend(["-c:v", video_encoder])
    if video_encoder != "copy":
        if resolution != "原始分辨率":
            command_parts.extend(["-s", resolution])
        command_parts.extend(["-b:v", video_bitrate])
        
        # 根据不同编码器添加特定参数
        if video_encoder == "libx264":
            command_parts.extend(["-preset", "fast"])
        elif "nvenc" in video_encoder:
            command_parts.extend([
                "-preset", "p4",
                "-rc", "cbr"
            ])
        elif "qsv" in video_encoder:
            command_parts.extend(["-preset", "medium"])
        elif "videotoolbox" in video_encoder:
            command_parts.extend(["-allow_sw", "1"])
    
    # 音频编码参数
    command_parts.extend(["-c:a", audio_encoder])
    if audio_encoder != "copy" and 'audio_bitrate' in locals():
        command_parts.extend(["-b:a", audio_bitrate])
    
    # HLS参数
    command_parts.extend([
        "-f", "hls",
        "-hls_time", str(segment_time),
        "-hls_playlist_type", playlist_type,
        "-hls_segment_filename", f'"{output_dir}/segment_%03d.ts"'
    ])
    
    # 加密参数
    if encryption_enabled:
        key_file = os.path.join(output_dir, "enc.key")
        key_info_file = os.path.join(output_dir, "enc.keyinfo")
        command_parts.extend([
            "-hls_key_info_file", f'"{key_info_file}"',
            "-hls_enc", "1"
        ])
        if key_rotation_period > 0:
            command_parts.extend(["-hls_key_rotation_period", str(key_rotation_period)])
    
    # 输出文件
    output_path = f"{output_dir}/{output_name}.m3u8"
    command_parts.append(f'"{output_path}"')
    
    # 显示命令
    ffmpeg_command = " ".join(command_parts)
    st.code(ffmpeg_command, language="bash")
    
    
    # 使用说明
    st.info("""
    **使用说明：**
    1. 复制上面生成的FFmpeg命令
    2. 在终端/命令行中运行该命令
    3. 确保输入文件存在且FFmpeg已正确安装
    4. 输出目录会自动创建（如果不存在）
    """)
    
    # 转换信息
    st.header("📊 转换信息")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("分片时长", f"{segment_time}秒")
        if video_encoder != "copy":
            st.metric("视频码率", video_bitrate)
            st.metric("分辨率", resolution)
        st.metric("视频编码器", video_encoder)
    with col2:
        st.metric("播放列表类型", playlist_type)
        if audio_encoder != "copy" and 'audio_bitrate' in locals():
            st.metric("音频码率", audio_bitrate)
        st.metric("音频编码器", audio_encoder)
        if encryption_enabled:
            st.metric("加密模式", "AES-128")


if __name__ == "__main__":
    main()

