# 第14节：Adding Type（候选动画已制作，基线整体效果获认可）

续作补读watch-rawvq3su九帧和watch-_w6n3bq7六帧：04:45实际Opacity0；05:10光标00:00:00:29与两个结束关键帧重合；05:51的End速度提示后仍有拖动，不能当最终Influence。06:00最终速度图手读十点，经实际原生插值差分拟合得到End out9/in45，RMS2.75%/sec；仍是近似。Position out14.5/in36.2也是估算，源Random Seed未读，保留本机实际默认0。先前把速度图手柄长度当影响量的001已保留，002修正曲线。

已完成baseline002真实151帧AEP/MP4、文字编辑保存重开恢复、逐帧原生曲线检查、实际视频字符位移检测。用户先看06:03–06:08原版与002对照后答“整体符合，可以保留”，仅绑定SHA552cfc459177e3e48b3c74c0946d2a70fa386ccf3dededc07458736ef5c551ec；不因此声称精确源参数。另三组新文字ALGORITHM、Motion 2026、AI从独立Skill副本制作，均真实工程/渲染通过，三组文字不外推到其他字体或中文。四组各10张真实视频帧已审阅，质心位移最大误差均<0.046px；冻结终帧负例被检测拒绝。证据evaluations/course-p14-probe-001/summary.json，分支并入高级表达式0.4.0，整体仍candidate。下文保留最初取证时的未知项，以本段后续核实为准。

为查最终项目的文字动画，先读取本节；第13节Compositing尚未学习，不把目录跳读写成完整覆盖。388.8秒，Watch缓存watch-o_43y1u2，9张全局帧实际审阅；全片现有本机small转录共66段已全部阅读。再审watch-hvhgqlek的00:54、01:36、02:56、04:05、04:52、05:28、05:51七帧，技术操作以画面为准。

标题为SUBPRIME（8字符），DM Sans Bold160px、Baseline Shift4px、白字黑底。项目面板title显示1280×720、30fps、时间码0:00:05:01；时长需按后续原生设置/读回核实，不简写成5秒。01:36可见文字层Position[258,420]、Anchor[0,0,0]，属于当前英文标题构图，不能直接当任意输入的中心对齐公式。

删除Position Animator的Range Selector，增加Expression Selector，Based On Characters。02:56仍在输入else1，属于不完整中间画面；04:05能读到完整Amount式if(textIndex%2) -100; else 100。奇数返回-100，偶数100。Animator Position先300作解释，再在04:05看到Y=-79，最终05:51为0；负Y乘奇数负选择量使奇数字符从下方开始，不能把方向机械写反。

另建Opacity Animator，口述Opacity0；需再补属性值实际画面。Range Selector Advanced显示Percentage、Characters、Add、Amount100、Square、Smoothness100、Ease High/Low0，Randomize Order On。End按口述从100→0，05:28/05:51分别可见100/0；原生Random Seed具体值未读到，不猜。最终位置/End关键帧端点看似0至约1秒，尚未选中读时间，不把图上估算当精确关键帧时刻。

05:51速度图提示Speed -104.23%/sec、Influence12.80%。按百分比单位和时间轴推定是End属性的一个手柄，仍需核对选择状态及另一个手柄；不能套用第6节Easy Ease In的默认曲线替代本节实际调速结果。后续应先补帧，再探测本机原生文字Animator/Expression Selector/Range Selector的真实matchName与行为。该节目前没有AEP或渲染，不新增verified，不以两帧字幕判断完成动态文字技能。
