# 第17节条带调色候选

执行scripts/build_streak_style.py --out全新目录，再用run_ae.py和render_ae.py。输入examples/course-streak-style.json引用自制P17隧道AEP和原生RGB Curves模板，均核对SHA；--glow-intensity为明确变体。无需课程视频、其他仓库或额外插件。输出可编辑project.aep、20秒final.mp4、请求/计划、原生回执、11个检查PNG与质量报告。

课程04:50、08:35先保留一个噪波层进行处理，再于08:37–08:38复制为7层（Camera/controls外另7层），不能把中途单层当最终。保留既有Position/Scale表达式与底值，不静默改成另一种噪波布局。内部FractalNoise→键白；Contrast2000、Width30、Height2270、Complexity1。外层Curves→Glow29.4%/30/5→Glow56.9%/111/1，Collapse开启，Position960/540/-19810（09:40）。不沿用早期Colorama或14层重复乘算。

ScaleX100→0，Y/Z100。主173→190帧按最终尺标估算；Easy Ease Out首键、影响33.333333是重建，源没有直接显示影响数值。不同帧的试验键位置不能合并成多段动画。

原生曲线CUSTOM_VALUE无法通过本机脚本直接设置控制点；实际GUI重建11:50最终三通道，再保存AEP和重开。控制点估读值见examples/course-streak-style-curves.json，不宣称原作者精确数值。调用复制原生图层并替换Source、移除Ramp，保留可编辑曲线，不用LUT或表达式替代课程效果器。

验证实际修改宽Glow Radius111→112、保存重开确认并恢复111。遍历480帧表达式、Scale单调及Y/Z不变；全帧解码与原生PNG同帧检查。技术通过不等于课程视觉通过；继承相机、随机图样、Mask估算和后段红线/标题未完成的限制仍在。

排错：三维Scale的TemporalEase必须提供三个维度数组；一维数组本机实际报错，不能忽略。GUI点击靠近另一通道的现有点会切换通道，应先在目标曲线上加点再拖动；保存后重开查看各通道。若对照宽度/密度不一致，先查是否恰好7个噪波层、外部白键或Colorama，再查摄影机和空间位置。
