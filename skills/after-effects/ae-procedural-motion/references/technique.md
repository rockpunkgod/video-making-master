# 延迟与空间分布

本页主要说明build.py/template.jsx历史自主变体；它的Order、时间点和曲线不属于0.3.0课程原法验收。当前课程调用以course-stage.md及build_course_stage.py为准。

核心不是复制关键帧，而是为每个元素定义稳定的序号 n，读取同一主控属性在 t - n·delayFrames/fps 的值。空间深度另由 n·zSpacing 决定。

教学实现以 index 与主控层 index 的差求序号。独立实现把序号写进各层的 Order 滑块，以免插入文字、背景或相机后改变序号。这是设计改进，不是视频原样操作。

三维图形 Position 返回 [x,y,z]，Scale 返回三维比例；2D 内容应置于预合成再启用三维。主控只承载动画与参数，不渲染。原始素材层、预合成和相机均保留可编辑。

输入：name、width、height、fps、duration、count、delay_frames、z_spacing、size、stroke_width、color、rotation_degrees、camera_zoom、shape（square/triangle/hexagon）、asset（可选图像或视频绝对路径）。

输出：目标目录中的 build.jsx、project.aep、receipt.json 与 render 队列。参数必须为有限数，数量有上限；素材路径必须存在。默认无音轨，因此声画同步检测为不适用，不能记为通过声音设计测试。

当前教程的关键帧缓动具体数值未从画面可靠读取。示例的时间点、镜头尺寸及缓动属于独立设计，需由实测评价，不宣称为原教程参数。

组合：可作为 kinetic typography 的空间容器或 compositing 的背景；未提供跟踪、投影重建、Mocha 或 PR 自动剪辑能力。
