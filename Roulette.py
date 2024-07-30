############################################
# Python(H) Final Project
##         Monte Carlo Simulation
# Time Spent: 23h in total
############################################ 

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import matplotlib.pyplot as plt
import numpy as np

class FairRoulette:
    '''
    公平轮盘类，初始化转盘，随机产生结果
    '''
    def __init__(self):   ##初始化轮盘
        self.pockets = list(range(1, 37))  
        self.ball = None
        self.pocketOdds = len(self.pockets) - 1  ##设置赔率

    def spin(self):  ##随机抽取，模拟转盘
        self.ball = random.choice(self.pockets)

    def get_pocket(self):
        return len(self.pockets)
    
    def betPocket(self, pocket, amt):  ##计算结果
        if str(pocket) == str(self.ball):
            return amt * self.pocketOdds
        else:
            return -amt

    def __str__(self):  ##输出
        return 'Fair Roulette'

class EuropeanRoulette(FairRoulette):
    '''
    欧式轮盘继承公平转盘 增加0
    '''
    def __init__(self):
        super().__init__()  ##继承父类-公平转盘的函数
        self.pockets.append(0)  ##增加0

    def __str__(self):
        return 'European Roulette'

class AmericanRoulette(FairRoulette):
    '''
    美式轮盘继承公平转盘 继承0和00
    '''
    def __init__(self):
        super().__init__()
        self.pockets.extend([0, '00'])

    def __str__(self):
        return 'American Roulette'

class RouletteGame:
    """
    轮盘游戏类
    """
    def __init__(self, root):
        """
        构造函数
        """
        self.root = root    # 初始化窗口对象，root为根窗口
        self.root.title("Roulette Game")  ##设置窗口标题
        self.total_funds = 0    # 初始赌资为0元
        self.roulette_type = tk.StringVar(value="公平轮盘") # 在tk中的string变量
        self.bets = []      # 储存下注信息的空列表
        self.create_window()    # 创建窗口
        self.load_image()

    def load_image(self):
        """
        加载并显示轮盘图像
        """
        image_path = "roulette.png"  ##将同一文件下的图片赋值给image_path
        img = Image.open(image_path)
        width, height = img.size
        new_width, new_height = width*0.6, height*0.6
        img = img.resize((int(new_width), int(new_height)), Image.LANCZOS)  # 压缩图片
        self.photo = ImageTk.PhotoImage(img)  ##显示图片
        
        self.image_label = tk.Label(self.scrollable_frame, image=self.photo)
        self.image_label.grid(row=5, column=3, padx=0, pady=0, columnspan=6)  ##创建图形界面所要用到的框架


    def create_window(self):
        """
        创建一个带有垂直滚动功能的窗口，可选择轮盘类型，输入投注金额，开始游戏和添加投注的按钮
        垂直滚动功能由大语言模型添加
        """
        self.canvas = tk.Canvas(self.root)  # 创建一个画布
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)  # 创建垂直滚动条
        self.scrollable_frame = tk.Frame(self.canvas)

        # 更新Canvas的滚动区域(运用大语言模型)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # 在画布中创建窗口
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)  ##设置滚动条

        # 放置画布和滚动条，并设置填充模式
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 添加提示标签，和一些选择按钮
        tk.Label(self.scrollable_frame, text="选择轮盘类型：").grid(row=0, column=0)
        for i, roulette_type in enumerate(["公平轮盘", "欧式轮盘", "美式轮盘"], start=1):
            tk.Radiobutton(self.scrollable_frame, text=roulette_type, variable=self.roulette_type, value=roulette_type).grid(row=i, column=0)

        tk.Label(self.scrollable_frame, text="总赌资：（请点击确认）").grid(row=0, column=1)
        self.total_funds_entry = tk.Entry(self.scrollable_frame)
        self.total_funds_entry.grid(row=0, column=2)

        tk.Button(self.scrollable_frame, text="确认", command=self.set_total_funds).grid(row=0, column=3)

        self.add_bet_section()  ##添加进入游戏后显示的“数字”“奇偶”“列”等选项

        tk.Button(self.scrollable_frame, text="开始游戏", command=self.play_game).grid(row=1, column=1, columnspan=2)
        tk.Button(self.scrollable_frame, text="添加下注", command=self.add_bet_section).grid(row=2, column=1, columnspan=2)

        self.result_label = tk.Label(self.scrollable_frame, text="当前总资金：0 元")
        self.result_label.grid(row=4, column=0, columnspan=3)  ##输出结果显示框的位置设置

        # 设置具体信息框的格式
        self.details_text = tk.Text(self.scrollable_frame, height=10, width=50)
        self.details_text.grid(row=5, column=0, columnspan=3)

    def set_total_funds(self):
        """
        获取总资金并输出 包含异常处理
        """
        try:  
            self.total_funds = int(self.total_funds_entry.get())
            self.result_label.config(text=f"当前总资金：{self.total_funds} 元")
        except:
            messagebox.showerror("错误", "请输入有效的总赌资金额")  # 第一个参数为窗口名字，第二个为输出内容

    def add_bet_section(self, start_row=None):
        """
        添加下注的部分 参数为开始的行数 默认为None
        """
        # 下注内容总共6行
        if start_row is None:
            start_row = len(self.bets) * 6 + 6  ##添加下注共有六行内容，每添加一次就多六行

        # 创建下注类型，下注金额
        bet_type = tk.StringVar(value="数字")
        bet_amount = tk.Entry(self.scrollable_frame)
        self.add_placeholder(bet_amount, "请输入下注金额(整数)")  # 文字提示
        # Frame组件用于存放下注信息
        bet_details_frame = tk.Frame(self.scrollable_frame)

        # bets列表，元素为元组，元组中有下注类型，下注金额和下注信息
        self.bets.append((bet_type, bet_amount, bet_details_frame))

        # 创建下注类型选择按钮，按下按钮调用bet_options方法
        tk.Radiobutton(self.scrollable_frame, text="数字", variable=bet_type, value="数字", command=lambda: self.bet_options(bet_details_frame, bet_type.get())).grid(row=start_row, column=0)
        tk.Radiobutton(self.scrollable_frame, text="奇偶", variable=bet_type, value="奇偶", command=lambda: self.bet_options(bet_details_frame, bet_type.get())).grid(row=start_row+1, column=0)
        tk.Radiobutton(self.scrollable_frame, text="红黑", variable=bet_type, value="红黑", command=lambda: self.bet_options(bet_details_frame, bet_type.get())).grid(row=start_row+2, column=0)
        tk.Radiobutton(self.scrollable_frame, text="高低", variable=bet_type, value="高低", command=lambda: self.bet_options(bet_details_frame, bet_type.get())).grid(row=start_row+3, column=0)
        tk.Radiobutton(self.scrollable_frame, text="区域", variable=bet_type, value="区域", command=lambda: self.bet_options(bet_details_frame, bet_type.get())).grid(row=start_row+4, column=0)
        tk.Radiobutton(self.scrollable_frame, text="列", variable=bet_type, value="列", command=lambda: self.bet_options(bet_details_frame, bet_type.get())).grid(row=start_row+5, column=0)

        # 绘制下注金额和下注具体信息
        bet_amount.grid(row=start_row, column=1)
        bet_details_frame.grid(row=start_row, column=2, rowspan=6)
        # 默认数字方法
        self.bet_options(bet_details_frame, bet_type.get())

    def add_placeholder(self, entry, placeholder):
        """
        显示提示文本 由大语言模型完成
        """
        entry.insert(0, placeholder)
        entry.config(fg="grey")
        entry.bind("<FocusIn>", lambda event: self.on_entry_click(event, entry, placeholder))
        entry.bind("<FocusOut>", lambda event: self.on_focus_out(event, entry, placeholder))

    def on_entry_click(self, event, entry, placeholder):
        """
        点击输入框调用 由大语言模型完成
        """
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def on_focus_out(self, event, entry, placeholder):
        """
        点击其他位置调用 由大语言模型完成
        """
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    def bet_options(self, frame, bet_type):
        """
        根据下注类型创建复选框
        """
        # 销毁所有子组件
        for widget in frame.winfo_children():
            widget.destroy()

        if bet_type == "数字":
            # 创建数字选项
            roulette = self.get_roulette()  # 获取轮盘类型
            options = roulette.pockets  # 选项为轮盘中的数字
            # 创建复选框并放入框架
            for option in options:
                chk = tk.Checkbutton(frame, text=str(option))   # str()保证有00选项
                chk.var = tk.IntVar()
                chk.config(variable=chk.var)
                chk.grid()
        else:
            options = {
                "奇偶": ["奇数", "偶数"],
                "红黑": ["红", "黑"],
                "高低": ["低", "高"],
                "区域": ["1-12", "13-24", "25-36"],
                "列": ["第一列", "第二列", "第三列"]
            }
            # 其他下注类型，从字典获取列表作为复选框
            for option in options.get(bet_type, []):
                chk = tk.Checkbutton(frame, text=option)
                chk.var = tk.IntVar()
                chk.config(variable=chk.var)
                chk.grid()

    def check_win(self, result, bet_type, bet_detail):
        """
        根据bet_type确定投注类型 result为轮盘结果 bet_detail为下注情况
        赢了返回True
        """
        if bet_type == "数字":
            return str(result) == str(bet_detail)
        
        elif bet_type == "奇偶":
            if bet_detail == "偶数":
                if result % 2 == 0:
                    return True
                else:
                    return False
            else:
                if result % 2 != 0:
                    return True
                else:
                    return False

        elif bet_type == "红黑":
            black_numbers = {1, 3, 5, 7, 9, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
            red_numbers = {2, 4, 6, 8, 10, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
            if result in red_numbers:
                if bet_detail == "红":
                    return True
                else:
                    return False
            elif result in black_numbers:
                return bet_detail == "黑"
            else:
                return False
        
        elif bet_type == "高低":
            # 如果结果为0则直接返回false
            if result == 0 or result == '00':
                return False
            if bet_detail == "低":
                if result >= 1 and result <= 18:
                    return True
                else:
                    return False
            else:
                if result >= 19 and result <= 36:
                    return True
                else:
                    return False
            
        elif bet_type == "区域":
            if bet_detail == "1-12":
                return 1 <= result <= 12
            elif bet_detail == "13-24":
                return 13 <= result <= 24
            elif bet_detail == "25-36":
                return 25 <= result <= 36
            else:
                return False
        
        elif bet_type == "列":
            # 第一列中的数被3除余数为1
            if result % 3 == 1:
                return bet_detail == "第一列"
            elif result % 3 == 2:
                return bet_detail == "第二列"
            elif result % 3 == 0:
                return bet_detail == "第三列"
            else:
                return False
        return False

    def calculate_winnings(self, bet_type, bet_amount, num_wins):
        roulette_type = self.get_roulette()
        num_odds = roulette_type.get_pocket() - 1
        odds = {
            "数字": num_odds,
            "奇偶": 1,
            "红黑": 1,
            "高低": 1,
            "区域": 2,
            "列": 2
        }
        return bet_amount * (odds[bet_type]+1) * num_wins


    def play_game(self):
        """
        主要函数 游戏进行
        """
        # 检查赌资是否设置
        if not self.total_funds:
            messagebox.showerror("错误", "请先设置总赌资")
            return

        # 下注金额和下注信息
        total_bet = 0
        bets_details = []

        # 遍历所有下注
        for bet_type, bet_amount, bet_details_frame in self.bets:
            try:
                bet_amount_value = int(bet_amount.get())
                total_bet += bet_amount_value
                # 将下注信息都添加到下注列表
                selected_details = [chk.cget("text") for chk in bet_details_frame.winfo_children() if chk.var.get() == 1]
                if not selected_details:
                    continue
                bets_details.append((bet_type.get(), selected_details, bet_amount_value))
            except ValueError:
                messagebox.showerror("错误", "请输入有效的下注金额")
                return

        # 下注总金额超过总资金报错
        if total_bet > self.total_funds:
            messagebox.showerror("错误", "总下注金额不能超过当前总资金")
            return

        # 使用roulette相关对象的方法转动轮盘，存储结果
        roulette = self.get_roulette()
        roulette.spin()
        result = roulette.ball

        # 输出结果
        self.details_text.insert(tk.END, f"本轮结果：{result}\n")

        """
        使用下列信息计算剩余资金
        bets_details是一个列表 每个元素是一个元组 有三个元素：
        1. bet_type下注类型 为字符串类型
        2. bet_contents具体的下注内容 为一个列表
        3. bet_amount为下注金额
        例如：
        bets_details = [
        ("数字", ["5", "10", "15"], 100),      # 在数字5 10 15总共投注了100
        ("奇偶", ["奇数"], 50),               # 在奇数上投注了 50
        ("红黑", ["红"], 75),                 # 在红色上投注了 75
        ]
        
        需使用self.calculate_winnings()和self.check_win()函数
        结果结构：
        if win:
            self.details_text.insert(tk.END, f"你赢了 {winnings} 元在 {bet_type} 下注: {', '.join(map(str, bet_details))}\n")
        else:
            self.details_text.insert(tk.END, f"你输了 {bet_amount} 元在 {bet_type} 下注: {', '.join(map(str, bet_details))}\n")

        self.total_funds += total_winnings - total_bet
        self.result_label.config(text=f"当前总资金：{self.total_funds} 元")
        """
        total_winnings = 0  # 赢得总金额初始化

        # 遍历所有下注列表
        for bet_type, bet_contents, bet_amount in bets_details:
            win = False
            winnings = 0    # 单个获胜金额初始化
            for bet_detail in bet_contents:     # 遍历每一个下注具体信息
                if self.check_win(result, bet_type, bet_detail):        # 获胜
                    individual_bet_amount = bet_amount / len(bet_contents)      # 处理投注情况
                    winnings += self.calculate_winnings(bet_type, individual_bet_amount, 1)     # 调用calculate_winnings函数计算赔率
                    win = True
            
            if win:     # 如果获胜，输出获胜信息，输出为没有减去本金的情况，但在计算剩余资金是考虑了本金，即赢得金额+获胜部分本金
                total_winnings += winnings - bet_amount
                self.details_text.insert(tk.END, f"你赢了 {winnings} 元在 {bet_type} 下注: {', '.join(map(str, bet_contents))}\n")
            else:       # 未获胜显示输了的金额即为下注金额
                total_winnings -= bet_amount
                self.details_text.insert(tk.END, f"你输了 {bet_amount} 元在 {bet_type} 下注: {', '.join(map(str, bet_contents))}\n")

        # 总计
        self.total_funds += total_winnings
        self.result_label.config(text=f"当前总资金：{self.total_funds} 元") # 更新总资金


    def get_roulette(self):
        # 读取轮盘类型函数
        if self.roulette_type.get() == "公平轮盘":
            return FairRoulette()
        elif self.roulette_type.get() == "欧式轮盘":
            return EuropeanRoulette()
        elif self.roulette_type.get() == "美式轮盘":
            return AmericanRoulette()

def monte_carlo_simulation(roulette_type, bet_type, total_spins):
    '''
    蒙特卡洛模拟函数：
    输入 轮盘类型 下注类型 总次数
    输出余额的折线图 同时在命令行输出方差
    折线图取点总共取20个点
    '''
    step = int(total_spins / 20)    # step必须是int
    bet_amount = 1                  # 假设单次投注1元
    total_funds = 0     # 总资金
    total = []          # 取样的总资金
    sampled_spins = list(range(1, total_spins + 1, step))   # 取样点的次数列表

    # 三种轮盘类型
    if roulette_type == 'Fair':
        roulette = FairRoulette()
    elif roulette_type == 'European':
        roulette = EuropeanRoulette()
    else:
        roulette = AmericanRoulette()

    for spin in range(1, total_spins + 1):
        # 从第一次开始
        roulette.spin()
        if bet_type == 'Number':        # 数字类型
            bet_choice = random.choice(roulette.pockets)    # 随机生成一个下注数字
            winnings = roulette.betPocket(bet_choice, bet_amount)   # 计算单词资金
        elif bet_type == 'Odd/Even':    # 奇偶类型
            bet_choice = random.choice(['Odd', 'Even'])     # 随机选一种类型
            if roulette.ball == '00':       # 00的情况单独处理
                winnings =  -bet_amount
            else:
                if (roulette.ball % 2 == 0 and bet_choice == 'Even') or (roulette.ball % 2 != 0 and bet_choice == 'Odd'):
                    winnings = bet_amount * 1  
                else:
                    winnings = -bet_amount
        elif bet_type == 'Column':      # 列的情况
            if roulette.ball == '00':
                winnings =  -bet_amount
            else:
                bet_choice = random.choice(['First', 'Second', 'Third'])
                if bet_choice == 'First' and roulette.ball % 3 == 1:
                    winnings = bet_amount * 2  
                elif bet_choice == 'Second' and roulette.ball % 3 == 2:
                    winnings = bet_amount * 2
                elif bet_choice == 'Third' and roulette.ball % 3 == 0:
                    winnings = bet_amount * 2
                else:
                    winnings = -bet_amount

        total_funds += winnings     # 累计单次资金计算总资金
        if spin % step == 0:        # 取样点
            total.append(total_funds)

    plt.plot(sampled_spins, total)  # 绘制取样点的图像
    variance = np.var(total)        # 计算方差并输出
    print(f"Variance: {variance}")

    # 图标内容相关
    plt.title(f"{roulette} Simulation total funds: {total_funds}", fontsize=14, color="g")
    plt.xlabel("Play times:" + str(total_spins), fontsize=15, color="red")
    plt.ylabel("Total funds", fontsize=16, color="b")
    plt.scatter(sampled_spins, total)
    plt.plot([0, max(sampled_spins)], [0, 0], color="r")
    plt.show()





if __name__ == "__main__":
    '''
    主函数：
    选择模式 游戏模式和蒙特卡洛模拟模式
    窗口独立 选择完毕关掉游戏窗口或蒙特卡洛模拟窗口还可以再次选择
    '''
    def start_game():
        # 游戏函数，创建窗口，创建RouletteGame类
        game_window = tk.Toplevel(root)
        app = RouletteGame(game_window)
        game_window.protocol("WM_DELETE_WINDOW", lambda: return_to_main(game_window))

    def start_monte_carlo_simulation():
        # 模拟函数
        def run_simulation():
            roulette_type = roulette_var.get()  # 获取轮盘类型
            bet_type = bet_var.get()    # 获取下注类型
            try:    # 获取模拟次数 并处理异常
                total_spins = int(total_spins_entry.get())
                if total_spins <= 0 or total_spins % 20 != 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("错误", "请输入有效的模拟次数")
                return
            # 调用模拟函数
            monte_carlo_simulation(roulette_type, bet_type, total_spins)

        # 创建相应窗口
        sim_window = tk.Toplevel(root)
        sim_window.title("Monte Carlo Simulation")
        sim_window.protocol("WM_DELETE_WINDOW", lambda: return_to_main(sim_window))

        # 默认类型
        roulette_var = tk.StringVar(value="Fair")
        bet_var = tk.StringVar(value="Number")

        # 提供选择菜单
        tk.Label(sim_window, text="选择轮盘类型:").pack()
        tk.Radiobutton(sim_window, text="公平轮盘", variable=roulette_var, value="Fair").pack(anchor=tk.W)
        tk.Radiobutton(sim_window, text="欧式轮盘", variable=roulette_var, value="European").pack(anchor=tk.W)
        tk.Radiobutton(sim_window, text="美式轮盘", variable=roulette_var, value="American").pack(anchor=tk.W)

        tk.Label(sim_window, text="选择下注类型:").pack()
        tk.Radiobutton(sim_window, text="数字", variable=bet_var, value="Number").pack(anchor=tk.W)
        tk.Radiobutton(sim_window, text="奇偶", variable=bet_var, value="Odd/Even").pack(anchor=tk.W)
        tk.Radiobutton(sim_window, text="列", variable=bet_var, value="Column").pack(anchor=tk.W)

        # 输入模拟次数
        tk.Label(sim_window, text="输入模拟总次数(请输入20的整数倍):").pack()
        total_spins_entry = tk.Entry(sim_window)
        total_spins_entry.pack()

        # 点击可以多次模拟，输出到同一个图像
        tk.Button(sim_window, text="开始模拟", command=run_simulation).pack()


    def return_to_main(window):
        # 返回主窗口函数
        window.destroy()
        root.deiconify()

    # 主窗口
    root = tk.Tk()
    root.title("Roulette Game Mode Selection")

    # 选择模式
    tk.Label(root, text="请选择模式：").pack()

    tk.Button(root, text="游戏模式", command=lambda: [root.withdraw(), start_game()]).pack()
    tk.Button(root, text="蒙特卡洛模拟模式", command=lambda: [root.withdraw(), start_monte_carlo_simulation()]).pack()

    root.mainloop()     # 窗口循环