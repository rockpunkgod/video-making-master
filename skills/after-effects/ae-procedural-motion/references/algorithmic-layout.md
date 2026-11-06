# 第11节算法三维布局扩展（candidate 0.1.0）

本分支生成课程的可编辑三维排列；课程11:14参考停在第0帧，未看到明确播放/关键帧。5秒视频是静态布局检查载体，不冒称完成课程动画，也不继承第5/6节已验收的动画范围。

来源：BV1Yh4y1A7XT?p=11。07:20末行明确[x,y,z]+value；09:20将错误的myIndex+phaseInc改为myIndex*phaseInc；09:43–09:44椭圆路径Size为100,100；11:14主控Phase106、Phase increment63、Z increment35、Radius73。每层myIndex=index-thisComp.layer("controls").index，无-1。

位置原式：offset=myIndex*phaseInc；phase=degreesToRadians(Phase+offset)；r=Radius*Math.PI*2；x=r*Math.cos(phase)、y=r*Math.sin(phase)、z=Z_increment*myIndex；[x,y,z]+value。底层是XY恒定半径、Z按索引递增的空间排列。不要因课程引用数学网站的圆锥螺旋式，擅加t径向因子；Radius滑块是原式输入，实际XY半径还要乘2π。默认Active Camera没有显式CameraLayer，Custom View切换不是成片摄影机运动。

baseShape为300方形预合成，内部100像素灰圆，主合成1080方形30fps5秒、16bpc。灰圆100/255和背景224/255仍为推定颜色。最终层数未从源工程读出：实际AE制作44/88/176层，在固定241方形视口、无拟合下，IoU分别0.621/0.814/0.947，176层最接近；由此采用176作为经视觉检验的推定，不宣称唯一解或已读到原总数。

调用scripts/build_algorithmic_spiral.py --out全新目录；可设--count(1–300)、--phase(度)、--phase-step(度)、--z-step(像素)、--radius(原滑块单位)。--asset PNG为明确素材替换；原图复制至assets，100像素宽高适配并保留baseShape。--background black是改善灰底低对比度的独立变体，不改变圆形基线。细线和文字在远处缩小仍不可读，文字仅作装饰布局输入，不声称文字传达质量通过。

用本目录run_ae.py调用AfterFX，再render_ae.py调用aerender。宿主可能在saveFrameToPng返回后继续写PNG，因此构建结束后保留工程打开，由执行器等待五张原生图存在且文件大小稳定，避免过早关闭导致最后一张丢失。保留失败探针，不用重复启动覆盖旧工程。

每组逐帧验证myIndex及3D Position，实际Phase修改+20、保存重开再恢复重开。对150帧静态布局另取0/1/2/3/4秒原生PNG，五个文件必须字节一致；视频验证的static_layout契约要求这些证据，不用H264压缩带来的缩略图哈希变化冒充动画。PNG演示必须连同原生导出保留，方便重验。

时间检测改为先做64方形面积平均，再计算相邻帧平均亮度差，0.1门槛用于粗略运动存在性，不能评价局部亚像素运动或审美。全分辨率直接差分曾将静态纹理的压缩残差0.136616当成变化，该失败检查保留；降采样后同一文件0.0314941。已回查五组真实第6节运动视频及五组本节静态视频，并确认本节静态基线以“必须有动画”请求会被拒绝，见temporal-gate-regression.json。静态成功还必须具备五张字节一致的原生PNG和150帧原生位置检查，不能仅凭小差分通过。

变参时AE滑块会存储浮点量化值，例如72.1实际读为72.0999984741211。001变参按输入字面量预测，产生0.001089像素差，失败保留；002按宿主读回值计算独立期望，仍用1e-8门槛，通过。未通过放宽误差阈值掩盖问题。

当前基线及一组变参、三组PNG的原生工程和视频已制作；后四组经复制Skill在实验室外cwd执行。灰底PNG三组对比度低；另制作黑底三组比较，文字缩小可读性仍受限。全部8组各10张视频帧已审阅，技术检测与审美限制分开。最终渲染视频与课程暂停视口的IoU0.9477、对称掩码距离均值0.02924显示像素，仅证明这一静态轮廓接近。详情见tests/algorithmic-layout-results.json；原片对照位于本机cache/reviews/p11-original-vs-baseline001-001，不分发原教程片段。
