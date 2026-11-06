# 来源与可信度

来源：https://www.bilibili.com/video/BV1Yh4y1A7XT/ ，标题 Advanced After Effects Coding for Motion Design，上传者 XQ_祈灵。页面说明其为搬运，画面含 Domestika 标识。未取得素材再分发许可，因此缓存不参与分发。

该链接包含20节；默认第1节 About Me不是技术制作课。本技能仅提取第5和第6节的局部技术，不代表整套课程已学完。

## 第5节 ?p=5

- 02:00：明确展示 1080×1080、30fps、7秒合成，以及四个矩形轮廓在不同Z深度分布。
- 06:00：明确展示 controls 主控和 Position 表达式编辑。
- 08:00：画面中出现“expression result must be of dimension 3”临时错误，不能把未写完的代码当成最终实现。
- 10:00：明确展示序号计算 index - controls.index - 1、Z Spacing 和 ref + [0,0,offset]。
- 12:00：明确展示多个重复层、Z间距795、Z旋转33度（当时画面状态，不是最终统一参数）。
- 14:00：明确展示 time 驱动参数的编辑中状态。
- 16:00：明确展示 Camera 1 的 Z Position 表达式 value+time*500，以及透视隧道。

## 第6节 ?p=6

- 01:15：明确展示红色矩形空间隧道及 Camera 1、controls、多重复图层。
- 03:32：明确展示 framesToTime(Time offset) 与 index - controls.index，仍在输入代码中。
- 03:55：明确展示 offset=myTime*myIndex 及 ref.valueAtTime(time-offset)。
- 06:06、06:25：明确展示 Trimpath 主控、延迟取样与 Opacity 的同类实现。
- 06:50：明确展示重复层依次形成红色轮廓隧道，Time offset 显示2，Trimpath显示100。
- 07:10：明确展示预览中的旋转轮廓，不能仅由单张图推定速度曲线。

已使用 Watch 全段稀疏抽帧并补充定位帧。第5节场景抽帧几乎漏掉全部界面操作，已用2分钟间隔的指定帧补充。两节均无可用原生字幕；语音含义未验证。时间戳是源视频时间，非合成时间。

第6节06:50—06:52另外使用FFmpeg以24fps提取48帧，逐帧接触表均已审阅，可观察到轮廓旋转与重复层延迟。但录屏中包含预览循环和播放头状态，不能把录屏时间直接等同合成时间；没有可靠拟合原始速度曲线。

续作已生成6组Adobe原生工程和成片，基础矩形的轮廓、三维深度与延迟旋转机制对照通过，见项目evaluations/first-skill.json。不是整门课程的完整视觉复刻，也不是对原始未知缓动参数的验证。
