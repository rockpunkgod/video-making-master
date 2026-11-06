# 来源2第32节：云遮烈日

课程：https://www.bilibili.com/video/BV1c7GTzMEh5/?p=32 。视频3001.44秒、音轨1500.8425秒。已查看18次全局帧和28次技术帧（包含重复），本机既有small模型转录的330段有声内容全文已阅读；无新安装或上传。无声后半仅稀疏全局检查，不断言全部重复内容或全部细节已学完。

明确技术：Fractal Noise亮度遮罩白色固态层形成透明云预合成，sampleImage半径[2,2]读取Alpha[3]，将0..1线性映射到耀斑Brightness100..50。最终云偏移time*60。参数和时间戳、过程与最终值差异见Skill references/cloud-occlusion.md。课程实际使用Optical Flares和Golden Sun；本机实际宿主效果目录及已安装插件目录未发现该插件，原版制作阻塞。05:37口述允许选其他镜头光晕插件，所以仅制作明确声明的内置LensFlare变体，不能充当课程原版完成。

真实原生测试发现sampleImage在同步循环中未稳定，保留失败回执与原生渲染顺序探针；改用scheduleTask分阶段源Alpha/主合成渲染及读回。变体的素材泛化、技术检查和人工反馈分别记录；不把像素检查通过当作Golden Sun视觉一致。
