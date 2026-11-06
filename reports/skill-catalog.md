# 当前技能目录

按用户追加的严格课程标准，当前1个verified、3个candidate。课程原法、暂停参考、参数、原生制作/泛化和用户视觉验收分别记录，录屏精确播放时码不冒充通过。总体课程任务未完成。

|技能|版本/状态|已测能力|使用入口与证据|
|---|---|---|---|
|ae-procedural-motion|0.3.0 verified，限课程配置与PNG分支|原法Opacity/Trim Paths/摄影机/缓入，变参、三素材、编辑重开、独立复制、用户效果验收|skills/after-effects/ae-procedural-motion/SKILL.md；evaluations/course-p06-final-001/summary.json|
|ae-camera-tracking|0.2.0 candidate，课程复核中|三种合成场景技术测试已过；课程完整参考增强/地面/网格/归一化/Alpha流程待复刻|skills/after-effects/ae-camera-tracking/SKILL.md；evaluations/tracking-verified.json|
|pr-cinematic-sound|0.1.0 candidate|三组八轨、编辑重开导出、全帧素材对照和复制目录运行已过；课程叙事与完整效果链待复刻|skills/premiere-pro/pr-cinematic-sound/SKILL.md；evaluations/pr-sound-suite-002/summary.json|
|ae-advanced-expressions|0.3.0 candidate|第8节阈值显隐、第9节三维随机布局/X漂移、第10节循环数字序列均有真实工程/视频、变参和重开测试；第10节3配置不冒充3外部素材，排版待反馈，PNG前景可读性限制保留|skills/after-effects/ae-advanced-expressions/SKILL.md；registry的evidence_by_unit指向各单元原生、像素及反馈证据|

跟踪最终演示和工程：

- 房间几何：samples/tracking-fixture-001/solve-calibrated-001/composite-001/
- 房间文字变参：samples/tracking-fixture-001/solve-calibrated-001/composite-typography/
- 画廊纹理：samples/tracking-gallery-001/solve-001/composite-pixel-sized/
- 走廊文字：samples/tracking-corridor-001/solve-calibrated-001/composite-pixel-sized/

各目录有project.aep与final.mp4，迁移需保留输入原片与贴图。复制技能独立调用的实际新输出在samples/tracking-gallery-001/solve-001/bundle-reuse-001/。

尚未实现的方向以registry.json的research_queue为准，包括通用高级表达式系统、电影摄像机/摄影机投影、Mocha、动态文字、高级合成、叙事剪辑、调色。相关课程覆盖只有局部，不能按技能名称认定已具备制作能力。

PR已有samples/pr-sound-suite-002/{baseline,variation,reveal}/project.prproj与final.mp4。候选技能保留自制泛化实验，下一步优先完成明确课程片段的制作流程和效果对照。剩余课程按内容融合，不追求每个视频生成一个技能。

第16节噪波调色新增4秒可编辑组件基线与发光变化版：原生Colorama→Glow，96帧解码及7原生PNG、每帧淡出和编辑重开恢复通过。仅组件技术检查，前段空黑、近似相机和未完成总装仍待处理，未通过课程视觉验收，ae-advanced-compositing0.1.6为candidate。详见evaluations/course-p16-noise-style-001/summary.json。
