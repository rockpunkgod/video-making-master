# 第15节极坐标圆环：候选分支

来源：https://www.bilibili.com/video/BV1Yh4y1A7XT/?p=15 ，05:35–08:45；最终播放对照08:40–08:45。该分支复用本Skill自制examples/inputs/noise.aep，不需要教程工程或原始素材。

保留1080×1080/30fps/7秒/16bpc的噪波重复结构及禁用的Camera1。保留FN7，改变Fractal Noise为非等比Width500/Height149.9（07:43可读），其余Strings/Block/Invert/Contrast2000/Complexity1沿用前课。Evolution沿用`time*5`；加Polar Coordinates，Interpolation100%、Rect to Polar。按原法复制到FN7–FN12六层，Multiply、3D、Z间隔350、旋转间隔0、缩放间隔0，基础Position[540,540,500]沿用输入工程。

Offset Turbulence基础值重置540/540，最终表达式是`value+[0,time*100]`。此前time*50和手动关键帧是试调，不能替代最终设置。每个副本独立计算噪波，精确弧段随机图样依赖图层身份；原片种子参数没有显示。自制输入的seedRandom(1,true)来自前课复刻，不能宣称已恢复教程源工程的图层身份。

本机实际发现：Polar Coordinates插值的脚本值范围0..1，GUI100%应设1，直接设100会失败。转换枚举1在本机中文界面实际显示“矩形到极线”，与Rect to Polar一致。原生截图native-still-gui-conversion.png保留，不能用未经核验的下拉序号猜测。

调用scripts/build_noise_asset.py --out全新目录，默认examples/course-polar.json；随后本Skill run_ae.py和render_ae.py。--offset-speed、--height、--count、--seed是明确变体，保留请求/计划。输入AEP先核SHA并复制进交付inputs，拒绝关闭未保存或其他工作的AE工程。

原生检查六层各210帧的Offset、Evolution与Z间隔，实际改写偏移表达式、保存重开再恢复；检查外部媒体缺失和表达式错误。导出4个原生PNG，与真实渲染对应帧比较；全帧解码另检查可见运动。检查器用冻结视频做过实际负例，格式正常仍应因没有动画而失败。这些只证明技术性质，不证明审美或课程精确同步。

状态candidate。已制作基线、速度60/Height90/9层/种子7变体，并从隔离Skill副本制作速度140/Height120/3层/种子23工程及视频。它们是参数测试，不等于三组不同素材。没有完成本节空间条带、渐变背景和总装；用户原片对照结论单独写入测试记录，不向变体转移。

排错：插值超范围先核0..1宿主值；变成条形或扭曲方向错误时核转换类型；只有单层时核复制数量及图层可见性；圆环位置不对先核默认摄像机与旧Camera1禁用状态，别加入自设摄像机；画面看似静止时检查Offset表达式是否启用，而非换静帧交付。

用户对p15-polar-002原片对照的最新反馈为“整体符合，可以保留”。仅接受该视频的圆环层次、疏密及整体运动，变体/精确随机身份/跨素材未由此获验收；Skill仍为candidate。
