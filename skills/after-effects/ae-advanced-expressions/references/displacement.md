# 三维随机布局、X漂移与手动偏移（candidate）

来源：https://www.bilibili.com/video/BV1Yh4y1A7XT/?p=9 。00:40/00:49明确Fill颜色表达式seedRandom(5,1); random([1,1,1,1])，不是固定RGB或自选配色。08:35显示位置最终式；09:06显示最终主控seed409、driftSpeed=-124、Position Min[-1084,-630,1930]、Position Max[3130,1950,8890]。48个形状加controls共49层，Active Camera(Default)，没有课程摄影机运动。

核心代码取seed后seedRandom(seed,1)，取两个3D Point Control数组，再pos=random(posMin,posMax)。漂移drift=time*random(driftSpeed)，最终pos+drift+value。+value前先把原始位置归零，允许手动微调。保留实际3D Point Control，不拆成三个自制滑块；只在中文宿主将参数显示名换成同参数(1)。

本机原生探测[10,20,30]+5实际为[15,20,30]，不是三个分量同时加5；课程pos+drift也仅X变化。数组运算的维度处理见[Adobe表达式语言参考](https://helpx.adobe.com/after-effects/desktop/work-with-expressions/expression-language-reference/expression-language-reference.html)。因此不能在“优化”中替换为三轴随机漂移。Fill随机数组第4项确实生成随机Alpha，保留原式，不偷偷设成1。用同一个属性身份读取随机pos与速度，再恢复原式独立核验150帧；不要从另一个Slider的random值推断Position的随机样本。

参数：--stage final（默认）48形状；--seed默认409；--drift-speed默认-124；--asset调用者PNG复制为assets/input.png，导入可编辑ORIGINAL_INPUT预合成并以300像素范围保留比例；每层实际使用同一空间公式。PNG不加Fill随机色，属于课程方法泛化。--stage initial只是课程初始三个形状的静态几何诊断，不是最终动画，其视频不应通过“存在运动”的动画门槛。

1920x1080、30fps、5秒、16位。圆直径300、方形270、三角形底311.769高270是视口推定，没读到源属性面板；背景224/255也是压缩视频RGB采样推定，未经色彩管理原值确认。初始形状在固定视口裁剪对照通过平均轮廓差0.0356像素；先前包含界面细边线的失败结果保留，后续按真实面积区分三个形状，没有调整构图或曲线来套参考。

真实制作：samples/course-reproduction-005/p09-final-002，另有seed165/speed310课程内变参和geometry/typography/texture三个PNG案例。5组各150帧、native位置公式、颜色不随时间改变、+186手动偏移及速度加倍后保存重开还原均通过。后四组从独立技能副本、实验室外cwd执行。每组10张接触帧已实际检查，运动连续，但薄线和小文字PNG在浅灰背景对比弱、可读性不足；技术通过不等于审美/可读性通过。没有三维旋转、自动摄影机或景深能力声明。

诊断：素材过小/低对比，先记录预览失败条件，再让新需求选择有足够对比与有效画幅的素材，或明确制作泛化变体；不能改课程基线掩盖问题。手动拖动无效时检查最终是否+value、原始Position是否归零。漂移方向错误时检查标量加数组行为及宿主版本，不按普通JavaScript字符串加法解释AE表达式。
