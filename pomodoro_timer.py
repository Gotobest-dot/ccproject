"""番茄钟核心计时逻辑"""

from pomodoro_config import WORK_TIME, BREAK_TIME, CYCLES_BEFORE_LONG_BREAK, LONG_BREAK_TIME


class PomodoroTimer:
    """番茄钟计时器，负责计时逻辑和状态管理，与 UI 完全分离。"""

    def __init__(self):
        self.work_time = WORK_TIME
        self.break_time = BREAK_TIME
        self.long_break_time = LONG_BREAK_TIME

        self.is_work_phase: bool = True
        self.is_running: bool = False
        self.remaining_seconds: int = self.work_time
        self.total_seconds: int = self.work_time
        self.pomodoro_count: int = 0

        # 回调函数（由 UI 设置）
        self.on_tick = None     # 每秒调用，参数: remaining_seconds, total_seconds
        self.on_finish = None   # 计时完成时调用
        self.on_phase_change = None  # 阶段切换时调用

    def start(self):
        """开始或恢复计时"""
        self.is_running = True

    def pause(self):
        """暂停计时"""
        self.is_running = False

    def reset(self):
        """重置当前阶段计时"""
        self.is_running = False
        self.total_seconds = self.work_time if self.is_work_phase else self.break_time
        self.remaining_seconds = self.total_seconds
        if self.on_tick:
            self.on_tick(self.remaining_seconds, self.total_seconds)

    def tick(self) -> bool:
        """每秒调用一次。返回 True 表示计时结束。"""
        if not self.is_running:
            return False

        self.remaining_seconds -= 1

        # 通知 UI 更新
        if self.on_tick:
            self.on_tick(self.remaining_seconds, self.total_seconds)

        # 计时结束
        if self.remaining_seconds <= 0:
            self.is_running = False
            self._switch_phase()
            if self.on_finish:
                self.on_finish()
            return True

        return False

    def _switch_phase(self):
        """切换工作/休息阶段"""
        if self.is_work_phase:
            # 工作结束，番茄数 +1
            self.pomodoro_count += 1
            self.is_work_phase = False
            # 判断是否进入长休息
            if self.pomodoro_count % CYCLES_BEFORE_LONG_BREAK == 0:
                self.total_seconds = self.long_break_time
            else:
                self.total_seconds = self.break_time
        else:
            self.is_work_phase = True
            self.total_seconds = self.work_time

        self.remaining_seconds = self.total_seconds
        if self.on_phase_change:
            self.on_phase_change()

    def get_time_str(self) -> str:
        """返回 MM:SS 格式的时间字符串"""
        mins = self.remaining_seconds // 60
        secs = self.remaining_seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def get_progress(self) -> float:
        """返回进度比例 0.0 ~ 1.0（剩余 / 总时长）"""
        if self.total_seconds == 0:
            return 0.0
        return self.remaining_seconds / self.total_seconds

    def set_work_time(self, seconds: int):
        """自定义工作时长"""
        self.work_time = seconds
        if self.is_work_phase:
            self.total_seconds = seconds
            self.remaining_seconds = seconds

    def set_break_time(self, seconds: int):
        """自定义休息时长"""
        self.break_time = seconds
        if not self.is_work_phase:
            self.total_seconds = seconds
            self.remaining_seconds = seconds
