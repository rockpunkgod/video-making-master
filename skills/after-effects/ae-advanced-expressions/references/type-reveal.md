# 第14节：奇偶归位与随机淡入

来源：[Adding Type](https://www.bilibili.com/video/BV1Yh4y1A7XT/?p=14)。00:54字体DM Sans Bold160、Baseline Shift4；01:36文字Position[258,420]；04:05完整表达式；04:45原生Opacity0；04:48–04:52随机顺序与Advanced；05:10末关键帧位于00:00:00:29；06:03–06:08最终播放。用户对baseline002答“整体符合，可以保留”，仅绑定该成片SHA。精确源曲线与随机种子不因此成为已读参数。

先建立Point Text，白字黑底。Position Animator不用Range Selector，改Expression Selector，Based On Characters，Amount保留`if(textIndex%2) -100; else 100`。Animator Position Y=-79到0，奇数从下方、偶数从上方归位。再建独立Opacity Animator，Opacity0；Range Selector End100到0，Randomize Order On。Percentage、Characters、Add、Amount100、Square、Smoothness100、Ease High/Low0。动画属性和文字都保持原生可编辑。

明确显示：标题SUBPRIME、字号160、起点Position、Y=-79/0、Opacity0、End100/0、Randomize Order开启。项目面板显示1280×720、30fps、05:01，本机实际151帧。05:10光标00:00:00:29与两个末关键帧重合，按29帧建立基线。源Random Seed未读出，基线保留已实测本机默认0，不能称与源相同。

缓动：04:12出现Easy Ease In，随后手调速度图，不能用默认缓动冒充最终值。05:51 tooltip的End起点Speed=-104.23%/sec、Influence12.80%是当时状态，之后仍有拖动。直接把屏幕手柄长度占比当影响量的001试验使曲线过缓。002使用06:00最终速度图的十个手读采样，经本机End.valueAtTime差分拟合，得到out9%、in45%，RMS2.75%/sec；这是近似图形拟合，不是读取到了原关键帧。Position out14.5%/in36.2%也为画面估算，起速按距离/时长。所有估算在request内标明，保留001及拟合证据，不伪造精确源曲线。

运行：同Skill scripts/build_type_reveal.py --out全新目录，再run_ae.py --ae本机路径，最后render_ae.py --aerender本机路径 --reuse。--text/--font-size/--x/--y/--offset-y/--reveal-frames/--seed明确控制输入；示例见examples/type-reveal-profiles.json。字体必须实际匹配DMSans-Bold，缺失依随附会话字体工具检查，不静默替换。脚本不读取教程缓存或原库代码。参数改变是变体，不把新布局称课程原构图。

已实测基线及ALGORITHM、Motion 2026、AI三组不同文字，含大写、大小写/空格/数字、两字符短输入；三组均从独立副本、实验室外目录调用。它们构成本分支的三组新文字输入，不能外推为三种字体、中文、图片或任意版面泛化。当前只支持有限ASCII字母/数字/空格；长文需要显式调整排版，裁切风险会原生报错，不自动压缩字号掩盖。

原生检查151帧曲线单调、端点和稳定终态；真实修改文字、保存重开、恢复重开。渲染器自动调用validate_type_reveal.py，以实际视频的字符列带逐字符量测奇偶位移和渐显，固定1.25px质心误差门槛覆盖栅格化/编码，不用字幕推断动画。另检查开始空白、到点稳定、完整151帧解码。冻结终帧的真实反例被拒绝。该像素检查抽取8–9个关键帧，不声称每帧逐字符OCR或原片完全同步。每个案例另审10张实际视频帧。

排错：字体不符先检查宿主识别；文字裁切先显式减字号或改位置；首帧有字检查Opacity0和End100；奇偶方向错误检查表达式符号及Position Y；只有静态则检查两个Animator关键帧；随机排列改变先读Random Seed和宿主身份。AE有未保存工作时停止构建并保留。任何异常保留回执，另建新目录修复，不覆写已认可的baseline002。
