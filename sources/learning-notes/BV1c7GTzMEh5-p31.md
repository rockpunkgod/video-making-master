# 来源2第31节：读取进度动画

[课程](https://www.bilibili.com/video/BV1c7GTzMEh5/?p=31)。实际视频2324.08秒、音轨1162.1545秒；18次全局和38次技术Watch帧查看，75张局部运动帧查看，包含重复。既有本机small模型336段语音完整读完，至1160秒；无安装、模型下载或音频上传。无声后半仅稀疏全局检查，不称完整重复或全部操作细节完成。

课程核心：15秒PAL720×576/1.09、25fps；LOADING在0/8/16帧100/50/100透明度，最后pingpong循环。Numbers使用Gulim Regular Horizontal Right，05:02–05:07连续帧确认最后Right，不能采用此前试选Center。Value表达式if(time<10)time*10;elsevalue，必须把原始Value设100；早先70导致完成后回落是明确教学故障。位置391/355、Size62、Decimal0可见。

550×50条形以左anchor缩放，x直接取NumbersValue，y取transform.scale[1]。条形上加4色渐变会一起缩放，课程明确否决；换独立调节层下移，仅染色条形，固定位置颜色不随长度改变。最后四点124446、345448、595451、3924798.4及红黄绿蓝可见。原生字段、过程/最终区别、推定边界见Skill参考及source-frame-provenance.json。

本机原生目录缺AdobeHeitiStd/Gulim，使用明确的标题ArialNarrow-Bold+111/130字形补偿和Numbers实际MicrosoftYaHeiUI Regular Right适配。Numbers字体选项会弹原生窗口，脚本参数枚举未给出setter；保留自制、无外部媒体的Numbers原生种子AEP，整Skill复制后已独立自动制作和渲染。不是从原课或安装目录抽取供应商项目。基线字形补偿为原片量测推定，不冒充原始TextScale。

已完成5例AEP/视频1750帧、71张原生PNG，三新PNG标题和改完成时间/时长/闪烁频率的独立调用。逐帧参数及影片几何/标题明暗/固定点颜色/数码原生检查点通过；调整层真实开关证明标题/数字不变、条形改变。冻结末帧负例被拒绝。源色相及坐标语义仍有差异；实际尝试坐标偏移假设效果更差，未应用，不凭猜测补全课程。

合并到高级表达式Skill的loading_progress单元，与数值/循环单元融合，并保留Numbers效果与SourceText不同实现。先展示原课18:16–18:21左右对照，左右5fps，右侧是按源合成时间码选择已有原生电影帧的评审重放，完整15秒电影和工程连续不变。源预览裁切与刷新滞后已说明，人工整体反馈待答。总18来源/166章节未完成。
