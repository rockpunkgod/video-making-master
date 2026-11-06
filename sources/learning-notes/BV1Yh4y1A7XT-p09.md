# 第9节：Randomization — Displacement（尚未制作）

586.5秒，Watch缓存watch-4cg7gf71。11张全局帧及watch-2u9glhav的6张指定帧已实际审阅；全片已有本地small ASR完成并阅读。字幕不是视觉操作的替代，下一步需补初始形状尺寸、Fill颜色表达式及合成背景证据。

本节重点为三维位置随机数组、每层随机速度的时间漂移，以及用+value保留手动微调。当前没有证据表明本节写了随机旋转表达式；界面的旋转柄只是3D图层控件，不能从柄形状推断动画。

03:39位置代码可见：seed=thisComp.layer("controls").effect("seed")("Slider"); seedRandom(seed,1); posMin从Position Min的3D Point取得；posMax同理；pos=random(posMin,posMax);。当时seed77，Min[0,0,0]，Max[1920,1080,3000]。这是真实3D Point Control，不能代换成各轴独立Slider后称课程原结构。

04:57扩大范围且使用Custom View 1绕视观察，seed165、XMin=-1084、XMax3130。Custom View是检查空间分布的视图，不是已经制作了摄影机运镜。05:15切回Active Camera(Default)，YMin=-630、YMax1950，Z范围还在调整。06:45明确读到最终Min[-1084,-630,1930]、Max[3130,1950,8890]，seed165，driftSpeed310；代码加drift=time*random(thisComp.layer("controls").effect("driftSpeed")("Slider"));，最后pos+drift。scalar drift加到位置向量的原生行为尚需实测，不预先改写成三个随机方向。

08:35同一位置公式最后变成pos+drift+value，图层原始Position先设[0,0,0]，随后手动X186示范加偏移。这样并非解除表达式，而是利用原始属性值做艺术指导。09:06主控seed409、driftSpeed=-124，位置范围仍如上；形状层总数显示48，加controls共49层。具体随机色值不作为跨版本固定承诺。

课程口述提出可以设置随机速度下限50，随后明确这只是练习未展开；不得将该建议加进课程baseline。后续可作带出处的泛化变体。主控位置范围与速度经历多次试验，早期[0,0,0]→[1920,1080,3000]不是最终画面设置。

融合计划：作为ae-advanced-expressions的独立三维随机布局/漂移分支，共用seedRandom原理，但不与第8节threshold显隐硬合并为一个公式。现在仅学习取证，未生成第9节AEP或视频，不计verified或已制作。
