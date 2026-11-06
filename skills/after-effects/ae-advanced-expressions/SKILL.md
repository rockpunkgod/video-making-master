---
name: ae-advanced-expressions
description: 使用AE的seedRandom与条件表达式控制多图层随机显隐，提供可编辑种子、阈值、正反向关键帧；当前为待验候选。
---

当前只实现课程第8节的随机阈值显隐，状态candidate，不能泛称已掌握全部高级表达式。先读references/threshold.md确认来源和参数边界。

1. 选择圆形基础复刻或调用者自有PNG泛化，用scripts/build_visibility.py --out全新目录构建；默认消失38帧，--direction appear默认113帧，--seed改变排列，--asset复制PNG。
2. 本目录scripts/run_ae.py以目标AfterFX运行，要求真实AEP、保存重开、原生逐帧条件核对、实际种子编辑/恢复通过。
3. 本目录scripts/render_ae.py调用aerender输出视频；scripts/validate_video.py全解码；按tests/protocol.md检查画面。新输出单独验收。

固定1080方形、30fps、5秒，原生图层可编辑。原生层身份影响伪随机序列，不承诺与旧课程某个圆的随机数字相同。不能把该显隐逻辑改成自制缓入曲线或逐层延迟作为课程基线。
