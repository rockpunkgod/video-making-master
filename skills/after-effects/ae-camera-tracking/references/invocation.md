# 独立调用

依赖：Windows中文AE26.0，能执行ExtendScript和aerender；FFmpeg/ffprobe；Python、Pillow（视频缩略图检查）、NumPy和OpenCV（漂移验证）。不依赖其他项目或教程素材。scripts内的宿主执行、渲染、检测、窗口工具复用本实验室已经实测的底层工具；json-encode.jsx复用首个技能的宿主兼容序列化函数。

以下命令从技能目录运行。调用方提供绝对路径的AE、aerender、新的运行目录、原创或获许可的视频与贴图。每一步读实际回执后才执行下一步，不把启动器退出0当作成功。

```powershell
python scripts/start.py INPUT.mp4 --out RUN --solve-method typical --detailed
& AE.exe -r RUN/start.jsx
python scripts/prepare_poll.py RUN
& AE.exe -r RUN/poll.jsx
```

等solve-state.json显示已求解。fov是有依据的水平视角（度），可用--fov提供；不知道时让软件估计，不得编造。已测走廊需要已知视角才能满足全平面误差门槛，不能把该值移植给别的镜头。

```powershell
python scripts/prepare_ui.py RUN
& AE.exe -r RUN/show-ui.jsx
./scripts/capture_native_window.ps1 -ProcessId PID -OutputPath VIEW.png
```

Agent查看当前截图，选择同一刚性平面上三个不共线且分布充分的点。坐标为该原生窗口内的物理像素，不能抄本实验的历史数值。

```powershell
./scripts/create_tracked_solid_gui.ps1 -ProjectPath RUN/tracking-attempt.aep -ProcessId PID -X X1 -Y Y1 -Points 'X1,Y1;X2,Y2;X3,Y3' -SelectOnly
```

截图确认三个黄色点及红色平面目标。再去掉-SelectOnly执行创建；ContextX/ContextY可指定已观察的右键命中点。窗口归属不符则停止该GUI动作。主机可能被其他窗口遮挡，可重新执行show-ui.jsx；不要操作遮挡应用。不要盲目点击或枚举点云隐藏API。

```powershell
& AE.exe -r RUN/finalize-plane.jsx
python scripts/prepare_composite.py --tracking-dir RUN --asset OVERLAY.png --name composite-001 --screen-width 180
python scripts/run_ae.py RUN/composite-001/build.jsx --ae AE.exe
python scripts/measure_tracking_drift.py INPUT.mp4 --trace RUN/composite-001/projection-trace.json --report RUN/composite-001/drift.json --radius 120
python scripts/render_ae.py RUN/composite-001 --aerender AERENDER.exe --reuse
```

半径必须根据实际画面选择，确保整个ROI在同一参考平面，并能覆盖贴图四角。失败或inconclusive仍可渲染诊断视频，但不能交付为已通过。强视差、遮挡或平面边界使矩形ROI不合适时，停止该检测结论，准备分段/掩膜参考或更合适的镜头；当前工具不支持掩膜输入。

输出project.aep保留摄影机、原片层、可替换贴图层、诊断点表达式与原生效果。图片文字仍是可替换的图片，不是AE文本图层。输出final.mp4、quality.json、projection-trace.json、placement.json、drift.json。渲染后保存原片、贴图、求解工程和输出工程，不能只拷贝AEP而丢失引用素材。

实际验收版本见tests/results.json。已知失败：单点平面导致错误方向、未知视角走廊漂移、局部ROI外推不可靠。按workflow.md诊断，不用真值摄影机替换求解结果。
