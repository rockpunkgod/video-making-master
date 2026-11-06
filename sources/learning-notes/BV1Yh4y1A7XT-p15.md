# 第15节 Additional Design Assets（部分原生制作，课程尚未完成）

来源：https://www.bilibili.com/video/BV1Yh4y1A7XT/?p=15 。完整1218.1秒原片经现有Watch取得；24张全局帧实际审阅，现有本机faster-whisper-small完整英文转录已阅读，无安装、模型下载或上传。公开1080p视频另用于10张指定操作帧及05:33/07:43/08:45三张补帧，全部实际查看。字幕只定位讲解，参数以下述画面为依据。

## 径向轮廓背景 00:57–05:33

00:57合成1920×1080、24fps、10秒、黑底。Fractal Noise Basic/Soft Linear，Contrast400、Brightness-100、Complexity6、Invert关；演化使用前课建立的演化速度Slider，而非新粒子算法。05:11演化速度48仍是试调；05:28输入框只有未完成数字2，不能截取当最终值。05:33最终显示25。

效果顺序：Fractal Noise → evolution_speed控制器 → CC Radial Fast Blur → Unsharp Mask → Find Edges → Curves。Radial中心960/540、Amount100、Zoom Brightest；Unsharp Amount300/Radius1/Threshold0；Find Edges反转开、原图混合0。03:28–04:55分别编辑RGB通道曲线，产生蓝紫色轮廓与暗部色彩。讲师04:35口述可用Hue/Saturation进一步调整，但对应操作画面至05:33没有该效果，不能把建议写成已执行步骤。

曲线确切点值未显示。按04:55曲线图重建红色多峰、绿色窄峰和蓝色提亮；记录为画面推定，不能写成课程精确数字。初版偏紫红，放大曲线原片后重新在AE中调节得到002。保留课程原效果器，不用Tint、Lumetri或后处理滤镜代替。复刻中的原生曲线可编辑；随机种子0是宿主默认，原片未显示，确切噪波图样同源尚未证实。

本机AE26.0x67实测：CurvesCustom-0001为CUSTOM_VALUE，读取即报未实现，故用必要GUI操作完成通道曲线，保存自制AEP模板供脚本导入。CC Radial Fast Blur的Zoom1实际Standard，2实际Brightest；初稿1已修复为2，两个菜单读值都有实际界面核对。不能把默认枚举当Brightest。

真实制作：p15-radial-002为10秒240帧，p15-radial-slow-002为6秒144帧、速度12、种子17的变体。速度/种子/时长变化不等于三组跨素材泛化。通过原生控制器修改、保存重开、恢复以及全帧演化值核查；渲染基本检查不证明课程视觉验收。P15其余素材与总装尚未完成。

## 极坐标圆环 05:35–08:45（已取证，尚未原生制作）

复制第13节条带预合成，加入Polar Coordinates。最终Interpolation100、Rect to Polar，不能沿用默认转换方向。07:43可读到Fractal Strings/Block/Invert、Contrast2000、Complexity1、非等比Width500/Height149.9；此前Height20是旧条带，不是新圆环最终值。

先对Offset Turbulence打关键帧，再改为`value+[0,time*50]`并重置基础值540/540。08:20最终改为`value+[0,time*100]`，这是后续制作应保留的表达式。08:32和08:45时间轴显示FN7–FN12六层，Multiply、3D，Position Z spacing350、Rotation Z spacing0、Scale interval0。Camera1存在但当时是Active Camera(Default)，不要擅自启用来源相机或复制主摄像机运动。演化值也随时间变化，具体沿用前课表达式需要核对。

## 空间条带及粗总装（已全局理解，细参数待核对）

约09:00起复制旧噪波条带改窄、改长，再复制随机位置控制器和Position表达式；讲师强调不需要漂移、约19:20才缩小Z范围，不能把中途复制的旧范围和driftSpeed误当最终设置。最终白色条带主层Z约-16540从19:18画面读取；精确条带宽高/层数/禁用漂移方式尚需逐项取证。

约12:00加入径向背景并随摄像机后退淡出，12:45用4-Color Gradient建立深色底，14:00加入前节文字与圆环。16:00之后预览跳帧，仍为粗布局，完整风格化在16/17节。不能为填满20秒尾部自行创造剧情、颜色和镜头并称课程复刻。

尚缺：圆环/条带原生制作与验证、渐变底色的真实数值、背景淡出关键帧、文字/圆环进入主合成的精确时序、全节总装、三组适合该效果的新输入测试、用户原片对照反馈。
