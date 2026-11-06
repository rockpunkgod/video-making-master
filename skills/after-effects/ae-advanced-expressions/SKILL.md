---
name: ae-advanced-expressions
description: 使用AE表达式制作随机显隐、三维随机布局与漂移、可编辑数字/二进制序列，保留种子、阈值、空间范围与手动微调；当前为待验候选。
---

0.3.2为candidate，融合课程第8节阈值显隐、第9节三维随机布局/漂移、第10节循环数字序列，不能泛称已掌握全部高级表达式。第10节002/003被用户否决，静态004也被指出不是所需动画。p10-controls-animation-005虽已原生制作和检查，也被用户明确否决“仍不符合课程动画”。第10节没有已验收的动画；先定位用户要求的原片时间段，不能继续用自行编排替代课程。

随机显隐读references/threshold.md，调用下述build_visibility.py；三维散布/漂移读references/displacement.md，调用build_displacement.py --out全新目录，可选--seed、--drift-speed、--asset。后者固定1920x1080、30fps、5秒，直接保留课程pos+drift+value；本机标量只作用X，不擅改成三个随机方向。

长数字或二进制先读references/number-sequences.md。build_number_sequences.py默认course模式保留原式，存在逐帧换号，不作为已解决抖动的动画；--animation static只用于失败诊断。--animation controls-demo是固定8秒黑底白字控制器演示，timeless与HOLD关键帧属于明确的动画适配，尚不支持变参，不静默忽略输入。此模式原生逐帧核对控制器与文本变化，渲染器自动调用validate_controller_animation.py检查只在四个预定帧更新。字体缺失先检查随附OFL字体与会话加载工具，原生构建再次确认字体，禁止静默替换。结果边界见tests/number-sequence-results.json。

1. 选择圆形基础复刻或调用者自有PNG泛化，用scripts/build_visibility.py --out全新目录构建；默认消失38帧，--direction appear默认113帧，--seed改变排列，--asset复制PNG。
2. 本目录scripts/run_ae.py以目标AfterFX运行，要求真实AEP、保存重开、原生逐帧条件核对、实际种子编辑/恢复通过。
3. 本目录scripts/render_ae.py调用aerender输出视频；scripts/validate_video.py全解码；按tests/protocol.md检查画面。新输出单独验收。

显隐分支固定1080方形、30fps、5秒，原生图层可编辑。原生层身份影响伪随机序列，不承诺与旧课程某个圆的随机数字相同。不能把该显隐逻辑改成自制缓入曲线或逐层延迟作为课程基线。各单元均已实际制作和测试，具体通过项与缺口分别见tests/results.json、tests/displacement-results.json、tests/number-sequence-results.json；薄线/小字PNG在浅灰背景中的可读性未建立，不能当成熟前景文字排版技能交付。
