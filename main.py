import tkinter as tk
import musicplayer
import random
import datetime


class TimerAppGUI:
    def __init__(self, my_config, my_music_player):

        self.Label_motto_en = None
        self.Label_motto_cn = None
        self.rule_parts = None
        self.frame = None
        self.str_rules = None
        self.align_str = None
        self.Label_tips = None
        self.title_font_size = 30
        self.str_title = None
        self.Label_time = None
        self.countdown_Mid_Term = None
        self.Label_countdown = None
        self.Label_motto = None
        self.time_motto_font_size = 35
        self.Label_rules = None
        self.rules_font_size = 20
        self.config = my_config
        self.music_player = my_music_player
        self.root = tk.Tk()

        formatted_date = datetime.datetime.strptime(self.config.get_config("Deadlines_day"), "%Y/%m/%d")
        mid_term_time = datetime.datetime(formatted_date.year, formatted_date.month, formatted_date.day, 0, 0, 0)
        today_time = datetime.datetime.today()
        difference = mid_term_time - today_time
        self.countdown_Mid_Term = difference.days

        self.repeat_times = 15
        colors = self.config.get_config("color_settings")[random.randint(0, 2)]
        self.bg_color, self.schedule_color, self.motto_color, self.time_color = colors

        self.width = 1024
        self.height = 576
        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()

    def setup_gui(self):
        self.root.title(self.config.get_config("title_name"))
        self.root.overrideredirect(True)  # 去除标题栏
        # 设置快捷键来关闭窗口
        self.root.bind("<Escape>", self.close_window)
        # 设置快捷键来显示和隐藏窗口标题栏
        self.root.bind("<Control-h>", self.toggle_titlebar)
        self.align_str = '%dx%d+%d+%d' % (
            self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2)
        self.root.geometry(self.align_str)

        self.root.configure(bg=self.bg_color)

        self.title_style()

        self.Label_time = tk.Label(self.root,
                                   text=datetime.datetime.now().strftime(self.config.get_config('time_style')),
                                   bg=self.bg_color, fg=self.time_color, font=("monaco", self.time_motto_font_size))
        self.Label_time.pack()

        self.Label_countdown = tk.Label(self.root,
                                        text=f"距离{self.config.get_config("Deadlines_title")}"
                                             f"还有{str(self.countdown_Mid_Term)} 天",
                                        height=0, anchor="n",
                                        bg=self.bg_color, fg=self.schedule_color,
                                        font=("微软雅黑", self.title_font_size))
        self.Label_countdown.pack()

        self.motto_style()
        self.rule_style()

        # 设置座右铭更新的定时器
        self.Label_motto_cn.after(3000, self.update_motto)  # 每 5 分钟更新一次
        # 设置座右铭更新的定时器
        self.Label_time.after(1000, self.update_time)  # 每 1 秒更新一次

    def close_window(self, event):
        self.root.destroy()

    def toggle_titlebar(self, event):
        self.root.overrideredirect(not self.root.overrideredirect())

    def title_style(self):
        # 创建一个 Frame 用于存放 Label 和 Text
        self.frame = tk.Frame(self.root, bg=self.bg_color)
        self.frame.pack()
        label1 = tk.Label(self.frame, text=self.config.get_config("classes"),
                          width=10, height=2, anchor="w",
                          bg=self.bg_color, fg=self.motto_color,
                          font=("微软雅黑", self.title_font_size))
        label2 = tk.Label(self.frame, text=self.config.get_config("study_group"),
                          width=10, height=2, anchor="w",
                          bg=self.bg_color, fg=self.motto_color,
                          font=("微软雅黑", self.title_font_size))
        label3 = tk.Label(self.frame, text=f"值班家长：{self.config.get_config("student_parent")}",
                          width=20, height=2, anchor="w",
                          bg=self.bg_color, fg=self.motto_color,
                          font=("微软雅黑", self.title_font_size))
        # 将 Label 放入 Frame 中
        label1.grid(row=1, column=0, padx=5, pady=0, sticky="e")
        label2.grid(row=1, column=1, padx=5, pady=0, sticky="e")
        label3.grid(row=1, column=3, padx=5, pady=0, sticky="w")

    def rule_style(self):
        self.str_rules = self.config.get_config("str_rules")
        # 创建一个 Frame 用于存放 Label 和 Text
        self.frame = tk.Frame(self.root, bg=self.bg_color)
        self.frame.pack()

        for rule in self.str_rules:
            # 将每条规则按照换行符分割
            self.rule_parts = rule.split('|')
            # print(self.rule_parts)
            # 创建两个 Label，分别显示第一列和第二列的内容
            label1 = tk.Label(self.frame, text=self.rule_parts[0], width=10, anchor="center",
                              bg=self.bg_color, fg=self.schedule_color, font=("微软雅黑", self.rules_font_size))
            label2 = tk.Label(self.frame, text=self.rule_parts[1], width=10, anchor="center",
                              bg=self.bg_color, fg=self.schedule_color, font=("monaco", self.rules_font_size))
            label3 = tk.Label(self.frame, text=self.rule_parts[2], width=10, anchor="center",
                              bg=self.bg_color, fg=self.schedule_color, font=("微软雅黑", self.rules_font_size))

            # 将 Label 放入 Frame 中
            label1.grid(row=self.str_rules.index(rule), column=0, padx=5, pady=0, sticky="e")
            label2.grid(row=self.str_rules.index(rule), column=1, padx=5, pady=0, sticky="e")
            label3.grid(row=self.str_rules.index(rule), column=3, padx=5, pady=0, sticky="w")

    def motto_style(self):
        mottos = random.choice(self.config.get_config("str_motto"))
        # mottos = self.config.get_config("str_motto")[5]
        print(f"{datetime.datetime.now().minute}:{datetime.datetime.now().second}初始化motto{mottos}")
        self.Label_motto_cn = tk.Label(self.root, text=mottos[0],
                                       bg=self.bg_color, fg=self.motto_color,
                                       font=("行楷-简", self.time_motto_font_size))
        self.Label_motto_cn.pack()
        self.Label_motto_en = tk.Label(self.root, text=mottos[1],
                                       bg=self.bg_color, fg=self.motto_color,
                                       font=("comic sans ms", self.time_motto_font_size))
        self.Label_motto_en.pack()

    def update_motto(self):
        mottos = random.choice(self.config.get_config("str_motto"))
        print(f"{datetime.datetime.now().minute}:{datetime.datetime.now().second}更新2motto{mottos}")
        self.Label_motto_cn.config(text=mottos[0])
        self.Label_motto_en.config(text=mottos[1])
        self.Label_motto_cn.after(300000, self.update_motto)  # 每 5 分钟更新一次

    def run(self):
        self.setup_gui()
        # self.root.after(10, self.trick_it)
        self.root.mainloop()

    def update_time(self):
        # 获取当前时间
        current_datetime = datetime.datetime.now()
        # 获取当前格式化小时:分钟时间
        now_time = current_datetime.strftime("%H:%M")
        # 计算前一分钟的时间
        one_minute_ago_timestamp = current_datetime + datetime.timedelta(minutes=1)
        # 获取前一分钟的格式化小时:分钟时间
        one_minute_ago = one_minute_ago_timestamp.strftime("%H:%M")
        # print(f"当前时间{now_time}，一分钟前{one_minute_ago}")
        if now_time in self.config.get_config("after_class_time") and current_datetime.second == 0:
            self.Label_time.config(text="休息一下吧！")
            print(f"{now_time}下课")
            self.root.update()
            self.music_player.play_music(1)
        elif one_minute_ago in self.config.get_config("class_time") and current_datetime.second == 0:
            self.Label_time.config(text="准备上课啦！")
            print(f"{one_minute_ago}上课")
            self.root.update()
            self.music_player.play_music(0)
        else:
            self.Label_time.config(text=current_datetime.strftime(self.config.get_config('time_style')))

        self.root.update()
        self.Label_time.after(1000, self.update_time)


if __name__ == "__main__":
    import config as con

    config = con.Configuration("config.yaml")
    # import pprint
    # pprint.pprint(config.config)
    music_player = musicplayer.MusicPlayer(config)
    timer_app = TimerAppGUI(config, music_player)
    timer_app.run()
