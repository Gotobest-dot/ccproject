"""番茄钟配置常量"""

# ===== 时间配置（秒）=====
WORK_TIME = 25 * 60      # 专注时长
BREAK_TIME = 5 * 60      # 短休息时长
LONG_BREAK_TIME = 15 * 60  # 长休息时长（预留）
CYCLES_BEFORE_LONG_BREAK = 4  # 每几个番茄后进入长休息

# ===== 窗口配置 =====
WINDOW_WIDTH = 380
WINDOW_HEIGHT = 480
WINDOW_TITLE = "番茄钟 · Pomodoro"

# ===== 颜色方案（来自配色图）=====
COLOR_BG = "#FFFFFF"              # 背景 - 纯白
COLOR_FRAME_BG = "#F7FAFB"        # 卡片背景 - 极浅蓝灰
COLOR_TEXT_PRIMARY = "#601F0A"    # 主文字 - 深咖啡色
COLOR_TEXT_SECONDARY = "#8B6F64"  # 次要文字 - 浅咖啡色
COLOR_ACCENT = "#EE8360"          # 强调色 - 暖珊瑚橙（专注）
COLOR_ACCENT_DARK = "#D96E4D"     # 按钮按下色 - 深珊瑚
COLOR_BREAK = "#A8DEEA"           # 休息阶段 - 浅青蓝
COLOR_PROGRESS_BG = "#EDE8E4"     # 进度条背景

# ===== 按钮颜色 =====
COLOR_BTN_START = "#EE8360"
COLOR_BTN_START_HOVER = "#F59878"
COLOR_BTN_PAUSE = "#F9DD4F"
COLOR_BTN_PAUSE_HOVER = "#FBE67A"
COLOR_BTN_RESET = "#D0CCC8"
COLOR_BTN_RESET_HOVER = "#E0DCD8"
COLOR_BTN_TEXT = "#FFFFFF"
COLOR_BTN_PAUSE_TEXT = "#601F0A"  # 黄色按钮上用深色文字

# ===== 字体配置 =====
FONT_TIMER = ("Segoe UI", 56, "bold")
FONT_STATUS = ("Segoe UI", 16, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_COUNT = ("Segoe UI", 18)
FONT_BUTTON = ("Segoe UI", 13, "bold")

# ===== 通知配置 =====
NOTIFY_SOUND_FREQ = 800   # 提示音频率 (Hz)
NOTIFY_SOUND_DURATION = 600  # 提示音持续 (ms)
NOTIFY_REPEAT = 3         # 重复次数
NOTIFY_REPEAT_INTERVAL = 400  # 重复间隔 (ms)
