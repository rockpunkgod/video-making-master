# 第16节动态球形核心

来源：https://www.bilibili.com/video/BV1Yh4y1A7XT/?p=16 ，00:26–06:30；动态原片对照06:22–06:27。基线p16-core-001用户反馈“整体符合，可以保留”，只覆盖该视频整体展开、空心结构与色彩层次。参数变体、精确缓动与三种素材没有由此获验收。

复用本Skill自制examples/inputs/core.aep中的第11节空间方程，保留每层myIndex相对controls的索引，不把旋转改写成另一种几何算法。主合成1080方形/30fps/5秒1帧/16bpc，无显式CameraLayer。100个3D形状层、controls、stylize调整层，共102层。基础baseShape仍300方形，100像素椭圆去Fill、加22像素Stroke，Gradient Ramp起点[150,71]、终点[150,300]，黑→白。22来自00:49工具栏，不能使用口述的中间尝试10。

新增matte白色实心椭圆134×134（01:58读数），Scale0→100，作为下面描边层的Alpha Matte。最终Scale键约帧0/26，从02:15尺标估读；不是最早尝试的帧0/10。通过本机实际setTrackMatte关联，保存重开后读回trackMatteLayer和ALPHA类型验证。关闭matte自身可见开关不移除其遮罩作用。

Phase表达式time*50；Phase increment63；Z increment由0→18，Radius由0→61。Z键约16/43帧，Radius约17/43帧（03:18–03:45时间轴估读±1帧）。原方程r=Radius×2π、phase=degreesToRadians(Phase+myIndex×63)、z=Z_increment×myIndex，末行[x,y,z]+value保留。按课程Easy Ease In重建原生incoming Bezier speed0/influence33.3333，outgoing Linear；影响百分比是标准原生操作的重建，课程未展开精确速度框，不声称完全一致。

调整层链：Tritone→CC Vector Blur→CC Lens。Tritone中间调最后可读05:45为#0CF6F0，高光白/阴影黑、Blend0；Vector Blur Perpendicular/Amount35/Angle0/Ridge1/Map None/Property Lightness/Softness15；Lens Center540/540、Size73、Convergence100。本机实际枚举3在GUI显示Perpendicular；保留原生证明PNG。06:15尝试的Fast Box Blur半径3/迭代3，06:22已移除，默认不包含该效果。不要把建议的Levels当成实际应用。

scripts/build_core.py --out新目录生成请求/计划/JSX并复制自己的原生输入；run_ae.py后render_ae.py --reuse实际渲染。--count20–176、--speed1–150为显式参数变化。默认100依据讲师05:01附近口述；源工程最终实际总数未直接读出。输出可编辑project.aep、151帧final.mp4、原生回执、六个检查PNG及质量报告。不依赖教程原素材或Video Making。

逐层逐帧核对位置公式，实际修改Phase increment63→64、保存重开、恢复63再重开，检查Alpha Matte和效果顺序。渲染器全帧解码、检验可见运动、对照四个原生检查帧；真实冻结视频虽然解码成功仍被运动条件拒绝。技术检查不能量化审美或证明任意新素材可用。80层/speed65变体从独立Skill副本真实执行，不是三种输入素材测试。

基线的全分辨率青色高光较原片半分辨率预览集中，宿主/采样差异原因尚未实测归因，用户只接受整体效果。需要精确对齐时先取得干净连贯参考帧、对应合成时间和色彩设置，不能通过重新调色后转移原验收。后续总装仍须处理背景淡出、Colorama、圆环Screen/黑色键控、Glow及标题问题，本资产不表示整片完成。
