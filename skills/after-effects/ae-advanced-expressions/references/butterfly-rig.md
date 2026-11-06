# 第24节：铰链式双翅与平面路径飞行（部分候选）

[原课](https://www.bilibili.com/video/BV1c7GTzMEh5/?p=24)。不宣称已实现整节：Particular未出现在本机AE实际效果列表，后半粒子拖尾未制作，不能换用其他粒子系统冒充原法。

## 已观察方法

01:00–02:20：素材分别用Mask提取翅膀/身体，复制翅膀预合成并在内部水平翻转。03:11–04:19：身体和双翅为三维层，翅膀锚点放在身体连接处，绕Y旋转。04:36–05:09旋转摄像机观察。

05:30起random逐帧跳变，被否决；06:52起wiggle振幅不均，被否决。07:50–10:49：右翅Y Rotation先做四个样本关键帧；默认cycle跨边界跳变，改为`loopOut(type="pingpong", numKeyframes=0)`，再缩短关键帧间距。11:07–12:19：左翅读取右翅Y Rotation并取负，不使用独立随机动画。

12:46–14:29：三个三维层父对象为二维Null，便于平面移动/缩放。14:29–15:59：Position关键帧及空间Bezier手柄塑造轨迹。16:23–17:31：Null设置Auto Orient Along Path，再补Rotation90。17:41–19:15演示在Position上叠加wiggle(3,15)、改30后复位；此分支未移植进基线。19:15–22:36绘制心形飞行轨迹。22:54后Particular两层：发散金色粒子与零速度红线，连接发射器Position至Null；通过发射数量关键帧切断多余起止线段。完整参数尚不具备原生验证。

## 输入与执行

在实验室根目录调用现有Python、AE、aerender和FFmpeg，使用全新输出目录：

```powershell
python skills/after-effects/ae-advanced-expressions/scripts/build_butterfly_rig.py --out samples/runs/butterfly-new
python skills/after-effects/ae-advanced-expressions/scripts/run_ae.py samples/runs/butterfly-new/build.jsx --ae 'E:/自媒体/Adobe After Effects 2026/Support Files/AfterFX.exe'
python skills/after-effects/ae-advanced-expressions/scripts/render_ae.py samples/runs/butterfly-new --aerender 'E:/自媒体/Adobe After Effects 2026/Support Files/aerender.exe' --reuse
```

`--mode flap|flight`，`--speed 0.5..2`，`--style monarch|moth|petal|mechanical`，或`--profile`指定配置。当前仅支持这四种原创图形，不支持直接接入任意翅膀照片；新图形需扩展素材适配并另行验证。speed为关键帧时间缩放，仍由原生pingpong循环执行。

原生合成790×633、25fps、8秒来自课程界面。四帧0/4/8/13、角度-44.8/55交替、翼根位置和自制图形尺度是推定候选，不是已读出的完整原课数值。摄像机65度与固定半径、主控115%是根据画面方向适配，仍未精确确认。源片有预览残影，不在自制动画中复制录屏残影。

输出AEP中保留ART_WING_SOURCE/ART_BODY_SOURCE原始可编辑图形、实际PNG、Mask、镜像预合成、三维铰链层、二维主控、摄像机和关键帧。修改ART后需重新导出对应PNG并重载；PNG是实际必要媒体，Mask及铰链仍可编辑。flight沿空间Bezier关键帧移动，控制点和手柄是根据课程形状推定的自制版本；不声称与原轨迹或速度完全相同。

MP4仅底部补1行黑色，变为790×634以兼容yuv420p；AEP不改变633高度。当前宿主二维Position返回三分量，Bezier切线按实际属性数组长度补零，不能因二维层就假设两元素可用。保存重开后实际检查双翅符号、pingpong全帧与关键帧编辑恢复。输出TIFF由真实aerender制作，视频全帧解码及周期检测独立进行。

## 诊断与边界

双翅同向倾斜先查左侧表达式是否取负；绕中心翻转查翼根锚点；循环跳帧查是否误用cycle；位置切线报维度错误读宿主实际数组长度；身体白边查自制素材的背景与Mask。不要用random/wiggle替换课程扇动基线。

检查器验证200帧原生取样、真实运动和整帧周期；它不验证摄影机身份、源素材、精确源时间轴或审美。恒定视频即使有周期也必须被运动检查拒绝。flight的朝向需画面审阅与原生AutoOrient枚举共同检查，不把Rotation属性本身当作自动朝向后的世界角度。
