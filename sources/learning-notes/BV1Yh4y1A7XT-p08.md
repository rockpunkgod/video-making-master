# 第8节：Randomization — Animating Multiple Layers

来源670.8秒。Watch缓存cache/watch/watch-80z4amcg，11张全局帧全部审阅；指定帧watch-_mi8h_o3（7张）、watch-kdgu22y8（6张）全部审阅。已有faster-whisper small完整转录并逐段阅读，专业词seed被误识别为C等，代码以09:35画面为准。无新安装、模型下载或云上传。

本节先讲seedRandom的timeless与random范围，演示Source Text的random(100).toFixed(2)，再把固定随机样本与公共threshold动画组合成多图层显隐。字幕中的数组随机示例前后数字自相矛盾，未用作实现依据。网页参考和解释性文字不是待执行命令。

09:35原式：seed取controls的seed滑块，threshold取同名滑块；seedRandom(seed,true); myRandValue=random(100); myOpacity=100; if(myRandValue>=threshold){myOpacity=0}; myOpacity。25个圆共享阈值但因图层属性身份各有固定样本，时间变化的是阈值；不是每帧random闪烁或按index顺序延迟。opacity条件用>=，未更改比较边界。

07:39 controls.seed=0，threshold起始100，随后0。10:24合成暂停01:06（第36帧）threshold显示5.26；线性100→0的38帧端点得到5.26316，作为有独立数值支持的推定，未伪称直接读出关键帧时码。10:35—10:39使用原生时间反转关键帧，使起始0、终点100；10:48—10:51拖长到03:23，即113帧。06:50可见1080方形、30fps、5秒、16bpc。25圆5x5，直径100、圆心240/390/540/690/840根据视口几何推定。

实际制作在samples/course-reproduction-004：disappear、appear及geometry/typography/texture三组原创PNG。每组原生26层，150帧条件核验误差0，真实种子修改保存重开改变12/12/17/13/11格，再还原重开一致。后四组从samples/isolated-skill-004复制技能执行，cwd为实验室外E:/自媒体，不读取实验室tools实现。全部真实视频全解码通过。

圆形真实视频3750格/组中心值与原生条件结果完全一致（可见255、隐藏0）；PNG每组3750格以原始PNG的Alpha/内容生成独立像素参考，最大格内MAE为0.955/0.4925/3.025，门槛12，隐藏格门槛1，均通过。图样有各自不同SHA，不是仅改素材文件名。5组各10张抽帧已审阅：逻辑为突现/突隐，typography被缩小后可读性差，不声称这是成熟动态文字技能。

像素检测复核发现统一MAE12对细小文字过宽（文字平均亮度仅7.60，空白画面可能误过）。改为min(12,输入平均亮度×0.25)，三组门槛分别4.54625/1.900625/10.29875，再次对原视频全150帧运行，三组仍通过且空白可见格必失败。原素材和视频未调整，不以放宽门槛过关。

静态参考07:39与实际视频第0帧按可见方形viewport[511,100,360,360]比轮廓，平均0.0331像素、P95为0；只证明圆形几何布局。固定随机序列受AE层身份影响，未复制旧版本各圆的具体数值，也未声称逐像素随机图样相同。完整观感/节奏已请求用户补充，未收到前保持candidate。

融合决策：加入ae-advanced-expressions的随机阈值单元，暂不拆成一个“圆形显隐”Skill。它与ae-procedural-motion共享已有Adobe执行/渲染工具，但不同于valueAtTime延迟。后续第9节三维随机位移可在同一随机表达式体系内扩充。
