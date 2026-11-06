# 16 Stylization and Art Direction 1

来源：https://www.bilibili.com/video/BV1Yh4y1A7XT/?p=16 ，19分49秒。Watch实际下载720p含音轨，另用已有yt-dlp取1080p视频；复用已安装faster-whisper-small，本机离线转录完整1188.767秒并通读。实际查看24个全局帧及25个前半节1080p技术帧。转录不是视觉操作证据；后半节只有全局理解，具体数值还未逐项提取。

00:26–02:15：把第11节圆点基础形状改为无Fill、Stroke22；Gradient Ramp起点150/71、终点150/300。另建matte椭圆，从最早300/200调整到134像素，作为Alpha Matte；Scale0→100时间由最早10帧外移到约26帧。后者按尺标推定，不能记为直接读取关键帧时间。

02:35–03:45：Phase最终time*50，phase increment63，Z increment0→18、Radius0→61，形成展开而非静态排列。估读键帧Z16→43、Radius17→43；源画面执行Easy Ease In，未显示精确速度影响值。

04:02–06:30：加调整层stylize，CC Lens Size73/Convergence100；CC Vector Blur Type Perpendicular、Amount35。05:01附近口述减少到100形状。Tritone放最上、Lens最后；05:45中间调最后可读hex0CF6F0。主合成改黑底，1080方形/30fps/05:01。Fast Box Blur半径3是06:15尝试，06:22移除，不能当默认效果链。本机实测Type3显示Perpendicular，setTrackMatte真实调用/重开关联通过。

06:30–09:00（全局）：回总装处理径向背景；尝试Curves/Levels后实际Hue/Saturation、手绘Mask与Feather，降低背景边缘存在感。后续约15:28全局帧显示Hue315/Lightness-37；精确最终Mask路径、时间/透明度尚未逐段核验，不创建参数。

09:00–12:30（全局）：噪波条带拉长，关闭部分子层，外部加Colorama后Glow。阶段画面有Scale100/2280/100，随后改X；12:18帧显示Scale240/1630/100，但是否最终需追踪。Glow阈值48.2、Radius122、Intensity0.8在全局帧可读，仍需后续确认。

12:30–15:30（全局）：复制Colorama至圆环，主层Z改-7000；对子层Find Edges并Invert；发现Multiply导致线条不显示，改Screen；外部Linear Color Key改键黑色，追加Glow，调整Radius和Colorama增加白色。各枚举/最终值/渐变Palette尚未探测，不凭口述补造。

15:30–17:00（全局）：核心、点阵和背景淡出联动。16:38帧可见点阵Opacity表达式thisComp.layer("L7_algorithmic_spiral").transform.opacity。主层排序改变，不再简单沿用第15节；准确时序/淡出键尚待细看。

17:00–19:49（全局）：复制主合成为titleSeq_2，隧道加白色Fill/Glow；进入原预合成动画Z spacing，调整time offset到1，拉长Trim Paths时间并强调深度。课程延续下一节，标题问题未被本次前半节制作解决。

已实际制作：p16-core-001，100层/Phase速度50；p16-core-variation-001，独立Skill副本80层/速度65。各151帧原生渲染，全层运动公式及参数编辑重开恢复通过。用户对基线原片对照反馈“整体符合，可以保留”。精确曲线与三素材尚缺，ae-advanced-compositing0.1.5仍candidate；不宣称完整风格化片头。详细脚本与交付见该Skill的references/course-core.md及tests/core-results.json。
