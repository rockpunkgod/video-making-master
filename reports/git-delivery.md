# Git交付范围

后续验收覆盖：005用户答“仍不符合课程动画”，也按失败保留。32组为原生制作历史数量，不是32组用户验收成功；第10节没有已认可动画。具体反馈见summary.current_animation_trial.human_visual_review。

用户指定发布到rockpunkgod/video-making-master。远端检查为空仓库，本项目仍以独立video-skills-lab运行，不引入或接入其他Video Making内部实现。

提交Skills源文件、来源与学习笔记、工具和验证记录，并保留32组代表性原生工程、视频及其必要的inputs/assets。精确文件、大小和SHA256见git-delivery-manifest.json。状态为当前进度快照：1个verified、3个candidate，全部18条来源/166章节学习目标尚未完成。ae-advanced-expressions0.3.2含第8/9/10节三个单元，第10节当前试验为p10-controls-animation-005：原生8秒控制器动画及逐帧更新检查通过，但关键帧为适配而非课程原有时间轴，尚待用户验收与泛化。先前002排版及003抖动被用户否决，已发布旧工程保留为历史；静态004也因不符合动画意图被否决，其工程留本机，不列当前演示。附课程原字体DM Sans Bold和OFL许可，仅在Windows当前会话注册，不捆绑字体安装器。

教程原片、教程抽帧、本机环境/语音模型、重复失败试验的原生大文件、Adobe自动保存、消息传输临时文件、从已安装Adobe导出的厂商预设不进入Git。本地原文件全部保留；历史报告中部分路径属于本机历史证据，不在本次Git分发范围。

工程保留可编辑图层和轨道，原始媒体路径为本机Windows路径。换机器优先按Skill说明用随附脚本重建；手动打开时重链接各案例的inputs/assets。依赖目标机器已有AE/PR、FFmpeg等，不打包Adobe安装文件或预设。PR CC0声音素材随案例credits.md保留署名和来源。
