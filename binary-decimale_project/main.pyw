import tkinter as tk
from random import randint
import sys
import os
import datetime as dt

# settings
deg_bg_color = '#d7d8e0'
normal_width = 1200
normal_height = 585

cd = os.getcwd()

level, checked_levels, complexity, cnt_w_ans, cnt_r_ans = 0, 0, 0, 0, 0
k = 1  # коэффициент сложности


def log_w(row):
    if level == 0:
        log = open('logs.txt', 'w')
    else:
        log = open('logs.txt', 'a')
    log.write(row + '\n')
    log.close()


class Main(tk.Frame):
    def __init__(self):
        global cnt_r_ans, cnt_w_ans
        super().__init__(root)
        # строка вверху
        deg_bar = tk.Frame(bg=deg_bg_color, bd=1)
        deg_bar.pack(side=tk.TOP, fill=tk.X)
        # label таймера
        self.timer_label = tk.Label(deg_bar, bg=deg_bg_color, fg='green', bd=1, justify='center', anchor='c',
                                    font=f'Arial 16', width=5,
                                    text=f'0')
        self.timer_label.pack(side=tk.LEFT)
        # таблица со степенями двойки
        self.deg_img = tk.PhotoImage(file=cd + '/images/' + 'degrees2.gif')
        top_image = tk.Label(deg_bar, image=self.deg_img, bd=0)
        top_image.pack(side=tk.LEFT)
        # отображение количества ошибок и правильных ответов
        self.wr_counter = tk.Label(deg_bar, bg=deg_bg_color, fg='black', bd=0, anchor='w', justify='left',
                                   font=f'Arial 16',
                                   text=f'  Правильных: {cnt_r_ans}\n  Ошибок: {cnt_w_ans}')
        self.wr_counter.pack(side=tk.LEFT)
        # кнопка завершения
        otst = tk.Label(deg_bar, bd=0, text='       ', bg=deg_bg_color)
        otst.pack(side=tk.LEFT)
        self.finish_img = tk.PhotoImage(file=cd + '/images/' + 'finish.gif')
        finish_btn = tk.Button(deg_bar, image=self.finish_img, bg=deg_bg_color,
                               bd=1, command=self.finish, font='Arial 15')
        finish_btn.pack(side=tk.LEFT)

        # очередь таймеорв
        self.q = {}
        self.q_complexity = {}
        self.cur_timer = -1

        self.timer_running = 0
        self.timer_seconds = 0

    def add_timer_request(self, num, complexity):
        self.q[num] = dt.datetime.now()
        self.q_complexity[num] = complexity
        if len(self.q) <= 1:
            try:
                self.timer_next()
            except KeyError:
                sec = complexity * 5000
                # print(sec)
                self.timer_start(sec)

    def delete_timer_request(self, num, delay):
        self.q.pop(num)
        if self.cur_timer == num and len(self.q) != 0:
            self.after(delay, self.timer_next)
            self.timer_running = 0
        if len(self.q) == 0:
            self.timer_running = 0
            self.timer_label['text'] = '0'

    def timer_start(self, sec):
        try:
            keys = list(self.q.keys())
            self.cur_timer = keys[0]
        except IndexError:
            pass

        self.timer_seconds = float("{0:.1f}".format(sec / 1000))
        self.timer_running = 1
        self.timer_tick()

    def timer_next(self):
        try:
            keys = list(self.q.keys())
            self.cur_timer = keys[0]
        except IndexError:
            pass

        # да, время для отсчёта в левом углу и таймера самого задания задаётся одинаково в двух местах
        # кривовато, но это оказалось самым удобным решением для меня тут
        # задаётся время для отсчёта в левом верхнем углу
        if self.q_complexity[self.cur_timer] < 7:
            sec = 5000 * self.q_complexity[self.cur_timer]
        else:
            sec = 35000

        delt = dt.datetime.now() - self.q[self.cur_timer]
        delt_sec = delt.seconds * 1000 + (delt.microseconds // 1000)
        self.timer_seconds = float("{0:.1f}".format((sec - delt_sec) / 1000))
        # print(self.timer_seconds)
        self.timer_running = 1
        self.timer_tick()

    def timer_tick(self):
        if self.timer_running and self.timer_seconds:
            app.after(100, self.timer_tick)  # перезапустить через 0.1 сек
            # уменьшить таймер
            self.timer_seconds -= 0.1
            self.timer_update(abs(self.timer_seconds))

    def timer_update(self, val):
        val = float("{0:.1f}".format(val))
        if val == 0.0 or val == 0.1:
            val = 0
        self.timer_label['text'] = str(val)

    def finish(self):
        global root
        root.withdraw()
        ResultWindow()


# окно для результата
class ResultWindow(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()

    def init_child(self):
        global checked_levels, cnt_r_ans, root
        try:
            result = int(cnt_r_ans / checked_levels * 100)
        except ZeroDivisionError:
            result = 0
        self.title('Результаты')
        self.geometry('380x200+400+300')
        self.resizable(False, False)

        result_bar = tk.Frame(self, bd=5)
        result_bar.pack(expand=1)

        bal = tk.Label(result_bar, text='баллов: ', font='Arial 16')
        result_b = tk.Label(result_bar, text=str(result), font='Arial 50', fg='blue')
        result_b.pack(side=tk.RIGHT)
        bal.pack(side=tk.RIGHT)
        otst = tk.Label(result_bar, text='  ', font='Arial 20')
        otst.pack(side=tk.RIGHT)

        if 90 <= result <= 100:
            result = 5
        elif 78 <= result < 90:
            result = 4
        elif 66 <= result < 78:
            result = 3
        else:
            result = 2

        bal = tk.Label(result_bar, text='оценка: ', font='Arial 16')
        bal.pack(side=tk.LEFT)
        result_a = tk.Label(result_bar, text=str(result), font='Arial 50', fg='blue')
        result_a.pack(side=tk.LEFT)

        quit_bar = tk.Frame(self, bd=0)
        quit_bar.pack(side=tk.BOTTOM, fill=tk.X)
        quit_button = tk.Button(quit_bar, text='выйти', bd=1, font='Arial 17', command=root.destroy)
        quit_button.pack(fill=tk.X)

        otst_bar = tk.Frame(self, bd=0)
        otst_bar.pack(side=tk.BOTTOM, fill=tk.X)
        otst = tk.Label(otst_bar, font='Arial 7', text='@ortieom did it', fg='gray70')
        otst.pack()

        details_bar = tk.Frame(self, bd=2)
        details_bar.pack(side=tk.BOTTOM, fill=tk.X)
        detailed_res = tk.Label(details_bar, font='Helvetica 18',
                                text=f'Всего: {checked_levels}      Правильных: {cnt_r_ans}')
        detailed_res.pack()

        self.protocol("WM_DELETE_WINDOW", sys.exit)

        self.grab_set()
        self.focus_set()


def task_gen(complexity, level):
    app.add_timer_request(level, complexity)
    task = [0 for _ in range(11)]
    task_dec = 0
    for _ in range(complexity):
        rand = randint(0, 10)
        if task[rand] == 0:
            task[rand] = 1
        else:
            task[rand] = 0
    for i in range(len(task)):
        if task[i] == 1:
            task_dec += 2 ** (10 - i)
    return task, task_dec


def task_create_next():
    Answer()


class Answer(tk.Frame):
    def __init__(self):
        # вычисление сложности
        global level, complexity, k
        self.level = level
        if level % k == 0:
            complexity += 1
            k += level
        level += 1
        self.complexity = complexity

        self.cur_dec_value = 0
        # картинки
        self.zero_img = tk.PhotoImage(file=cd + '/images/' + 'zero.gif')
        self.one_img = tk.PhotoImage(file=cd + '/images/' + 'one.gif')
        self.red_zero_img = tk.PhotoImage(file=cd + '/images/' + 'red_zero.gif')
        self.red_one_img = tk.PhotoImage(file=cd + '/images/' + 'red_one.gif')
        self.status_img0 = tk.PhotoImage(file=cd + '/images/' + 'cross.gif')
        self.status_img1 = tk.PhotoImage(file=cd + '/images/' + 'check.gif')
        self.red_one_img = tk.PhotoImage(file=cd + '/images/' + 'red_one.gif')
        self.checked_flag = 0  # проверен ли таск
        self.value = [0 for _ in range(11)]  # текущее значение
        self.task, self.task_dec = task_gen(self.complexity, self.level)  # таск
        # окно заданий
        self.task_bar = tk.Frame()
        self.task_bar.pack(side=tk.TOP, fill=tk.X)
        super().__init__(root)
        self.init_task()

        # таймеры
        # второй раз задаётся время уже для проверки и генерации нового
        if complexity < 7:
            auto_check_seconds = 5000 * self.complexity
            new_task_seconds = 3200 * self.complexity
        else:
            auto_check_seconds = 35000
            new_task_seconds = 22400

        self.autocheck(auto_check_seconds)
        root.after(new_task_seconds, task_create_next)  # новое задание
        # print(f'your task for level {self.level} is {self.task}')

    def check(self):
        global cnt_r_ans, cnt_w_ans, checked_levels
        checked_levels += 1
        self.check_btn.config(state='disabled')

        # log_w(f'         # {str(self.level + 1).rjust(3, " ")} | {str(self.task_dec).rjust(7," ")}, {str(self.task)}')

        if self.value == self.task and self.checked_flag != 1:
            cnt_r_ans += 1
            status_image = tk.Label(self.task_bar, image=self.status_img1, bd=1)
            status_image.pack(side=tk.LEFT)
            self.checked_flag = 1
            self.destroy_bar(1000)
            # print('correct')
            app.wr_counter.configure(text=f'  Правильных: {cnt_r_ans}\n  Ошибок: {cnt_w_ans}')
            # log_w(f'Checked: # {str(self.level + 1).rjust(3, " ")} |  Answer: {self.value} | correct')

            app.delete_timer_request(self.level, 1000)

            return 1

        elif self.value != self.task and self.checked_flag != 1:
            cnt_w_ans += 1
            status_image = tk.Label(self.task_bar, image=self.status_img0, bd=1)
            status_image.pack(side=tk.LEFT)
            self.checked_flag = 1
            # Осторожно, дальше много сравнений для отображения ошибок (11)!

            btns = {"btn0": self.button1, "btn1": self.button2, "btn2": self.button3,
                    "btn3": self.button4, "btn4": self.button5, "btn5": self.button6,
                    "btn6": self.button7, "btn7": self.button8, "btn8": self.button9,
                    "btn9": self.button10, "btn10": self.button11}

            for i in range(11):
                if self.value[i] != self.task[i]:
                    self.neutral_to_chaos(btns[f"btn{i}"])

            self.destroy_bar(3000)
            # print('wrong')
            app.wr_counter.configure(text=f'  Правильных: {cnt_r_ans}\n  Ошибок: {cnt_w_ans}')
            # log_w(f'Checked: # {str(self.level + 1).rjust(3, " ")} |  Answer: {self.value} | wrong')

            app.delete_timer_request(self.level, 3000)

            return 0

    def autocheck(self, ms):
        if not self.checked_flag:
            self.task_bar.after(ms, self.check)

    # изменение состояния кнопки и вызов проверки
    def zero_to_one(self, button, task_text):
        button_text = button.cget('text')
        if len(button_text) == 2:
            binary_id = (int(button_text) // 10)
        else:
            binary_id = 10
        # print(f'key {binary_id + 1} was pressed in level {self.level}')
        if int(button_text) % 10 == 0:
            button.config(image=self.one_img, text=str(binary_id) + '1')
            self.value[binary_id] = 1
            self.cur_dec_value += 2 ** abs(10 - binary_id)
        else:
            button.config(image=self.zero_img, text=str(binary_id) + '0')
            self.value[binary_id] = 0
            self.cur_dec_value -= 2 ** abs(10 - binary_id)
        task_text.configure(text=f'{str(self.task_dec)} =\n--------\n{self.cur_dec_value}')

        # print(f'your answer for level {self.level} now {self.value}')

    def neutral_to_chaos(self, button):
        button_text = button.cget('text')
        if int(button_text) % 10 == 0:
            button.config(image=self.red_zero_img)
        else:
            button.config(image=self.red_one_img)

    def init_task(self):
        task_dec = tk.Button(self.task_bar, justify='center', height=3, width=6,
                             font='Arial 15', bd=0, text=f'{str(self.task_dec)} =\n--------\n{0}')
        task_dec.pack_propagate(0)
        task_dec.pack(side=tk.LEFT)
        # Осторожно, дальше много кнопок (11)!
        self.button1 = tk.Button(self.task_bar, bd=0, image=self.zero_img, text='00')
        self.button1.config(command=lambda: self.zero_to_one(self.button1, task_dec))
        self.button1.pack(side=tk.LEFT)
        self.button2 = tk.Button(self.task_bar, bd=0, image=self.zero_img, text='10')
        self.button2.config(command=lambda: self.zero_to_one(self.button2, task_dec))
        self.button2.pack(side=tk.LEFT)
        self.button3 = tk.Button(self.task_bar, bd=0, image=self.zero_img, text='20')
        self.button3.config(command=lambda: self.zero_to_one(self.button3, task_dec))
        self.button3.pack(side=tk.LEFT)
        self.button4 = tk.Button(self.task_bar, bd=0, image=self.zero_img, text='30')
        self.button4.config(command=lambda: self.zero_to_one(self.button4, task_dec))
        self.button4.pack(side=tk.LEFT)
        self.button5 = tk.Button(self.task_bar, bd=0, image=self.zero_img, text='40')
        self.button5.config(command=lambda: self.zero_to_one(self.button5, task_dec))
        self.button5.pack(side=tk.LEFT)
        self.button6 = tk.Button(self.task_bar, bd=0, image=self.zero_img, text='50')
        self.button6.config(command=lambda: self.zero_to_one(self.button6, task_dec))
        self.button6.pack(side=tk.LEFT)
        self.button7 = tk.Button(self.task_bar, bd=0, image=self.zero_img, text='60')
        self.button7.config(command=lambda: self.zero_to_one(self.button7, task_dec))
        self.button7.pack(side=tk.LEFT)
        self.button8 = tk.Button(self.task_bar, bd=0, image=self.zero_img, text='70')
        self.button8.config(command=lambda: self.zero_to_one(self.button8, task_dec))
        self.button8.pack(side=tk.LEFT)
        self.button9 = tk.Button(self.task_bar, bd=0, image=self.zero_img, text='80')
        self.button9.config(command=lambda: self.zero_to_one(self.button9, task_dec))
        self.button9.pack(side=tk.LEFT)
        self.button10 = tk.Button(self.task_bar, bd=0, image=self.zero_img, text='90')
        self.button10.config(command=lambda: self.zero_to_one(self.button10, task_dec))
        self.button10.pack(side=tk.LEFT)
        self.button11 = tk.Button(self.task_bar, bd=0, image=self.zero_img, text='100')
        self.button11.config(command=lambda: self.zero_to_one(self.button11, task_dec))
        self.button11.pack(side=tk.LEFT)
        otst = tk.Label(self.task_bar, bd=0, text='  ')
        otst.pack(side=tk.LEFT)
        self.check_btn = tk.Button(self.task_bar, bd=1, font='Arial 15', text='Проверить')
        self.check_btn.config(command=self.check)
        self.check_btn.pack(side=tk.LEFT)
        otst = tk.Label(self.task_bar, bd=0, text='    ')
        otst.pack(side=tk.LEFT)

    # удаление строки
    def destroy_bar(self, ms):
        self.task_bar.after(ms, self.task_bar.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    app = Main()
    app.pack()
    root.title("Тренажёр по двоичной системе счисления")
    root.geometry(f"{normal_width}x{normal_height}+50+50")
    root.resizable(False, False)

    # log_w(f'---New session---{dt.datetime.now()}')

    task1 = Answer()

    root.protocol("WM_DELETE_WINDOW", sys.exit)
    root.mainloop()
