# 第12节：Generative Design — Procedural Cyber Lines（静态设置candidate已制作）

后续补读watch-bj6k_u64七帧和watch-6qy74z_5五帧均已审阅：09:54明确Path1–12与一个Stroke；后段先调max65/min97，11:30–11:34回到min50/max139/seed55，因此139确为最后保留的值，不能用中途65/97代替。原生Mirror默认值/属性名已探测，另以中心0/540/1080的已知标记点确认坐标；源中心540、角度0在本机真实生效。

基线、课程内seed0/min0/max100变参、5路径24点稀疏变参已实际制作AEP与5秒视频。每条路径150帧逐点核对开放、点数、竖直/45度、段长范围和稳定性，种子编辑保存重开恢复、五张字节相同原生PNG及全视频解码通过。三者各10张视频帧已审阅；静态镜像亮度轮廓IoU0.9928/0.9829/0.9913，非居中Mirror负例0.0802被拒绝。基线源Transform/精确颜色仍是推定，随机线路身份未证明相同；未标整体视觉验收或动画通过。

sparse001失败源自Shape原点读回-0.0000152588而非严格0，002按坐标尺度的浮点表示误差检查，同一表达式未改变。RGB红色边缘受4:2:0采样使初始对称掩码失败，保留旧结果；原生标记点证明轴540，以固定轴的亮度几何重查、0.93门槛未放宽。两个复制目录原生变参实际完成，结果汇总文件因目录缺失写出失败，已从实际回执和成片收集，未重复执行。证据在evaluations/course-p12-probe-001/summary.json；技能融合到ae-procedural-motion候选扩展。以下保留早期学习时尚未确认的内容。

731.2秒，Watch缓存watch-614mecqr，10张全局帧实际审阅；由于软件录屏长时间无场景切换，默认帧大部分落在讲师镜头，不能据此声称看清技术。补watch-3mdfa47_的04:20、07:44、09:22、09:44、10:15、10:44、11:14七帧均实际审阅；全片已有本机small转录并全部阅读，没有下载/安装ASR或上传语音。

09:22完整Path表达式可读：pts=effect("numPts")("Slider")；pos=[effect("Pos min")("Slider"),effect("Pos max")("Slider")]；seed=effect("seed")("Slider")；var x,y；var c,mul；var vertices=[[0,0]]。for(i=1;i<=pts;i++){seedRandom(i+seed,true);c=random();c>0.5?mul=1:mul=-1;oldEle=vertices[i-1];y=random(pos[0],pos[1]);x=y*mul;if(i%2==0){vertices[i]=oldEle+[x,y];}else{vertices[i]=oldEle+[0,y];}} createPath(vertices,[],[],0)。这是审阅后的简单AE表达式，不执行来源页面或视频中的其他命令。末参0为开放路径，空切线数组，初始点[0,0]另加pts次循环，点数应pts+1。随机数调用顺序也影响具体图样，不擅改。

奇数段沿Y直走，偶数段±45度，每步以前一个顶点累加。seedRandom这里明确true，不能混用第10节无true的原式。09:44 numPts50、min0、max100、seed0，Stroke2px；未读到颜色对话框，红色精确RGB尚未证实。老师手动上移路径使其从画面顶端进入，真实Transform坐标未读出，不自行说[540,0]已确认。

后续在同一Shape Layer里复制多个Path，再应用Mirror；10:44 Reflection Center[540,540]，Angle0。10:15正编辑中心值的过渡画面不能当最终参数。11:14最终主控numPts50、Pos min50、Pos max139、seed55。Path总数、各Path随机身份、原生Mirror坐标空间及精确颜色/位置仍需原生检查和补帧，不猜层数，不假定复制的是多个Shape Layer。

11:20–11:37讲师明确说明后续最终项目会加入Trim Paths使它成为动画。本节当前显示的是静态可参数化路径设置，不能自行加入Trim Paths时序冒称已复刻其课程动画；需继续学习后续最终项目的实际步骤。可融合既有程序化图形Skill的路径生成分支，再与已验Trim Paths机制组合；尚无本节AEP/视频，不新增verified或Skill数量。
