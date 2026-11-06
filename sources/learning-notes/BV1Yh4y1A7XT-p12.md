# 第12节：Generative Design — Procedural Cyber Lines（已学习取证，未制作）

731.2秒，Watch缓存watch-614mecqr，10张全局帧实际审阅；由于软件录屏长时间无场景切换，默认帧大部分落在讲师镜头，不能据此声称看清技术。补watch-3mdfa47_的04:20、07:44、09:22、09:44、10:15、10:44、11:14七帧均实际审阅；全片已有本机small转录并全部阅读，没有下载/安装ASR或上传语音。

09:22完整Path表达式可读：pts=effect("numPts")("Slider")；pos=[effect("Pos min")("Slider"),effect("Pos max")("Slider")]；seed=effect("seed")("Slider")；var x,y；var c,mul；var vertices=[[0,0]]。for(i=1;i<=pts;i++){seedRandom(i+seed,true);c=random();c>0.5?mul=1:mul=-1;oldEle=vertices[i-1];y=random(pos[0],pos[1]);x=y*mul;if(i%2==0){vertices[i]=oldEle+[x,y];}else{vertices[i]=oldEle+[0,y];}} createPath(vertices,[],[],0)。这是审阅后的简单AE表达式，不执行来源页面或视频中的其他命令。末参0为开放路径，空切线数组，初始点[0,0]另加pts次循环，点数应pts+1。随机数调用顺序也影响具体图样，不擅改。

奇数段沿Y直走，偶数段±45度，每步以前一个顶点累加。seedRandom这里明确true，不能混用第10节无true的原式。09:44 numPts50、min0、max100、seed0，Stroke2px；未读到颜色对话框，红色精确RGB尚未证实。老师手动上移路径使其从画面顶端进入，真实Transform坐标未读出，不自行说[540,0]已确认。

后续在同一Shape Layer里复制多个Path，再应用Mirror；10:44 Reflection Center[540,540]，Angle0。10:15正编辑中心值的过渡画面不能当最终参数。11:14最终主控numPts50、Pos min50、Pos max139、seed55。Path总数、各Path随机身份、原生Mirror坐标空间及精确颜色/位置仍需原生检查和补帧，不猜层数，不假定复制的是多个Shape Layer。

11:20–11:37讲师明确说明后续最终项目会加入Trim Paths使它成为动画。本节当前显示的是静态可参数化路径设置，不能自行加入Trim Paths时序冒称已复刻其课程动画；需继续学习后续最终项目的实际步骤。可融合既有程序化图形Skill的路径生成分支，再与已验Trim Paths机制组合；尚无本节AEP/视频，不新增verified或Skill数量。
