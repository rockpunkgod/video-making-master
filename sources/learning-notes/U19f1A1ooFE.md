# 四个表达式的知识融合

来源：https://www.youtube.com/watch?v=U19f1A1ooFE ，ukramedia，Ben Marriott参与。已取得YouTube英文自动原语字幕；已审阅24个全局帧及13个技术定位帧。场景抽帧偏重片头宣传，补充05:30至16:00的定位帧后才能确认操作。

明确画面证据：

- 05:30：Effects层Turbulent Displace的Random Seed用time驱动；镜头是剑形图案的边缘变形。06:20显示time*4，字幕说明改变种子变化速度。
- 08:50：Transform效果的Position使用wiggle(12,1)，用于非常小幅的手绘感抖动。不是大幅镜头抖动，也不是弹簧系统。
- 11:10：Diamond作为String的子层，Rotation引用String.rotation*-1。该操作抵消父级旋转，作用与延迟阵列不同，可保留为绑定变体。
- 14:30：重复楔形图层以index*11.2控制旋转，形成展开扇形；其优势是复制层自动分布，劣势是插层会改变index。

抽象与合并决定：不为四个简单表达式分别新建Skills。index分布与已验证的ae-procedural-motion存在原理重合，可作为另一来源支持；本实验室采用显式Order防止插层改变序号。时间驱动噪声、小幅抖动及抵消父级旋转保留为待测试变体，不扩大现有verified技能范围。

尚未完成：05:30附近的全部效果参数未逐项复刻；四种变体尚无独立原生测试。字幕自动识别错误与录屏未清楚展示的设置不能直接补全。本条课程技术方向已识别，保持partially_analyzed，不能标记所有制作已验证。
