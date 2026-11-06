# 第16节噪波条带调色组件

来源：[课程第16节](https://www.bilibili.com/video/BV1Yh4y1A7XT/?p=16)，09:00–12:18。这里只制作噪波组件；不包含核心、点阵、渐变背景和后段圆环，不代表完成总装。

09:42可见fN6、fN7关闭，fN至fN5保留。09:35和10:50的Scale100/2280/100是中间值；11:40与11:50更清楚显示342/423/100。主层保持Orientation Z90、Z=-5000和折叠变换。保留前面课程建立的可编辑Fractal Noise层及表达式，不使用教程截图或视频作为纹理。

外部效果顺序是白色Linear Color Key→Colorama→Glow。10:50调色盘保留三个色标：顶部紫色、底部青色、左下蓝色；随后继续调整顶部紫色。11:30及11:50可读Glow Threshold48.2%、Radius122、Intensity0.8。12:18原片主时间03:23显示Opacity0；另一键约02:11。59→95帧按尺标估算，线性插值未被直接显示，不能列为教程精确值。

## 原生调色盘

本机AE26匹配名是`APC Colorama`，不是`ADBE Colorama`。`APC Colorama-0012`属于CUSTOM_VALUE，实测读取失败。使用软件界面删除红、黄、绿三个色标，将紫色拖到顶部，再经原生颜色窗口设置估算值#5500FF。青色和蓝色保留原生默认。位置根据课程色轮外观重建，精确角度及原课hex未显示。

自制`assets/course-p16-colorama-noise-template.aep`保留可编辑色标。内含单层Ramp→Colorama→Glow，Ramp只用于模板检查；生成器复制整层保留原生调色盘，替换为自己的噪波预合成，再移除Ramp并添加白色键。不能用其他效果替代Colorama后声称按课程复刻。Adobe说明支持拖走色标删除、双击修改颜色，见[官方颜色效果说明](https://helpx.adobe.com/sa_ar/after-effects/desktop/adjust-colors/work-with-color-correction-effects/color-correction-effects.html)。

Glow阈值在原生脚本中是0–255，48.2%应设置122.91；直接设置48.2会改变效果。脚本实际重开后读取122.91000366，误差是浮点表示。

## 调用与输出

从实验室根目录运行`python skills/after-effects/ae-advanced-compositing/scripts/build_noise_style.py --out 全新目录`，再按通用run_ae.py与render_ae.py执行。默认Profile为examples/course-noise-style.json，原生输入校验SHA并随交付复制。`--glow-intensity 0.4`为显式变体。测试范围为4秒、1920×1080、24fps；尚未验证其他时长、画幅和三组素材。

输出project.aep、final.mp4、request/plan/receipt/quality/scene-quality及7张原生PNG。实际编辑Glow Radius122→123，保存重开后恢复122；每个表达式计算96帧，Opacity全96帧检查。早期001的淡出检查报告失败：嵌套条件表达式给出错误预期，实际轨迹正确；改为明确if/else后002通过。只保留失败报告，不保留失败工程。

## 结果边界与诊断

002基线与独立Skill副本生成的强度0.4变体均已真实渲染、全解码及7检查帧对照。基线39/48/60帧有蓝青条带、80帧淡出；0/24/95帧为空黑。前段空黑来自单独展示噪波和沿用的近似摄影机：其他组件缺席，不能当整片或声称与原课开场一致。继承的摄影机精确时序和随机图样仍需总装对照，用户没有验收这一新分支。

全黑时先核对时间点、相机与Z=-5000的前后关系，再检查白键、折叠变换及源图层启用状态。彩虹色说明自制Colorama模板没有复制成功；从随附原生输入重建，不能删除调色效果掩盖错误。缺输入或SHA变化立即停止。AE面板缩略预览不能代替原生PNG和成片验证。
