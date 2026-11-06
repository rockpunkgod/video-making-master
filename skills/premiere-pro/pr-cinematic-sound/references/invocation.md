# 独立调用

本目录的scripts已独立复制并从实验室外工作目录实际调用。所有文件参数使用调用者明确指定的绝对路径；无需导入实验室tools。运行环境为现有Python/NumPy、FFmpeg、AE26和PR26，脚本不安装软件。

调用者先按课程片段提取事件、轨道、包络、效果与顺序，再准备plan.json。当前可执行部分是八轨剪辑与音量包络；没有实现的原生效果器保持缺失，不能用这个入口声称完整课程效果链已复刻。plan中的audio_clips需要path、track（0—7）、start、duration、source_in=0、role和gain_keys（源秒、线性幅度）。所有输入为48kHz立体声，画面源入点当前仅验证0。picture_clips给出path、start、duration、in=0；另提供width、height、fps、duration、audio_sample_rate=48000、native_unity_parameter=0.17782793939114及cuts。

顺序调用各脚本的--help取得参数：

1. prepare_pr_sound_plan.py：读取调用者计划，复制所引用媒体到新目录，并从调用者本机原生sequence-base派生八轨序列预设。
2. build_pr_sound_case.py：指定该目录、empty-project、export-preset、audio-preset，生成已审查的原生JSX。构建会拒绝已有工程/脚本，保护旧结果。
3. start_pr_and_run.py：指定JSX、pr、ae、当前预期project及全新out回执目录。已有PR保留，路径不符则停止；无PR时仅打开指定自有工程。原生执行完成才算制作成功。
4. mux_pr_sound.py：以真实原生画面和WAV封装final.mp4；原生工程保留全部独立音轨与关键帧。
5. validate_pr_sound.py和validate_pr_picture.py：分别核对声音和全部画面。后者适用于当前未经额外视觉处理的顺序剪辑，不直接套用于调色、缩放或转场后的成片。
6. prepare_pr_sound_edit_audit.py：指定case、全新out、audio-preset，生成副本音乐减半审计JSX；通过同一受保护原生通道执行，再用validate_pr_sound_edit.py核对实际WAV差异。

时间、长度和媒体需要在制作前核对。当前编译器仍仅验证实验用短片，复杂长片、非零源入点、单声道、额外视频效果和其他版本保持未验证。程序不会把候选能力自动升级verified。
