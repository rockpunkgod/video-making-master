---
name: ae-procedural-motion
description: 在 After Effects 中制作可编辑的三维轮廓隧道、延迟重复与程序化图形阵列，使用主控层、valueAtTime 和可参数化形状或素材。
---

# AE 程序化延迟阵列

0.3.0已在中文Windows AE26.0x67验证课程原法：相对controls的index、逐层Opacity/Trim Paths、单节点摄影机、原生Easy Ease In；通过基线、2→5帧变参、三种原创PNG输入、原生编辑恢复重开及独立目录执行。用户确认基线“整体符合课程效果”。按调用方registry和本目录tests/course-results.json核对范围。

先读references/course-stage.md。当前课程配置固定1080方形、30fps、7秒；PNG只支持opacity阶段，不提供Trim Paths或移动摄影机。其他画幅/时长及build.py/template.jsx的自主曲线/Order变体不在0.3.0课程验收范围。录屏播放时码的精确逐帧对齐仍未确认，不将其写成通过。

第7节扩展scripts/build_course_noise.py仍为candidate，需先用build_course_stage.py实际生成trim-final AEP，再以--base指定该工程、--out指定全新目录。它读取基线表达式，另存黑白杂色隧道，不覆盖基线；本机枚举Strings=19、Block=1经界面核对。实际制作记录见references/course-noise.md，不能将此分支称为0.3.0已验能力。

第11节扩展scripts/build_algorithmic_spiral.py为candidate静态三维布局，不属于上述verified动画范围。需要算法空间排列时先读references/algorithmic-layout.md及examples/algorithmic-layout-profiles.json；使用同目录run_ae.py/render_ae.py。已有圆形基线、变参和三组PNG真实制作，时间轴动画尚未确认，不能用5秒静态视频冒充动画验收。

1. 读取 [参数与制作原理](references/technique.md) 和 [来源证据](references/sources.md)。区分实测、视频明确展示与自行设计。
2. 按examples/course-profiles.json选择stage、delay_frames及可选PNG。trim-final是课程最终矢量效果；trim-linear是修改时长前的阶段；opacity是早期阶段/PNG泛化。新素材由调用者提供，复制进新输出目录。
3. 运行scripts/build_course_stage.py --stage trim-final --out全新目录，再以scripts/run_ae.py调用目标AfterFX。只接受真实AEP及成功回执。英文Slider/Color显示名在中文宿主以同参数(1)寻址；不改课程公式。最终阶段调用已实测“缓入”命令2510，命令不符则停止，不自行换曲线。
4. 用本目录scripts/render_ae.py和目标aerender原生渲染。回执需已保存重开、逐帧表达式通过，且实际修改/恢复Time offset成功。按宿主真实输出模板工作。
5. scripts/validate_video.py检查完整解码、帧数、画幅、时长与运动存在性；按tests/protocol.md另查来源画面、素材与原生参数。技术检查不替代视觉验收，新成片视觉状态单独记录。
6. 搬移本目录即可携带构建、执行、渲染和验证脚本；AE、aerender和FFmpeg由调用端提供。PNG工程连同输出assets一起保留，跨机器需重建绝对路径。

诊断：无回执先检查启动对话框和 reports 环境记录；表达式失败检查二维/三维向量、matchName、属性组失效和主控名称。切勿删除用户偏好或修改许可证来绕过启动问题。
