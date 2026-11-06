---
name: ae-advanced-expressions
description: 使用AE表达式制作显隐、三维布局、数字、文字、弹簧、双翅和放大镜；纵横滑页与滑块三维旋转、圆周投影和自转。各分支保留明确的候选验证边界。
---

0.10.0为candidate。十个单元有各自原生证据；第二套第26/27节滑页新增11例可编辑工程/视频、1980帧、三种图片双方向与独立复制调用，课程整体人工反馈仍待答。不能泛称已掌握全部高级表达式。第10节旧002–005失败保留；replay006收到“这次方向对，可以保留”，仅绑定006方向与节奏，不代表绝对种子、逐字数字或全部泛化通过。

无关键帧圆周运动先读references/orbit-projections.md，用scripts/build_orbit_projections.py --out全新目录及同目录run_ae.py/render_ae.py。保留独立cos/sin/add位置、X/Y控制点、辅助线父级和(time/Math.PI)*360自转；6例1800帧、三图片、反向/改半径和独立调用通过。固定画幅时长，原课素材/色彩和精确同步未证实，整体反馈待答。

滑块驱动三维文字旋转先读references/rotation-slider.md，用scripts/build_rotation_slider.py --out全新目录及同目录run_ae.py/render_ae.py。第28节原嵌套if边界缺陷实际保留，>=修复另列变体；8例720帧、三种新矢量和独立调用已实做。六ASCII字符/固定画幅时长；相机与布局为测量推定，整体反馈待答。原生开关图核验运动模糊，不靠单独开关值声称有效。

纵横滑页先读references/scroll-ui.md，再用scripts/build_scroll_ui.py --axis vertical或horizontal --out全新目录，以及同目录run_ae.py/render_ae.py。保留纵向自由Y+向量linear、横向独立Null+clamp滑块/linear内容的区别。原课手动拖动，视频是采样重放；画布/字体/布局推定，不能当源工程身份。原生和像素验证边界见tests/scroll-ui-results.json。若AE冷启动CEP失败，先读references/host-startup.md；启动工具只补子进程缺失Windows环境，不修改系统或授权。

随动放大镜读references/magnifier.md，调用scripts/build_magnifier.py --out全新目录，再用run_ae.py/render_ae.py。保持课程2000调节层/减法圆形Mask/Fast Blur/Bulge中心联动；原课手动拖动，视频位置关键帧为明确标注的采样重放。5例750帧与原生效果开关对照已检查，支持文字和PNG/JPG；字体/画布/镜框及轨迹有推定，光学效果待反馈，仍candidate。

双翅铰链循环先读references/butterfly-rig.md，用scripts/build_butterfly_rig.py --out全新目录，再用run_ae.py/render_ae.py执行。保留课程四键pingpong、左翅取反、二维父对象带动三维部件和原生路径朝向。6例1200帧通过技术检查；素材/摄像机/精确键值有推定，整体运动待反馈，Particular缺失导致整节粒子拖尾尚未制作。当前只支持四组自制图形，不宣称任意外部翅膀素材适配。

水平弹簧连接先读references/spring-connector.md，调用scripts/build_spring_connector.py --out全新目录，再用同目录run_ae.py/render_ae.py实际执行。保持课程宽度归一化、正弦位移与线性振幅归零；不换成惯性模板。支持自制图形和固定高度透明PNG；7例1320帧完成原生及像素检查，课程整体人工评审待回复，仍为candidate。范围和失败修复见该参考及tests/spring-connector-results.json。

奇偶字符上下归位/随机淡入读references/type-reveal.md，用scripts/build_type_reveal.py --out全新目录；同目录run_ae.py/render_ae.py实际执行并核对字符位移。第14节baseline002收到“整体符合，可以保留”；三组新文字输入实测，但曲线估算、源种子未读和有限Latin范围须保留，不因此升级整个Skill为verified。证据见tests/type-reveal-results.json。

随机显隐读references/threshold.md，调用下述build_visibility.py；三维散布/漂移读references/displacement.md，调用build_displacement.py --out全新目录，可选--seed、--drift-speed、--asset。后者固定1920x1080、30fps、5秒，直接保留课程pos+drift+value；本机标量只作用X，不擅改成三个随机方向。

长数字或二进制先读references/number-sequences.md。复现已保留的原版演示节奏时，用build_sampled_number_animation.py --profile examples/p10-original-left-48-56.json --out全新目录，可选--seed-base换数字序列；同目录run_ae.py/render_ae.py负责原生制作、重开编辑与逐帧更新检查。输入Profile将观测时点和推定参数分开；初始300位仅显示9行的容量是本参考状态，其他新输入须先确认文字框容量。旧build_number_sequences.py三模式为历史/诊断，不能默认当作已解决的动画。字体缺失先检查随附OFL字体与会话加载工具，原生构建再次确认字体，禁止静默替换。结果边界见tests/number-sequence-results.json。

1. 选择圆形基础复刻或调用者自有PNG泛化，用scripts/build_visibility.py --out全新目录构建；默认消失38帧，--direction appear默认113帧，--seed改变排列，--asset复制PNG。
2. 本目录scripts/run_ae.py以目标AfterFX运行，要求真实AEP、保存重开、原生逐帧条件核对、实际种子编辑/恢复通过。
3. 本目录scripts/render_ae.py调用aerender输出视频；scripts/validate_video.py全解码；按tests/protocol.md检查画面。新输出单独验收。

显隐分支固定1080方形、30fps、5秒，原生图层可编辑。原生层身份影响伪随机序列，不承诺与旧课程某个圆的随机数字相同。不能把该显隐逻辑改成自制缓入曲线或逐层延迟作为课程基线。各单元均已实际制作和测试，具体通过项与缺口分别见tests/results.json、tests/displacement-results.json、tests/number-sequence-results.json；薄线/小字PNG在浅灰背景中的可读性未建立，不能当成熟前景文字排版技能交付。
