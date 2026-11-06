# 第15节径向轮廓背景：候选分支

来源与参数证据见本项目sources/learning-notes/BV1Yh4y1A7XT-p15.md；独立使用本Skill时保留本页即足够执行。来源https://www.bilibili.com/video/BV1Yh4y1A7XT/?p=15，00:57–05:33。

1920×1080/24fps/10秒/16bpc。Fractal Noise Basic、Soft Linear、400/-100/Complexity6 → 演化速度25控制器（Evolution=`time*effect("evolution_speed")(1)`）→ CC Radial Fast Blur中心960/540、100、Brightest → Unsharp Mask300/1/0 → Find Edges反转、混合0 → Curves独立RGB通道多点调色。

assets/course-p15-radial-template.aep是本实验在AE中独立制作的原生模板，不是教程工程、厂商预设或视频截帧。红/绿/蓝曲线按04:55图形视觉重建，数值不是课程明确显示；原生CUSTOM_VALUE在本机脚本中不可读写，保存模板使未来调用不必重复GUI点击。颜色与原片精确匹配仍待复核。不要删除Curves或换成其他着色方法后声称课程原法。

执行：`scripts/build_radial.py --out 全新目录`；然后用本Skill的run_ae.py执行输出build.jsx，再用render_ae.py渲染。示例默认examples/course-radial.json；可选--speed、--seed、--duration，均记录为变体。模板SHA不同即拒绝；导入后清空继承队列，只渲染新合成，复制输入模板到交付inputs中。

限制：当前只支持固定1920×1080/24fps的程序噪波背景，允许1–20秒、速度1–150、种子0–10000；仅部分配置做过真实原生测试。随机种子变化不是跨素材测试；没有验证三组新素材，也未完成第15节总装，所以保持candidate。调用者若要求真实照片/Logo/视频输入，不得静默换成程序噪波。

诊断：Zoom本机1=Standard、2=Brightest，2已由真实界面核对。错误枚举会显著降低射线轮廓。Curves未着色时应回到原生模板并核SHA；脚本读取CUSTOM_VALUE失败不能填造曲线JSON。重开/关键控制器改写失败就停止交付。原生saveFrameToPng循环曾只产生首张PNG、原因未证实，逐张验证文件存在，不能只信回执。程序渲染全帧通过仍不能替代主观课程对照。
