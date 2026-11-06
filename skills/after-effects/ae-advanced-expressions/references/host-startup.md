# 本机 AE 冷启动与子进程环境

本机AE26.0x67的原安装路径先报CEP加载错误；去掉CLI区域变量不够，单独补SystemDrive也失败。改用Windows `userenv.CreateEnvironmentBlock(NULL,FALSE)`读取系统环境，只补当前子进程缺失项，再移除LANG/LC_ALL/LC_CTYPE后，原路径正常启动。已保存原生空白探针、11例实际制作和正常关闭后的第二次冷启动探针。未隔离究竟哪一项变量起决定作用，不宣称某个变量是唯一病因。

本Skill的scripts/launch_adobe.py封装同一经过实际启动验证的方法；run_ae.py与render_ae.py已使用它。它不修改注册表、系统变量、Adobe首选项、安装文件或授权。调用者已有同名系统值保留，诊断只记录补齐的变量名，不输出其他环境内容。非Windows平台不调用该接口，也未经本库实测。

若启动仍失败，先看当前进程及所属对话框；有活进程时继续观察，不因等待超时重复启动。未经实际receipt、AEP重开和视频输出，不把启动器退出0当成功。保留脏工程和非本实验工作。发生不同错误时保留错误及缺失证据；本方法不是通用修复承诺。ASCII别名曾触发语言授权提示，后续未再用它，不修改授权规避错误。

官方接口依据：[Microsoft CreateEnvironmentBlock](https://learn.microsoft.com/en-us/windows/win32/api/userenv/nf-userenv-createenvironmentblock)。该接口NULL token返回系统变量，使用后销毁临时缓冲区。项目证据：evaluations/course2-p26-p27-scroll-001/host-environment-recovery.json、reports/host-native-cold-probe-scroll-001.json。单独分发Skill时，这些项目测试证据可另行提供；执行本身不依赖实验室路径。
