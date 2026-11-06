# 第9节：Randomization — Displacement

586.5秒，Watch缓存watch-4cg7gf71。11张全局帧及watch-2u9glhav的6张指定帧已实际审阅；全片已有本地small ASR完成并阅读。字幕不是视觉操作的替代，下一步需补初始形状尺寸、Fill颜色表达式及合成背景证据。

本节重点为三维位置随机数组、每层随机速度的时间漂移，以及用+value保留手动微调。当前没有证据表明本节写了随机旋转表达式；界面的旋转柄只是3D图层控件，不能从柄形状推断动画。

03:39位置代码可见：seed=thisComp.layer("controls").effect("seed")("Slider"); seedRandom(seed,1); posMin从Position Min的3D Point取得；posMax同理；pos=random(posMin,posMax);。当时seed77，Min[0,0,0]，Max[1920,1080,3000]。这是真实3D Point Control，不能代换成各轴独立Slider后称课程原结构。

04:57扩大范围且使用Custom View 1绕视观察，seed165、XMin=-1084、XMax3130。Custom View是检查空间分布的视图，不是已经制作了摄影机运镜。05:15切回Active Camera(Default)，YMin=-630、YMax1950，Z范围还在调整。06:45明确读到最终Min[-1084,-630,1930]、Max[3130,1950,8890]，seed165，driftSpeed310；代码加drift=time*random(thisComp.layer("controls").effect("driftSpeed")("Slider"));，最后pos+drift。scalar drift加到位置向量的原生行为尚需实测，不预先改写成三个随机方向。

08:35同一位置公式最后变成pos+drift+value，图层原始Position先设[0,0,0]，随后手动X186示范加偏移。这样并非解除表达式，而是利用原始属性值做艺术指导。09:06主控seed409、driftSpeed=-124，位置范围仍如上；形状层总数显示48，加controls共49层。具体随机色值不作为跨版本固定承诺。

课程口述提出可以设置随机速度下限50，随后明确这只是练习未展开；不得将该建议加进课程baseline。后续可作带出处的泛化变体。主控位置范围与速度经历多次试验，早期[0,0,0]→[1920,1080,3000]不是最终画面设置。

融合计划：作为ae-advanced-expressions的独立三维随机布局/漂移分支，共用seedRandom原理，但不与第8节threshold显隐硬合并为一个公式。现在仅学习取证，未生成第9节AEP或视频，不计verified或已制作。

续作实际制作：另补00:31/00:40/00:49/01:00/08:59五张指定帧，确认Fill原式seedRandom(5,1); random([1,1,1,1])，不将Alpha擅改1。本机原生[10,20,30]+5=[15,20,30]，drift只作用X；3D Point参数matchName实际ADBE Point3D Control-0001。探测AEP及receipt在evaluations/course-p09-probe-001。数组维度参考Adobe官方表达式文档，不能按普通JavaScript数组字符串行为改写课程式。

已生成samples/course-reproduction-005/p09-final-002、seed165-speed310-001及geometry/typography/texture三组PNG，5组真实AEP和5秒视频；每组49层、16位、无显式Camera层，150帧原生空间公式最大误差小于1e-12，颜色时间漂移0。实际Position原值+186、速度加倍均保存重开后验证，再恢复重开。三组PNG不同SHA、保持导入素材可编辑，未加Fill随机色。后四组从isolated-skill-006副本在实验室外cwd执行。全部150帧解码且各10张接触帧实际审阅。

初始形状诊断p09-initial-001是三形状静态渲染，故不以“有运动”门槛评价。形状尺寸推定圆300、方270、三角底311.769高270；灰底从压缩视频中取RGB224，不能称读到了AE原色。固定viewport[347,93,690,389]最初对照被界面边线污染，平均差4.62失败保留；排除实测面积<=775的边线碎片，仅保留三个面积>=1000的形状后，原构图/原裁剪未变，平均轮廓距离0.0356、P95=0，通过几何检查。这不验证精确RGBA或最终随机排列。

首个p09-final-001回执将activeCamera===null误当默认摄影机判断；有3D层时该判据不可靠，未将其当课程摄影机差异。脚本改查真实CameraLayer数量，重新制作002得到0个显式Camera层。旧001工程/回执保留，正式证据采用002。

画面限制：向左/右的缓慢连续漂移符合原式；原图样的具体排列跨层身份不同。PNG细线和小字在课程灰底上对比弱，文字可读性不足，未将技术通过冒充前景排版质量通过。已请求用户核对最终基线观感，尚未收到反馈，ae-advanced-expressions0.2.0仍candidate；该版本融合第8、9节，不按视频计技能数。上文“尚未制作”为之前学习阶段的历史状态，现已由这些真实输出更新。
