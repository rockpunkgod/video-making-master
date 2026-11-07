# 正弦波形的叠加、相乘与包络

来源：[BV1c7GTzMEh5第22节](https://www.bilibili.com/video/BV1c7GTzMEh5/?p=22)。与第30节共用Write-on累积绘制单元；第23节共用sin/linear数学原理，但该节输出是笔刷历史，不能替换成弹簧端点动画。

## 先按课程制作

以具有Pillow的既有Python执行本Skill的scripts/build_wave_writeon.py --mode sum --out新目录；再调用同目录run_ae.py（--ae实际AfterFX路径）和render_ae.py（--aerender实际路径，暖宿主可--reuse）。只串行运行Adobe任务，构建日志重定向文件。不要用FFmpeg模拟课程成片；FFmpeg仅封装实际AE渲染帧、分析与制作评审对照。

原生720×576、25fps、10秒、黑色全画幅Solid、白色Write-on；笔刷2、Hardness79%、Opacity100%、StrokeLength0、PaintTimePropertiesColor、BrushTimePropertiesNone、OnOriginalImage。正方形像素为当前推定；单独工程只保留正在演示的可见阶段，课程留作讲解的旧禁用层不复制。

| 模式 | 原式与明确参数 | 来源时间 |
|---|---|---|
| sine | y=sin(time*3)*80；x=time*60；返回[x,y+576/2] | 14:45、15:00原课单独A层 |
| sum | a=sin(time*3)*80；b=sin(time*20)*20；y=a+b；x=time*60；y再加288 | 11:00–14:20，16:45完整原式 |
| product | y=a*b；幅度最终40、5；角速度仍3、20；x=time*60；y加288 | 17:00–18:00；早先40×10或80×20为调试状态 |
| decay | fudu=linear(time,inPoint,outPoint,100,0)；y=sin(time*4)*fudu；x=time*75；y加288 | 19:00–23:30，早先固定7/9/10秒是过程变体 |
| slider | fudu=effect("Slider Control")("Slider")，其余与decay的正弦/水平速度一致 | 23:45–25:45 |

频率参数直接乘弧度，不擅自补2π。正sin使画面向下；累积绘制从左侧开始，不居中、不加平滑、不清理原版点状笔迹。sum/sine/decay间隔源UI0.010秒；product在18:02–18:10的刷新后UI明确0.003；先前编辑中0.00不是最终值，按0.003制作，实际读回值在receipt字段7。不要因源点状图样难看就替换成连续矢量曲线。原课中间写错高度720/2，后明确改576/2，使用更正后的式子。

slider必须传--slider-profile（JSON keyframes列表，每项time/value，线性），不内置伪造原工程键。examples/p22-slider-inferred.json明确为画面推算：三键0/2.08/9.96秒、100/275.01/0；来源25:08、25:14、25:16、25:20、25:24的时间线与数值有刷新滞后，初值和精确时点未读回。它是候选包络重建，不能标为原始关键帧。自有Profile也可制作多峰包络。

## 参数与输入

--mode sine|sum|product|decay|slider；--duration4..12秒且整25fps帧；--rate-a0.5..8、--rate-b5..30、--amplitude-a1..200、--amplitude-b1..30、--speed30..100。A幅度不控制slider，slider实际使用Profile。改时长会改变decay出点和包络归零时刻，其他模式不会自动适配水平速度；允许课程式边缘裁切，不能静默归一化。

--asset仅接受调用者自有720×576、不透明PNG，各RGB通道≤96，用于白色轨迹在不同暗底上的泛化；复制到输出assets后原生导入并明确设置PAR1。当前不支持视频、透明输入、白底、任意大小、其他笔刷颜色或自动图像适配。examples/assets/wave-{grid,circuit,gradient}.png为自制测试图，与教程两张数学插图无关。

输出request/plan、可编辑project.aep、receipt、final.mp4、quality/wave-quality和7张必要原生PNG。实际编辑笔刷2→3、保存重开确认再恢复2，逐帧读取原生笔刷坐标，不能把单纯JSX生成当作AE成功。观看对照后独立记录人工视觉反馈；这些模式目前均candidate。

## 组合与故障

同第30节共用原生Write-on效果、累积历史与渲染封装；保持单元内不同轨迹实现，不能把本课相加误改成圆周投影或弹簧动画。可将工程预合成作为后续合成Skill输入；未实做的跨Skill组合不算已验证。

位置属性必须返回二维数组；标量sin直接赋给BrushPosition会报维度错。曲线贴上边检查+576/2；振幅爆出画布先核对乘法的幅度乘积，不擅自缩放基线。点状轨迹检查原生间隔、BrushSize和速度，既要保持课程，又要区别压缩噪点。PNG变形检查导入Footage PAR1；重开后重新查找Comp/Layer，旧对象可能失效。宿主有未保存或其他项目时保留并报错，不强关。失败结果写报告，修复后输出全新目录。

详细验证结果见../tests/wave-writeon-results.json；指标仅检查几何、历史笔迹和真实原生输出，不替代逐帧原课同步或审美验收。
