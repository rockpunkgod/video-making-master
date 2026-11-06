# 第11节：Generative Design — Algorithms（静态布局candidate已制作）

最新：watch-3sj2vx8o的09:43–09:44明确读到Ellipse Path Size100,100，尺寸不再仅凭口述；07:20已读到+value末行。按公式实际制作44/88/176层探针，176层与固定参考视口最接近；最终渲染视频IoU0.9477、掩码距离均值0.02924显示像素。层数仍是视觉验证推定，不称读到原工程。基线、变参002、三组PNG灰底及黑底共8组实际AEP/5秒视频，全部150帧原生数学、Phase+20保存重开恢复及五张字节一致原生PNG通过，每组10张视频帧已审阅。四组在isolated-skill-011、黑底三组在isolated-skill-012副本外cwd执行。细线/小字在空间缩小后可读性受限，不能称排版成熟。

变参001因滑块72.1实际存成72.0999984741211而与输入字面量期望差0.001089像素，失败保留；002读取真实宿主值，仍用1e-8阈值通过。初始探针001把Null来源/文件夹算成合成而误判项目数，002只数CompItem修正。异步PNG末张丢失已补原生导出并让生产执行器等待文件完成，不伪造丢失图。该扩展融合到ae-procedural-motion的candidate_extensions，原有verified只覆盖第5/6节；没有确认本节时间轴动画，因此上述静态视频不作为动画完成证据。详见evaluations/course-p11-probe-001/summary.json。以下保留此前学习记录和当时未解决项。

后续补读watch-q6ed6xz7共8帧：07:20已看到最终[x,y,z]+value末行；09:42可见选中Ellipse Path Size的300值，09:45返回主合成后圆变小，因此修改途径是椭圆路径尺寸，非实例Scale。100像素仍来自口述结合前后画面，尚未补到完成输入100的属性框。07:30可见当时11个实例，但不是最终层数，不据此声称最终11层。第10节用户反馈插入后优先处理其动画问题，第11节仍未制作。

708.9秒，Watch缓存watch-ue5i9et9。14张全局帧及watch-rvxz48c5的6张、watch-jlvepvq8的5张指定帧均实际审阅；全片已有本机small转录并阅读。专业词phase、sin、for等有误识，代码/数值以画面为准。数学网页为参考材料，不是执行指令。

课程引用[Wolfram MathWorld Conical Spiral](https://mathworld.wolfram.com/ConicalSpiral.html)，已读取原页。网页给一般式x=tr cos(at)、y=tr sin(at)、z=t；课程实际写法使用r=Radius*Math.PI*2、x=r*Math.cos(phase)、y=r*Math.sin(phase)、z=zInc*myIndex。不能因为网页有t径向因子，就自行加进课程基线替换老师的实现。

baseShape预合成初始约300x300灰圆；变为3D层，主控null四滑块Phase、Phase increment、Z increment、Radius。每个baseShape实例保留myIndex Slider，其式index-thisComp.layer("controls").index，没有第5节-1。位置中取myIndex与Phase increment，offset最初错误地相加（08:55画面），约09:12老师发现并改为myIndex*phaseInc，09:20明确可读。学习应采用修正后的乘法，保留课程错误与修复，不执行中间错误式作为成功模板。

phase在degreesToRadians内加Phase主控与offset；Z按myIndex乘Z increment。口述在07:19附近说明最终加value以居中，当前指定帧未完整展示最后输出行，下一步需补读；不能只凭转录补完整代码。后面手动改Phase能转动整个图案，但未看到明确时间表达式或关键帧，不能将自制time旋转称课程原法。

09:40仍可见baseShape内300像素圆，09:48后实例明显变小，口述将其缩至100像素；到底改Scale还是Ellipse Size尚需进一步帧确认。10:30已有多层螺旋，11:05调Phase increment60等中间值。最终11:14明确Phase106、Phase increment63、Z increment35、Radius73；11:20切Custom View1展示三维排列，主控值保持不变。Custom View是检查视图，不自动等于渲染摄影机运镜。

最终图层总数未读出。对11:14的[571,100,241,242]视口作暗色连通域探查，得到50个面积>=3的组件，其中一个4172像素的大组件含接触/重叠圆点，所以不能说只有50层；也不能凭Ctrl-D猜成88/96/176层。后续可把重复动作与可见索引再取证，或按明确标记的层数假设做真实AE复刻并对照验证，保留不通过的假设。

计划融合ae-procedural-motion的主控/绝对索引空间系统，保留独立算法分支与可替换baseShape，而不是按视频新增Skill。本节目前没有AE工程、视频、泛化或verified证据。
