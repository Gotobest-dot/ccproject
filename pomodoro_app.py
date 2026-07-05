"""番茄钟 GUI 主窗口 — Swiss 瑞士风格"""

import math
import tkinter as tk
from tkinter import ttk, messagebox
import winsound
import threading

from pomodoro_config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    COLOR_BG, COLOR_FRAME_BG, COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY,
    COLOR_ACCENT, COLOR_ACCENT_DARK, COLOR_BREAK, COLOR_PROGRESS_BG,
    COLOR_BTN_START, COLOR_BTN_PAUSE, COLOR_BTN_RESET,
    COLOR_BTN_START_HOVER, COLOR_BTN_PAUSE_HOVER, COLOR_BTN_RESET_HOVER,
    COLOR_BTN_TEXT, COLOR_BTN_PAUSE_TEXT, COLOR_BTN_RESET_TEXT,
    COLOR_HAIRLINE, COLOR_TICK, COLOR_TICK_ACCENT,
    FONT_TIMER_MIN, FONT_TIMER_SEC, FONT_STATUS, FONT_LABEL, FONT_COUNT, FONT_BUTTON,
    NOTIFY_SOUND_FREQ, NOTIFY_SOUND_DURATION,
    NOTIFY_REPEAT, NOTIFY_REPEAT_INTERVAL,
)
from pomodoro_timer import PomodoroTimer


class PomodoroApp(tk.Tk):
    """番茄钟主窗口"""

    def __init__(self):
        super().__init__()

        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.configure(bg=COLOR_BG)

        # 居中显示
        self._center_window()

        # 计时器
        self.timer = PomodoroTimer()
        self.timer.on_tick = self._on_tick
        self.timer.on_finish = self._on_finish
        self.timer.on_phase_change = self._on_phase_change

        # 构建界面
        self._build_ui()

        # 启动定时刷新
        self._schedule_tick()

        # 窗口关闭处理
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ==================== UI 构建 ====================

    def _build_ui(self):
        """构建所有 UI 组件 — Swiss 精密计时仪器风格"""

        # ===== 1. 顶部状态标签 =====
        self.status_label = tk.Label(
            self, text="FOCUS", font=FONT_STATUS,
            bg=COLOR_BG, fg=COLOR_ACCENT
        )
        self.status_label.pack(pady=(25, 12))

        # 分隔线
        sep1 = tk.Frame(self, height=1, bg=COLOR_HAIRLINE)
        sep1.pack(fill="x", padx=50)

        # ===== 2. 圆形计时器表盘 =====
        self.canvas_size = 280
        self.circle_r = 118
        self.ring_width = 6               # Swiss: 细进度环

        self.canvas = tk.Canvas(self, width=self.canvas_size,
                                height=self.canvas_size,
                                bg=COLOR_BG, highlightthickness=0)
        self.canvas.pack(pady=(18, 10))

        cx = cy = self.canvas_size / 2
        r = self.circle_r
        rw = self.ring_width

        # 表盘背景（微灰圆形 + 1px 细线边框）
        self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill=COLOR_FRAME_BG, outline=COLOR_HAIRLINE, width=1,
            tags="face"
        )

        # 刻度线 — 12 根，每 5 分钟一根（30° 间隔）
        for i in range(12):
            angle_deg = i * 30
            angle_rad = math.radians(angle_deg - 90)  # 从 12 点方向开始

            inner_r = r - 2                          # 刻度线起点（表盘内侧）
            outer_r = r - 18 if i == 0 else r - 14   # 12 点位稍长

            x1 = cx + inner_r * math.cos(angle_rad)
            y1 = cy + inner_r * math.sin(angle_rad)
            x2 = cx + outer_r * math.cos(angle_rad)
            y2 = cy + outer_r * math.sin(angle_rad)

            is_accent = (i == 0)
            tick_color = COLOR_TICK_ACCENT if is_accent else COLOR_TICK
            tick_width = 2 if is_accent else 1

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=tick_color, width=tick_width, tags="tick"
            )

        # 进度环底色（轨道）
        self.track_arc = self.canvas.create_arc(
            cx - r + rw/2, cy - r + rw/2,
            cx + r - rw/2, cy + r - rw/2,
            start=90, extent=-359.9,
            style="arc", width=rw,
            outline=COLOR_PROGRESS_BG, tags="track"
        )

        # 进度环（初始满圈，克莱因蓝）
        self.progress_arc = self.canvas.create_arc(
            cx - r + rw/2, cy - r + rw/2,
            cx + r - rw/2, cy + r - rw/2,
            start=90, extent=-359.9,
            style="arc", width=rw,
            outline=COLOR_ACCENT, tags="progress"
        )
        self._current_progress_color = COLOR_ACCENT

        # 中心时间显示 — 分钟（大字、粗体）
        self.min_text = self.canvas.create_text(
            cx, cy - 12, text="25",
            font=FONT_TIMER_MIN, fill=COLOR_TEXT_PRIMARY, anchor="center",
            tags="time_min"
        )

        # 中心时间显示 — 秒（小字、常规字重）
        self.sec_text = self.canvas.create_text(
            cx, cy + 30, text="00",
            font=FONT_TIMER_SEC, fill=COLOR_TEXT_SECONDARY, anchor="center",
            tags="time_sec"
        )

        # ===== 3. 番茄计数区域 =====
        sep2 = tk.Frame(self, height=1, bg=COLOR_HAIRLINE)
        sep2.pack(fill="x", padx=50)

        count_frame = tk.Frame(self, bg=COLOR_BG)
        count_frame.pack(pady=(10, 0))

        self.count_label = tk.Label(
            count_frame, text="TOMATOES · 0", font=FONT_COUNT,
            bg=COLOR_BG, fg=COLOR_TEXT_PRIMARY
        )
        self.count_label.pack()

        self.today_label = tk.Label(
            count_frame, text="TODAY · 0", font=FONT_LABEL,
            bg=COLOR_BG, fg=COLOR_TEXT_SECONDARY
        )
        self.today_label.pack(pady=(2, 0))

        # ===== 4. 按钮区域 =====
        btn_frame = tk.Frame(self, bg=COLOR_BG)
        btn_frame.pack(pady=(18, 0))

        self.start_btn = tk.Button(
            btn_frame, text="START", font=FONT_BUTTON,
            bg=COLOR_BTN_START, fg=COLOR_BTN_TEXT,
            activebackground=COLOR_BTN_START_HOVER,
            activeforeground=COLOR_BTN_TEXT,
            relief="flat", bd=0, padx=36, pady=10,
            cursor="hand2",
            command=self._toggle_start_pause
        )
        self.start_btn.pack(side="left", padx=(0, 12))

        self.reset_btn = tk.Button(
            btn_frame, text="RESET", font=FONT_BUTTON,
            bg=COLOR_BTN_RESET, fg=COLOR_BTN_RESET_TEXT,
            activebackground=COLOR_BTN_RESET_HOVER,
            activeforeground=COLOR_BTN_RESET_TEXT,
            relief="flat", bd=0, padx=36, pady=10,
            cursor="hand2",
            command=self._reset
        )
        self.reset_btn.pack(side="left")

        # 绑定悬停效果
        self._bind_hover(self.start_btn, COLOR_BTN_START, COLOR_BTN_START_HOVER)
        self._bind_hover(self.reset_btn, COLOR_BTN_RESET, COLOR_BTN_RESET_HOVER)

    def _bind_hover(self, widget, normal_color, hover_color):
        """绑定鼠标悬停颜色变化"""
        def on_enter(e):
            if widget["state"] != "disabled":
                widget["bg"] = hover_color

        def on_leave(e):
            widget["bg"] = normal_color

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    # ==================== 窗口定位 ====================

    def _center_window(self):
        """将窗口居中显示"""
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - WINDOW_WIDTH) // 2
        y = (screen_h - WINDOW_HEIGHT) // 2
        self.geometry(f"+{x}+{y}")

    # ==================== 计时循环 ====================

    def _schedule_tick(self):
        """安排下一次 tick（每 1 秒）"""
        self.timer.tick()
        self.after(1000, self._schedule_tick)

    # ==================== 回调处理 ====================

    def _on_tick(self, remaining, total):
        """计时器每秒回调 — 更新分层时间显示和进度环"""
        mins = remaining // 60
        secs = remaining % 60

        # 更新分钟和秒分别显示
        self.canvas.itemconfig(self.min_text, text=f"{mins:02d}")
        self.canvas.itemconfig(self.sec_text, text=f"{secs:02d}")

        # 更新进度环（逆时针缩减）
        progress_pct = self.timer.get_progress()
        extent = -(progress_pct * 360)
        if abs(extent) < 0.01:
            extent = 0.01
        self.canvas.itemconfig(self.progress_arc, extent=extent)

    def _on_finish(self):
        """计时结束回调 — 弹窗 + 声音"""
        self._update_button_state()
        self._update_count_display()

        # 播放提示音（非阻塞线程）
        threading.Thread(target=self._play_notification, daemon=True).start()

        # 弹窗通知
        if not self.timer.is_work_phase:
            msg = "Focus session complete — take a break."
        else:
            msg = "Break over — time to focus."
        self.after(100, lambda: messagebox.showinfo("Pomodoro", msg))

    def _on_phase_change(self):
        """阶段切换回调 — 更新状态标签和环形颜色"""
        if self.timer.is_work_phase:
            self.status_label.config(text="FOCUS", fg=COLOR_ACCENT)
            self._update_ring_color(COLOR_ACCENT)
            self.start_btn.config(
                text="START", bg=COLOR_BTN_START,
                fg=COLOR_BTN_TEXT,
                activebackground=COLOR_BTN_START_HOVER,
                activeforeground=COLOR_BTN_TEXT
            )
        else:
            self.status_label.config(text="BREAK", fg=COLOR_BREAK)
            self._update_ring_color(COLOR_BREAK)
            self.start_btn.config(
                text="START", bg=COLOR_BTN_PAUSE,
                fg=COLOR_BTN_PAUSE_TEXT,
                activebackground=COLOR_BTN_PAUSE_HOVER,
                activeforeground=COLOR_BTN_PAUSE_TEXT
            )

        # 刷新时间显示为满圈
        mins = self.timer.remaining_seconds // 60
        secs = self.timer.remaining_seconds % 60
        self.canvas.itemconfig(self.min_text, text=f"{mins:02d}")
        self.canvas.itemconfig(self.sec_text, text=f"{secs:02d}")
        self.canvas.itemconfig(self.progress_arc, extent=-359.9)

    def _update_button_state(self):
        """更新按钮文字和状态"""
        if self.timer.is_running:
            self.start_btn.config(text="PAUSE",
                                  bg=COLOR_BTN_PAUSE,
                                  fg=COLOR_BTN_PAUSE_TEXT,
                                  activeforeground=COLOR_BTN_PAUSE_TEXT)
        else:
            if self.timer.is_work_phase:
                self.start_btn.config(text="START",
                                      bg=COLOR_BTN_START,
                                      fg=COLOR_BTN_TEXT,
                                      activeforeground=COLOR_BTN_TEXT)
            else:
                self.start_btn.config(text="START",
                                      bg=COLOR_BTN_PAUSE,
                                      fg=COLOR_BTN_PAUSE_TEXT,
                                      activeforeground=COLOR_BTN_PAUSE_TEXT)

    def _update_count_display(self):
        """更新番茄计数显示"""
        count = self.timer.pomodoro_count
        self.count_label.config(text=f"TOMATOES · {count}")
        self.today_label.config(text=f"TODAY · {count}")

    def _update_ring_color(self, color):
        """动态更新圆形进度环颜色"""
        self._current_progress_color = color
        self.canvas.itemconfig(self.progress_arc, outline=color)

    # ==================== 通知 ====================

    def _play_notification(self):
        """播放系统提示音（多次蜂鸣）"""
        for _ in range(NOTIFY_REPEAT):
            winsound.Beep(NOTIFY_SOUND_FREQ, NOTIFY_SOUND_DURATION)
            import time
            time.sleep(NOTIFY_REPEAT_INTERVAL / 1000)

    # ==================== 按钮事件 ====================

    def _toggle_start_pause(self):
        """开始/暂停按钮"""
        if self.timer.is_running:
            self.timer.pause()
        else:
            self.timer.start()
        self._update_button_state()

    def _reset(self):
        """重置按钮"""
        if self.timer.is_running or \
           self.timer.remaining_seconds != self.timer.total_seconds:
            if messagebox.askyesno("Confirm", "Reset current timer?"):
                self.timer.reset()
                self._update_button_state()
                mins = self.timer.remaining_seconds // 60
                secs = self.timer.remaining_seconds % 60
                self.canvas.itemconfig(self.min_text, text=f"{mins:02d}")
                self.canvas.itemconfig(self.sec_text, text=f"{secs:02d}")
                self.canvas.itemconfig(self.progress_arc, extent=-359.9)

    # ==================== 关闭处理 ====================

    def _on_close(self):
        """窗口关闭处理"""
        self.timer.pause()
        self.destroy()
