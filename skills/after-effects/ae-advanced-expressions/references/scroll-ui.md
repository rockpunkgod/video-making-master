# 第26/27节：纵横滑页（仅准备，原生制作受阻）

来源：[第26节](https://www.bilibili.com/video/BV1c7GTzMEh5/?p=26)、[第27节](https://www.bilibili.com/video/BV1c7GTzMEh5/?p=27)。两节已读取实际音轨与关键画面；新代码尚未在AE执行成功，**没有该分支AEP、成片或通过的原生测试**。当前冷启动在脚本运行前遇CEP加载错误，ASCII路径诊断另遇简体中文语言授权提示。不要把已生成JSX/配置当作已完成制作。

## 必须保留的原法差异

第26节12:45–13:25可读：滑块自身Position为`x=299; y=transform.position[1]; [x,y]`。只锁X，**Y没有clamp**。内容Position：

```javascript
a=thisComp.layer("控制").transform.position[1];
linear(a,13,225,[161,328],[161,-223])
```

控制器向下、内容向上；控制器可越界，内容由linear钳在端点。08:36附近演示标量结果不能直接返回二维Position；10:52附近发现误写`linear=`导致不按预期运动，删除等号。这里的修复来自视频，不宣称已在本机重演该错误。

第27节：单独二维Null“控制”驱动可见滑块和内容。17:30–18:22可读滑块：

```javascript
scroll=thisComp.layer("控制").transform.position[0];
min_s=20; max_s=300;
x=clamp(scroll,min_s,max_s);
y=223;
[x,y]
```

15:30可读内容：

```javascript
scroll=thisComp.layer("控制").transform.position[0];
min_s=615; max_s=-280;
x=linear(scroll,20,300,min_s,max_s);
y=104;
[x,y]
```

615是正数，-280是负数。内容映射不能直接换成clamp；滑块输出/输入范围相同，才可用clamp替换其早期linear写法。表达式变量在各自属性内定义，不是图层间共享变量。Null的Y不控制内容，Null可移到范围外但滑块/内容停在端点。

## 准备好的调用方式

宿主恢复后，在实验室根目录创建全新输出，不复用失败目录：

```powershell
python skills/after-effects/ae-advanced-expressions/scripts/build_scroll_ui.py --axis vertical --out samples/runs/scroll-new
python skills/after-effects/ae-advanced-expressions/scripts/run_ae.py samples/runs/scroll-new/build.jsx --ae 'E:/自媒体/Adobe After Effects 2026/Support Files/AfterFX.exe'
```

**确认真实receipt/AEP成功后才调用**同目录render_ae.py及aerender。横向改`--axis horizontal`；`--profile`自定请求；`--asset PNG/JPG`复制新素材并在规范化内容预合成内按比例适配；`--text`替换文字；`--content-start/--content-end`改变内容范围；`--overshoot`生成明确的越界测试变体。范围可被构建器接受不代表已验证。

内容预合成、文字、两根轨道线、方块和Null均由原生脚本创建；结构参照原课，素材自制。纵向图片分支加轨道底板防止新图像盖住轨道，这是泛化适配。预期输出可编辑AEP、真实视频、10张原生检查PNG、原生轨迹/编辑恢复/视频像素检查记录；当前这些输出均未取得。

320×240画布与30fps由视口/时间线推定；纵向内容322×656、横向950×208、锚点、字体KaiTi、字号、轨道与方块尺寸未从源工程准确读出。外层3倍合成用于960×720交付，不作为原课设置。默认运动采样自26节12:42–12:48和27节17:17–17:23，5fps屏幕方块中心按约0.95比例换算，属于推定重放；原课两段均为手动拖动，没有源动画关键帧。横向可见滑块无法反推出Null的越界原始位置。

## 待执行验证与诊断

先做两个原法基线，再做两方向越界变参、三个不同图片各两方向；原生保存重开、修改/恢复控制输入，检查180帧方向公式。validate_scroll_ui.py准备独立读取真实视频轨道上的灰色方块，固定容差1.5设计像素；内容公式另由原生逐帧记录。该校验器尚无真实视频验证，不能称已通过。冻结视频负例、空间关系、可编辑性和人工对照也都待做。

标量/向量错误查二维返回值；不动先查是否误写`linear=`；纵向X飘移查锁定表达式；横向内容移动幅度错查是否把内容linear误换clamp；素材遮住轨道查图片规范化/底板。恢复宿主时保留脏工程与非本实验工程。不要通过更改授权、替换安装文件或用FFmpeg模拟成片绕过原生制作。
