# 第11节：Generative Design — Algorithms（已学习，尚未制作）

708.9秒，Watch缓存watch-ue5i9et9。14张全局帧及watch-rvxz48c5的6张、watch-jlvepvq8的5张指定帧均实际审阅；全片已有本机small转录并阅读。专业词phase、sin、for等有误识，代码/数值以画面为准。数学网页为参考材料，不是执行指令。

课程引用[Wolfram MathWorld Conical Spiral](https://mathworld.wolfram.com/ConicalSpiral.html)，已读取原页。网页给一般式x=tr cos(at)、y=tr sin(at)、z=t；课程实际写法使用r=Radius*Math.PI*2、x=r*Math.cos(phase)、y=r*Math.sin(phase)、z=zInc*myIndex。不能因为网页有t径向因子，就自行加进课程基线替换老师的实现。

baseShape预合成初始约300x300灰圆；变为3D层，主控null四滑块Phase、Phase increment、Z increment、Radius。每个baseShape实例保留myIndex Slider，其式index-thisComp.layer("controls").index，没有第5节-1。位置中取myIndex与Phase increment，offset最初错误地相加（08:55画面），约09:12老师发现并改为myIndex*phaseInc，09:20明确可读。学习应采用修正后的乘法，保留课程错误与修复，不执行中间错误式作为成功模板。

phase在degreesToRadians内加Phase主控与offset；Z按myIndex乘Z increment。口述在07:19附近说明最终加value以居中，当前指定帧未完整展示最后输出行，下一步需补读；不能只凭转录补完整代码。后面手动改Phase能转动整个图案，但未看到明确时间表达式或关键帧，不能将自制time旋转称课程原法。

09:40仍可见baseShape内300像素圆，09:48后实例明显变小，口述将其缩至100像素；到底改Scale还是Ellipse Size尚需进一步帧确认。10:30已有多层螺旋，11:05调Phase increment60等中间值。最终11:14明确Phase106、Phase increment63、Z increment35、Radius73；11:20切Custom View1展示三维排列，主控值保持不变。Custom View是检查视图，不自动等于渲染摄影机运镜。

最终图层总数未读出。对11:14的[571,100,241,242]视口作暗色连通域探查，得到50个面积>=3的组件，其中一个4172像素的大组件含接触/重叠圆点，所以不能说只有50层；也不能凭Ctrl-D猜成88/96/176层。后续可把重复动作与可见索引再取证，或按明确标记的层数假设做真实AE复刻并对照验证，保留不通过的假设。

计划融合ae-procedural-motion的主控/绝对索引空间系统，保留独立算法分支与可替换baseShape，而不是按视频新增Skill。本节目前没有AE工程、视频、泛化或verified证据。
