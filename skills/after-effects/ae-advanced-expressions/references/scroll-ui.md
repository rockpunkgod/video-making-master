# 第26/27节：纵横滑页（原生候选，课程人工评审待答）

来源：[第26节](https://www.bilibili.com/video/BV1c7GTzMEh5/?p=26)、[第27节](https://www.bilibili.com/video/BV1c7GTzMEh5/?p=27)。两节已读取实际音轨与关键画面，并实际完成11个可编辑AEP及成片。1980帧原生公式/全视频解码和滑块像素轨迹通过；三种原创图片各两方向、越界变参、独立复制调用通过。110张原生检查PNG已以联系表查看。课程整体人工反馈待答，仍candidate；准确原课布局与手动轨迹不因此得到证明。

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

## 调用方式

在实验室根目录创建全新输出，不复用失败目录：

```powershell
python skills/after-effects/ae-advanced-expressions/scripts/build_scroll_ui.py --axis vertical --out samples/runs/scroll-new
python skills/after-effects/ae-advanced-expressions/scripts/run_ae.py samples/runs/scroll-new/build.jsx --ae 'E:/自媒体/Adobe After Effects 2026/Support Files/AfterFX.exe'
```

**确认真实receipt/AEP成功后才调用**同目录render_ae.py及aerender。横向改`--axis horizontal`；`--profile`自定请求；`--asset PNG/JPG`复制新素材并在规范化内容预合成内按比例适配；`--text`替换文字；`--content-start/--content-end`改变内容范围；`--overshoot`生成明确的越界测试变体。范围可被构建器接受不代表已验证。

内容预合成、文字、两根轨道线、方块和Null均由原生脚本创建；结构参照原课，素材自制。纵向图片分支加轨道底板防止新图像盖住轨道，这是泛化适配。预期输出可编辑AEP、真实视频、10张原生检查PNG、原生轨迹/编辑恢复/视频像素检查记录；这11例均已取得上述输出；未测试的其他输入不可直接声称通过。

320×240画布与30fps由视口/时间线推定；纵向内容322×656、横向950×208、锚点、字体KaiTi、字号、轨道与方块尺寸未从源工程准确读出。外层3倍合成用于960×720交付，不作为原课设置。默认运动采样自26节12:42–12:48和27节17:17–17:23，5fps屏幕方块中心按约0.95比例换算，属于推定重放；原课两段均为手动拖动，没有源动画关键帧。横向可见滑块无法反推出Null的越界原始位置。

## 已执行验证与剩余边界

两个原法基线、两方向越界变参、三个不同图片各两方向、独立复制Skill后的文字/内容范围变化，共11例。原生保存重开、修改/恢复控制输入及每例180帧方向公式通过。validate_scroll_ui.py读取实际视频轨道灰色方块，最大误差0.845设计像素，容差仍1.5；内容公式另由原生逐帧记录，未声称逐像素验证所有正文。竖向越界时实际只露1像素的三帧曾被成组门槛漏检，保留初次失败JSON，修复仅允许贴边短组；动画未改变。两条冻结负例实际拒绝，11工程真实媒体审计无缺失。

当前实例固定6秒/30fps/960×720，KaiTi需已安装；图片为PNG/JPG等比适配。尚未验证任意素材尺寸、不同画幅/时长/字体、视频输入或重排适配。参考视频只本机对照，不分发。用户视觉认可只绑定所评基线SHA，未答前不得提升verified。启动恢复和二次冷启动原生探针见references/host-startup.md。

标量/向量错误查二维返回值；不动先查是否误写`linear=`；纵向X飘移查锁定表达式；横向内容移动幅度错查是否把内容linear误换clamp；素材遮住轨道查图片规范化/底板。恢复宿主时保留脏工程与非本实验工程。不要通过更改授权、替换安装文件或用FFmpeg模拟成片绕过原生制作。
