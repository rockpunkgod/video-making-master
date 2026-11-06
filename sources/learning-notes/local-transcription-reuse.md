# 复用已有本地语音转录

用户最终选择本机已有工具，并明确不要重复安装。先前Watch设置命令因PATH缺少yt-dlp/Deno仅输出依赖检查提示，没有启动包或模型安装。

已确认现有Python环境：E:/自媒体/gpt-sovits-env/Scripts/python.exe；现有faster-whisper 1.2.1；完整small模型：E:/自媒体/GPT-SoVITS/tools/asr/models/faster-whisper-small，model.bin为483546902字节，配置、词表和tokenizer均存在。仅以只读方式复用，不修改这些目录。另发现voice-alternatives的Whisper环境、v3-audio-analysis的ggml-base模型及剪映安装，未调用或更改。

Watch现有fallback仅暴露WhisperX/云端接口，未假装其能直接调用此faster-whisper。tools/transcribe_existing_local.py是已有库的时间戳导出适配器，调用WhisperModel/transcribe原生能力，不实现新识别引擎。FFmpeg只提取本地16kHz单声道音频，CPU/int8运行，显式中文提示，local_files_only和离线环境标记，禁用需额外资源的VAD，不下载或上传。

来源BV1xP411C7u3：cache/watch/watch-igeyyb9t/download/run-29yfp3gc/video.mp4。先完成90–150秒试转，再完成全片0–520.6秒转录。原始结果分别在cache/local-transcripts/BV1xP411C7u3-pilot-001和BV1xP411C7u3-full-001，保留输入音频、transcript.json与transcript.srt，时码相对原视频。

状态：自动转录成功，准确率未验证。原始文本将Mocha Pro误识别为Mocaplode/Moccaflow，不能直接作为插件名或操作证据。原始转录不覆写；另建校注并对照可见界面。仅凭字幕不可确认不可见控件、网格参数或原生制作成功。Mocha Pro插件缺失的制作阻塞仍在。

此前Edge插件检查发现bilibili视频文稿助手2.0.6，它读取B站已有人工/AI字幕，没有内置语音识别。未将此插件的提取能力记成无字幕课程的转录能力；用户随后改为本机转录。
