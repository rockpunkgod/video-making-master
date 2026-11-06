---
name: ae-advanced-expressions
description: 使用AE表达式制作随机显隐、三维随机布局与漂移、可编辑数字/二进制序列，保留种子、阈值、空间范围与手动微调；当前为待验候选。
---

0.3.3为candidate，融合课程第8节阈值显隐、第9节三维随机布局/漂移、第10节循环数字序列，不能泛称已掌握全部高级表达式。第10节旧002–005失败保留；用户明确要左侧原版后，replay006按原片更新时点复现，收到“这次方向对，可以保留”。该反馈仅绑定006的方向与节奏，不代表绝对种子、逐字数字或全部泛化通过。

随机显隐读references/threshold.md，调用下述build_visibility.py；三维散布/漂移读references/displacement.md，调用build_displacement.py --out全新目录，可选--seed、--drift-speed、--asset。后者固定1920x1080、30fps、5秒，直接保留课程pos+drift+value；本机标量只作用X，不擅改成三个随机方向。

长数字或二进制先读references/number-sequences.md。复现已保留的原版演示节奏时，用build_sampled_number_animation.py --profile examples/p10-original-left-48-56.json --out全新目录，可选--seed-base换数字序列；同目录run_ae.py/render_ae.py负责原生制作、重开编辑与逐帧更新检查。输入Profile将观测时点和推定参数分开；初始300位仅显示9行的容量是本参考状态，其他新输入须先确认文字框容量。旧build_number_sequences.py三模式为历史/诊断，不能默认当作已解决的动画。字体缺失先检查随附OFL字体与会话加载工具，原生构建再次确认字体，禁止静默替换。结果边界见tests/number-sequence-results.json。

1. 选择圆形基础复刻或调用者自有PNG泛化，用scripts/build_visibility.py --out全新目录构建；默认消失38帧，--direction appear默认113帧，--seed改变排列，--asset复制PNG。
2. 本目录scripts/run_ae.py以目标AfterFX运行，要求真实AEP、保存重开、原生逐帧条件核对、实际种子编辑/恢复通过。
3. 本目录scripts/render_ae.py调用aerender输出视频；scripts/validate_video.py全解码；按tests/protocol.md检查画面。新输出单独验收。

显隐分支固定1080方形、30fps、5秒，原生图层可编辑。原生层身份影响伪随机序列，不承诺与旧课程某个圆的随机数字相同。不能把该显隐逻辑改成自制缓入曲线或逐层延迟作为课程基线。各单元均已实际制作和测试，具体通过项与缺口分别见tests/results.json、tests/displacement-results.json、tests/number-sequence-results.json；薄线/小字PNG在浅灰背景中的可读性未建立，不能当成熟前景文字排版技能交付。
