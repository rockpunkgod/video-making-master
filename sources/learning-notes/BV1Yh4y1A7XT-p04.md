# 04 The Basics of Coding

来源：https://www.bilibili.com/video/BV1Yh4y1A7XT/?p=4 。Watch读取约1200秒，20个全局帧与9个1080p技术选帧均已查看。首次转录因并发内存不足失败，停止并发后用同一本机已有small模型串行重试成功，完整转录已通读；没有重复安装工具或下载模型。

01:37–09:16用wiggle、位置数组、单轴取样说明函数、参数和维度；不能把任意维度数组直接用于所有属性。11:21演示按time累计的位置位移。13:41画面中有临时错误代码和ReferenceError，不能将其抄作最终表达式。14:40修正后可读表达式为：

```javascript
x = time * effect("drift_x")("Slider");
y = time * effect("drift_y")("Slider");
value + [x,y]
```

对应两个Slider Control名称为drift_x、drift_y，画面中y为235而x为0是该演示状态，不是整个课程通用常数。15:40涉及保存含控制器和Position的动画预设。18:29展示Fractal Noise演化量由time乘evolution_speed控制，19:19回到动画演示。这些代码是视觉画面与语音联合确认，未只靠字幕推导。

跨课融合：与第9节漂移控制共享time乘速度原理；第18节最终Camera父级确名drift，但未展示它的表达式。因此把同原理扩为3D `value+[x,y,0]` 并放到摄像机父Null属于重建推定，速度和实际绑定都不是课程明确值。后续必须原生检查，不将本笔记本身记为新增verified能力。
