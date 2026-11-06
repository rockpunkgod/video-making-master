---
name: ae-advanced-expressions
description: 使用AE的seedRandom制作多图层随机显隐、三维随机布局与漂移，保留种子、阈值、3D范围和手动位置微调；当前为待验候选。
---

0.2.0为candidate，覆盖课程第8节阈值显隐与第9节三维随机布局/漂移两个单元，不能泛称已掌握全部高级表达式。

随机显隐读references/threshold.md，调用下述build_visibility.py；三维散布/漂移读references/displacement.md，调用build_displacement.py --out全新目录，可选--seed、--drift-speed、--asset。后者固定1920x1080、30fps、5秒，直接保留课程pos+drift+value；本机标量只作用X，不擅改成三个随机方向。

1. 选择圆形基础复刻或调用者自有PNG泛化，用scripts/build_visibility.py --out全新目录构建；默认消失38帧，--direction appear默认113帧，--seed改变排列，--asset复制PNG。
2. 本目录scripts/run_ae.py以目标AfterFX运行，要求真实AEP、保存重开、原生逐帧条件核对、实际种子编辑/恢复通过。
3. 本目录scripts/render_ae.py调用aerender输出视频；scripts/validate_video.py全解码；按tests/protocol.md检查画面。新输出单独验收。

显隐分支固定1080方形、30fps、5秒，原生图层可编辑。原生层身份影响伪随机序列，不承诺与旧课程某个圆的随机数字相同。不能把该显隐逻辑改成自制缓入曲线或逐层延迟作为课程基线。两个单元均已实际制作和测试，具体通过项与缺口见tests/results.json、tests/displacement-results.json；薄线/小字PNG在浅灰背景中的可读性未建立，不能当成熟文字排版技能交付。
