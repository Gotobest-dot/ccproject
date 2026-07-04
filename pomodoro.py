"""桌面番茄钟 - 主入口"""  # 模块文档字符串：说明本文件是番茄钟程序的主入口

from pomodoro_app import PomodoroApp  # 从 pomodoro_app 模块导入 PomodoroApp 窗口类


def main():  # 定义主函数 main，作为程序的启动入口
    app = PomodoroApp()  # 创建 PomodoroApp 窗口实例，初始化整个番茄钟 GUI
    app.mainloop()  # 进入 tkinter 主事件循环，保持窗口运行并响应用户操作


if __name__ == "__main__":  # 判断当前模块是否作为主程序直接运行（而非被 import 导入）
    main()  # 如果是直接运行，则调用 main() 函数启动番茄钟应用
