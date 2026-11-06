---
name: pr-cinematic-sound
description: 在Premiere中编排独立对白、音乐、环境和事件轨，制作闪避、淡化及转场包络；当前candidate，三组技术测试已通过，课程叙事和完整效果链基础复刻尚未完成。
---

# 多轨声音编排

当前0.1.0 candidate。三组suite002通过八轨原生制作、保存重开后渲染、实际音量编辑导出、独立混音和全帧素材对照，并已从复制目录运行。它们是自主泛化测试，不能替代课程基础复刻。用户仅认可旧suite001柔和基线的听感，新文件未试听。先按课程指定片段逐项复现叙事事件、声音分层、包络和效果链，再以泛化结果补充验证。

1. 阅读[原生工作流](references/workflow.md)、[教程证据](references/sources.md)和[参数例子](examples/case.json)。从叙事事件、对白窗口及镜头边界制定计划；素材应原创或有适当许可。
2. 保留对白、音乐、环境、拟音、上升音、冲击音等独立轨道。底床不是必须满铺；先确认是否需要，再决定频段和音量。不要把合成噪声等同于真实环境。
3. 按references/invocation.md调用本技能scripts中的prepare_pr_sound_plan.py、build_pr_sound_case.py、start_pr_and_run.py；通过Adobe BridgeTalk和可用AE宿主执行。严格核对PR当前工程，不使用最近项目和未验证的QE接口。
4. 原生插入会取整到画面帧；随后显式设置Time起止点、源出点，并读回至一个音频采样以内。关键帧以已校准源时间为基准。当前仅验证source_in=0的立体声输入。
5. 保存原生工程，导出PR的H.264画面和WAV混音。因本机H.264/AAC导出实测有1024采样延迟，用FFmpeg封装原生画面与原生WAV。独立数值参考混音只能用于检查，不能冒充PR输出。
6. 用scripts/validate_pr_sound.py比较独立PCM参考，scripts/validate_pr_picture.py逐帧对照原始画面，不能只检查视频可解码。用prepare_pr_sound_edit_audit.py和validate_pr_sound_edit.py验证修改保存后的实际输出，再做独立听感和画面审查。Media pending占位图按references/workflow.md修复，保留失败记录。

当前需要AE26.0和PR26.0、FFmpeg、Python/NumPy。本目录已携带调用脚本，不依赖实验室tools或其他视频仓库。调用端提供媒体、空白PR工程及本机Adobe预设路径；不分发厂商预设。详细证据与缺口见tests/results.json。
