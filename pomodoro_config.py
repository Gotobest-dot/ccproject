"""番茄钟配置常量 — Swiss 瑞士风格"""

# ===== 时间配置（秒）=====
WORK_TIME = 25 * 60      # 专注时长
BREAK_TIME = 5 * 60      # 短休息时长
LONG_BREAK_TIME = 15 * 60  # 长休息时长（预留）
CYCLES_BEFORE_LONG_BREAK = 4  # 每几个番茄后进入长休息

# ===== 窗口配置 =====
WINDOW_WIDTH = 380
WINDOW_HEIGHT = 480
WINDOW_TITLE = "Pomodoro"

# ===== Swiss 配色方案 =====
COLOR_BG = "#FFFFFF"              # 纯白背景
COLOR_FRAME_BG = "#F5F5F5"        # 表盘底色 - 微灰
COLOR_TEXT_PRIMARY = "#1A1A1A"    # 主文字 - 近黑
COLOR_TEXT_SECONDARY = "#757575"  # 次要文字 - 中灰
COLOR_ACCENT = "#002FA7"          # 专注强调色 - 克莱因蓝
COLOR_ACCENT_DARK = "#001C80"     # 按钮按下态
COLOR_BREAK = "#5B7F95"           # 休息阶段 - 石板蓝灰
COLOR_PROGRESS_BG = "#E0E0E0"     # 进度环底色

# ===== 按钮颜色 =====
COLOR_BTN_START = "#002FA7"
COLOR_BTN_START_HOVER = "#003DD4"
COLOR_BTN_PAUSE = "#5B7F95"
COLOR_BTN_PAUSE_HOVER = "#7195A8"
COLOR_BTN_RESET = "#E8E8E8"
COLOR_BTN_RESET_HOVER = "#D5D5D5"
COLOR_BTN_TEXT = "#FFFFFF"
COLOR_BTN_PAUSE_TEXT = "#FFFFFF"
COLOR_BTN_RESET_TEXT = "#1A1A1A"

# ===== Swiss 专用 =====
COLOR_HAIRLINE = "#D0D0D0"        # 1px 分割线 / 表盘边框
COLOR_TICK = "#B0B0B0"            # 刻度线颜色
COLOR_TICK_ACCENT = "#002FA7"     # 12 点刻度强调色

# ===== 字体配置 =====
FONT_TIMER_MIN = ("Segoe UI", 58, "bold")   # 分钟部分
FONT_TIMER_SEC = ("Segoe UI", 28)           # 秒部分（regular weight）
FONT_STATUS = ("Segoe UI", 14, "bold")      # 状态标签
FONT_LABEL = ("Segoe UI", 10)               # 辅助文字
FONT_COUNT = ("Segoe UI", 13, "bold")       # 计数
FONT_BUTTON = ("Segoe UI", 12, "bold")      # 按钮

# ===== 通知配置 =====
NOTIFY_SOUND_FREQ = 800   # 提示音频率 (Hz)
NOTIFY_SOUND_DURATION = 600  # 提示音持续 (ms)
NOTIFY_REPEAT = 3         # 重复次数
NOTIFY_REPEAT_INTERVAL = 400  # 重复间隔 (ms)
