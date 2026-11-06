# 第12节程序化线路（candidate 0.1.0）

来源BV1Yh4y1A7XT?p=12。09:22完整createPath式；09:54能读到同一Shape Layer内Path1–12和一个Stroke，不是12个独立图层。11:34最终numPts50、Pos min50、Pos max139、seed55；Stroke2px，Mirror Reflection Center[540,540]、Angle0。红色FF0000、背景224/255和Layer Position[540,0]仍为视口推定值。

for(i=1;i<=pts;i++)，seedRandom(i+seed,true)后先取c=random()决定mul±1，再取y=random(min,max)，x=y*mul；奇数段oldEle+[0,y]，偶数段oldEle+[x,y]；初始vertices=[[0,0]]，末尾createPath(vertices,[],[],0)。点数为pts+1、开放路径、零切线。保留随机调用次序和源三元式，不擅改成曲线路径或任意角度。不同Property身份影响具体随机图样，未证明与原录屏每条线身份一致。

调用scripts/build_cyber_lines.py --out全新目录；可选--points2–100、--paths1–48、--seed0–10000、--step-min/--step-max(0≤min<max≤300)。然后以本目录run_ae.py和render_ae.py实际执行。所有图形仍为原生Path、Stroke、Slider和Mirror，无插件。该章节把Trim Paths动画明确留到后续最终项目，当前5秒静态视频只是布局验证载体，不能算动画通过。

本机实际Mirror为ADBE Mirror，中心/角度matchName为ADBE Mirror-0001/-0002。先查了默认值，再以三个已知红圆原生探针核对中心0/540/1080的可见结果。中心540时保留x439.5并生成x640.5，不能把整幅hflip的539.5轴当成同一像素映射；按x'=1080-x对比有效列1–1079，未搜索最佳拟合轴。

真实基线、seed0/min0/max100的课程内变参、5路径24点的稀疏变参均原生制作、保存重开、实际种子修改恢复通过。每条路径150帧检查点数、开放、竖直/±45度、段长范围与时间稳定性；另有五张字节一致的原生PNG。每组10张视频帧已审阅。独立亮度轮廓镜像IoU为0.9928/0.9829/0.9913，默认中心1080的实际原生负例0.0802被拒绝。源颜色/Transform值和整体审美仍未验收，三组参数不能冒充三组外部素材。

保留失败：sparse001的原点读回-0.0000152588，是Shape内部单精度表示；002按坐标尺度/浮点精度检查，不改[[0,0]]原式，也不把数值强制归零。RGB红色边缘受H2644:2:0采样影响，最初镜像掩码低于门槛，失败报告保留；改用全分辨率亮度几何和已实测中心，0.93门槛未放宽。validate_cyber_symmetry.py需已有Pillow/NumPy，只检查首帧；其余静态/原生150帧证据由独立检查提供，不宣称该首帧检查覆盖全部时序。

证据在tests/cyber-lines-results.json及evaluations/course-p12-probe-001/summary.json；原片对照仅在cache/reviews/p12-original-vs-baseline001-001。尚缺课程最终动画步骤与三组不同输入素材的泛化，保持candidate扩展，不扩大第5/6节verified范围。
