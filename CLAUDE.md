# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

桌面番茄钟应用，使用 Python 标准库 + tkinter 构建，圆形手表风格 UI。无需安装额外依赖，Python 3.8+ 即可运行。

## 常用命令

```bash
# 运行番茄钟
python pomodoro.py

# 打包为 Windows exe
pip install pyinstaller
pyinstaller --onefile --windowed --name "番茄钟" pomodoro.py
```

## 架构

四文件分层架构，计时逻辑与 UI 完全分离：

| 文件 | 职责 |
|---|---|
| `pomodoro.py` | 入口，创建窗口并启动 mainloop |
| `pomodoro_config.py` | 所有可配置常量（时长、窗口尺寸、颜色、字体、通知参数） |
| `pomodoro_timer.py` | `PomodoroTimer` 类 — 纯计时状态机，通过回调通知 UI |
| `pomodoro_app.py` | `PomodoroApp(tk.Tk)` — GUI 窗口，Canvas 圆形表盘 + 按钮 |

**数据流：** `PomodoroTimer` 持有 `on_tick` / `on_finish` / `on_phase_change` 三个回调，由 `PomodoroApp` 在构造时注入。`_schedule_tick()` 通过 `self.after(1000, ...)` 每秒驱动一次 `timer.tick()`，不阻塞主线程。

**阶段切换：** 工作结束 → 番茄计数 +1 → 自动切到休息；休息结束 → 切回工作。每 4 个番茄触发一次长休息（15 分钟）。

**环形进度：** 使用 `tkinter.Canvas.create_arc` 绘制，起始角度 90°（12 点方向），extent 随剩余时间从 -360° 缩减至 0°。

**平台依赖：** `winsound.Beep` 仅 Windows 可用，通知音播放在线程中执行避免阻塞 UI。
