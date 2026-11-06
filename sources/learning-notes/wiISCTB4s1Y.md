# 三维摄像机跟踪流程

来源：https://www.youtube.com/watch?v=wiISCTB4s1Y ，Guerrilla Filmmaking。原语英文自动字幕与8个全局帧、8个技术定位帧已取证。并非已经复刻成功的Skill。

明确展示的工作流：

1. 01:20在复制的参考层上用Levels增强路面细节；当前画面的Input Black/White数值属于其32bpc素材，不能照搬至其他曝光或位深。
2. 01:45又加Unsharp Mask，预合成并移动全部属性，使跟踪参考增强与最终画面分离。
3. 02:10内置3D Camera Tracker完成103帧分析，Shot Type为Fixed Angle of View，Solve Method为Auto Detect，Method Used为Mostly Flat Scene，Average Error明确显示0.27 pixels。该误差只属于这段素材，不是可直接承诺的通用阈值。
4. 02:55选取路面点，右键Set Ground Plane and Origin，再创建Solid and Camera。
5. 03:25给Track Solid加Grid验证附着路面的效果，增大平面并预览观察漂移。
6. 04:45使用独立Normalize Track工具；05:15整理为多个彩色参考平面。该工具不是内置跟踪器按钮，当前尚未核实其安装、来源与接口。坐标归一化也不能替代求解误差检查。
7. 06:20把带Alpha火焰素材放入跟踪空间，对齐参考平面后再调整缩放和时间，最后关闭参考增强层，恢复底部原始画面。

抽象：参考增强→原生求解→地面/原点→测试网格→空间规范化→合成新元素→回到原片。失败诊断应区分特征不足、非刚体目标、纯旋转、滚动快门、错误平面、焦距变化和坐标尺度，不能把任何漂移都归因于“未归一化”。

本机能力探针确证内置效果matchName为ADBE 3D Tracker，另有Mocha AE与Keylight。尚未验证从脚本触发求解、读取点/误差或创建摄像机；这些步骤优先按实际接口检查，必要时GUI操作。未把知道matchName当作实际跟踪成功。
