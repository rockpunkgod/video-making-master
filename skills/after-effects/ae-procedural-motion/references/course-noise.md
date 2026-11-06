# 第7节黑白数字块隧道（candidate）

来源：BV1Yh4y1A7XT第7节，00:39—05:09黑白阶段。01:20明确Strings/Block/Invert/Contrast2000/Complexity1；02:30显示seedRandom(5,true); random(1000)，复制到主合成后03:58显示种子1；04:28两个间距控制为0，04:50显示20个FN Multiply层。保留却禁用Opacity表达式，沿用第6节空间表达式和摄影机，不加入Trim Paths。

本机AE26中文界面已确认Strings枚举19（不是旧推测16，16实测是Terrain）、Block枚举1。脚本按matchName设置；换宿主先重查枚举，不能盲目套用。

调用顺序：先build_course_stage.py生成并通过run_ae.py保存trim-final工程；再build_course_noise.py --base该project.aep --out全新目录。使用本Skill的run_ae.py及render_ae.py执行。--seed默认1是主合成课程状态，tex_FN实验预合成保留seed5。读取基线的表达式后另存，不修改基线。旧版或非课程AEP拒绝。

本机实际样片为samples/course-reproduction-003/p07-blocks-002；原生检查20个不同且时间恒定的种子、全部210帧空间/演化、保存重开与种子编辑恢复通过，7秒原生H.264视频全解码且14张抽帧审阅。种子随机图样受AE层身份影响，不保证与旧课程像素相同。

此阶段尚缺三组泛化、独立目录执行和完整参考视觉验收，维持candidate，见tests/course-noise-results.json。PNG模板不可用时用本机已实测H.264模板；无支持模板则停止。失败001保留，不复用回执。

后续补看05:41—05:49的9张指定帧：05:43—05:46颜色框明确0057FF，FN15先由临时青色改成该蓝色，再将Tint复制给FN18。--course-tint按此完成两个图层着色，原生Tint的black/white/amount属性经默认值和真实matchName检查，保存重开后颜色通过；实际新视频samples/course-reproduction-003/p07-tint-001已210帧全解码、14张画面帧审阅，证据evaluations/course-p07-probe-001/tint-candidate.json。蓝色参数缺口已解决，整体视觉验收和三组泛化未完成，仍是candidate。

后续用户对上述Tint成片反馈“整体符合课程效果”，仅绑定该文件SHA d83aca3c…04196。另从samples/isolated-skill-005复制技能、在E:/自媒体调用seed7变体实际AEP/渲染，210帧解码、种子编辑恢复重开及14张画面帧审阅通过，见isolated-seed-variation.json。整体效果与独立调用缺口已补；仍缺三组不同输入素材的实际泛化，保持candidate。
