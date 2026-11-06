# 第15节空间条带：部分流程重建的候选

来源https://www.bilibili.com/video/BV1Yh4y1A7XT/?p=15 ，09:00–11:56，最后深度修改19:20–19:40。此分支不是已完成课程验收的Skill，不得绕过下列不确定项用于宣称精确复刻。

已观察：Fractal Noise Strings/Block/Invert，Contrast2000、Complexity1，09:47非等比Width24.6/Height2270；11:41多个图层Scale503%；11:05及19:25空间控制器seed713、driftSpeed0、Y Min=Max=540，最终X范围-1084..3130、Z范围0..2000。之前Z1930..8890和seed541/721是过程值。Camera1保留但关闭，使用默认摄影机。16层时间轴扣除Camera1与controls，推定14个噪波实体。

讲师复制前课Position属性与控制器，未展开粘贴后的完整代码。本候选沿用前课已读到的seedRandom(seed,1)、random(posMin,posMax)、标量drift及末尾`pos+drift+value`。将Position底值设为0，是根据前课属性与粘贴后Y540结果作出的重建，未在本节界面直接读到。旧Scale表达式的处理过程也未展示；本候选用常量503替换，匹配可见结果，不能称该替换是课程明确操作。

保留原生3D噪波图层和Multiply，演化为前课`time*5`，并非把视频平铺或用静帧模拟。独立调用scripts/build_streaks.py --out全新目录，再run_ae.py和render_ae.py。默认examples/course-streaks.json复用本Skill自制的噪波AEP，先核SHA，复制到输出inputs。--seed、--count、--scale、--depth为显式变体，写入请求及计划。

原生验证：每层210帧的位置漂移应为0、Y540、X/Z在所选范围、Scale恒定、Evolution=time*5；实际改动seed、保存重开再恢复，并核对位置变化。全视频解码与四个原生PNG对照只检查技术一致性，不证明课程视觉一致。基线14层，已从独立Skill副本完成10层、seed714、Scale420、Z0..1300的真实工程及视频。

目前没有三个不同素材的泛化证据，也没有总装后的课程对照结论；随机噪波身份不保证同源。外观过粗时先核对缩放与透视深度，再核对源图层噪波身份；不能悄悄调整Width来让截图更像。旧表达式因控制器被替换而失效时应明确报错、保留失败记录，不能填造已观察的修复步骤。

进入主合成时，19:40条带Z=-17230是比19:18的-16540更晚的可见值；加白色Linear Color Key，collapse按课程选择。该总装工作未包含在本分支中。
