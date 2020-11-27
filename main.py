"""
@Author : {Jason}
@License : (c)Copyright 2020-
@Contact : {54027901@qq.com}
@software : ${自动排班系统}"""
import tkinter.messagebox
import datetime
import re
import os

import tkinter as tk
import function as f


class ArangeDuty():
    def __init__(self):
        # a每周正常值班和周末值班的控制循环次数
        self.a = 0
        self.name_nomal_sequence = ['张旭辉', '钟晓东', '邹堪芳', '刘鹏辉', '王海涛', '苏伟健', '李琦学', '弯海峰', '李泽杰']
        self.name_weekend_sequence = ['刘鹏辉', '王海涛', '钟晓东', '张旭辉', '邹堪芳', '苏伟健', '李琦学', '弯海峰', '李泽杰']
        self.week = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        self.today = datetime.date.today()
        self.monday = datetime.date.today()
        self.sunday = datetime.date.today()
        self.one_day = datetime.timedelta(days=1)
        self.date, self.curduty = self.read_date()
        self.name_holiday = f.read_data()['name_holiday']
        while self.monday.weekday() != 0:
            self.monday -= self.one_day
        while self.sunday.weekday() != 6:
            self.sunday += self.one_day

        # 创建root
        self.root = tk.Tk()
        self.root.title("自动排班系统")
        width = 800
        height = 600
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - 700) / 2)

        # 设置窗口大小不可改变
        self.root.resizable(width=False, height=False)
        self.root.geometry(alignstr)
        # 创建文本框
        self.t = tk.Text(self.root)
        self.t.insert("end", '\r\n    我值班，我快乐，吼吼吼~~~~~~~~~    ^=^    !!!'
                             '\r\n\r\n@Author:{Jason}  @Contact:{54027901@163.com}  @History:'
                             '{20/11/21(First release)}\r\n***********************************'
                             '*********************************************\r\n本周值班人员：\r\n')

        if self.today <= self.date:
            after_work_go = f.read_data()["after_work_go"]
            back_work_next = f.read_data()['back_work_next']
            if after_work_go:
                go_rest = f.read_data()['go_rest']

                tk.messagebox.showinfo(title="提示", message="%s已经列入休假名单，将在本周值完班后，下周开始休假" % go_rest)
                # 执行本周未离队，下周离队打印输出
                self.after_work_go(go_rest)

                self.t.insert("end", "下周值班人员：\r\n")
                self.list_duty()
            if back_work_next:
                re_back = f.read_data()['re_back']
                tk.messagebox.showinfo(title="提示", message="归队人员%s，将在下周开始值班" % re_back)
                self.work_next()
                # 读入第一周排班后的顺序，加入调入的人员，就是第二周的
                self.name_nomal = f.read_data()['cache_name_nomal']
                self.name_weekend = f.read_data()['cache_name_weekend']
                self.name_holiday.remove(re_back)
                f.add_list(re_back, self.name_nomal, self.name_weekend, self.name_holiday)
            elif not back_work_next and not after_work_go:
                self.name_nomal, self.name_weekend = f.read_curent()
                self.list_duty()
        elif self.today > self.date:
            after_work_go = f.read_data()["after_work_go"]
            back_work_next = f.read_data()['back_work_next']
            if not after_work_go and not back_work_next:
                self.name_nomal, self.name_weekend = f.read_curent()

                # 计算过去了几周
                how_many_days = str(self.today - self.date)
                how_many_days = re.match('\d+', how_many_days)
                how_many_days = int(how_many_days.group())
                print(how_many_days // 7)
                how_many_week = how_many_days // 7
                # 将时间更新为本周星期日的时间
                f.update_date(self.sunday)
                # 判断是隔了几周，隔了几周，就掉几次list
                for i in range(how_many_week + 1):
                    self.loop_list()
                f.write_curent(self.name_nomal, self.name_weekend)

                # 经过loop后，需要再次将初始化self.a
                self.a = 0
                self.list_duty()
            elif after_work_go:
                data = f.read_data()
                data['after_work_go'] = False
                self.name_holiday.append(data['go_rest'])
                data['name_holiday'] = self.name_holiday
                f.write_data(data)
                # 读入第一周值班，第二周离队的状态，判断当前情况是过了一周，还是过了大于一周，如果一周，输出第二周离队状态，如果n周，loop
                # n次
                how_many_days = str(self.today - self.date)
                how_many_days = re.match('\d+', how_many_days)
                how_many_days = int(how_many_days.group())
                how_many_week = how_many_days // 7
                # 将时间更新为本周星期日的时间
                f.update_date(self.sunday)
                print(how_many_week)
                if how_many_week < 1:
                    self.name_nomal = f.read_data()['after_work_go_name_nomal']
                    print("0000000", self.name_nomal)
                    self.name_weekend = f.read_data()['after_work_go_name_weekend']
                    f.write_curent(self.name_nomal, self.name_weekend)
                    self.list_duty()
                elif how_many_week >= 1:
                    for i in range(how_many_week):
                        self.loop_list()
            if back_work_next:
                data = f.read_data()
                re_back = data['re_back']
                data['back_work_next'] = False
                self.name_holiday.remove(re_back)
                data['name_holiday'] = self.name_holiday
                self.name_nomal = f.read_data()['cache_name_nomal']
                self.name_weekend = f.read_data()['cache_name_weekend']
                f.add_list(re_back, self.name_nomal, self.name_weekend, self.name_holiday)
                f.write_data(data)
                f.write_curent(self.name_nomal, self.name_weekend)
                # 计算过去了几周
                how_many_days = str(self.today - self.date)
                how_many_days = re.match('\d+', how_many_days)
                how_many_days = int(how_many_days.group())
                how_many_week = how_many_days // 7
                # 将时间更新为本周星期日的时间
                f.update_date(self.sunday)
                if how_many_week < 1:
                    self.a = 0
                    self.list_duty()
                elif how_many_week >= 1:
                    for i in range(how_many_week):
                        self.loop_list()
                    # 经过loop后，需要再次将初始化self.a
                    self.a = 0
                    self.list_duty()
        #  创建几个子菜单
        # 文件子菜单
        self.file = tk.Menu(self.root, tearoff=False)
        self.file_1 = self.file.add_command(label='将当前排班内容另存为', command=self.save)
        self.file_2 = self.file.add_command(label='退出', command=self.quit_program)
        # 编辑子菜单
        self.edit = tk.Menu(self.root, tearoff=False)
        self.edit1 = self.edit.add_command(label="初始化", command=self.init_name)
        self.edit2 = self.edit.add_command(label="重置", command=self.reset)
        # 帮助子菜单
        self.help = tk.Menu(self.root, tearoff=False)
        self.help1 = self.help.add_command(label="帮助文档", command=self.open_help_file)
        self.help2 = self.help.add_command(label="联系方式", command=self.cotact)
        # 主菜单
        self.menubar = tk.Menu(self.root)
        self.menubar.add_cascade(label='文件', menu=self.file)
        self.menubar.add_cascade(label='操作', menu=self.edit)
        self.menubar.add_cascade(label='帮助', menu=self.help)
        self.menubar.add_command(label='关于', command=self.about)

        self.root.config(menu=self.menubar)
        # 欢迎标签
        tk.Label(self.root, text="欢迎使用排班系统", font='Arial 15 bold', height=2, anchor='ne'
                 ).place(x=300, y=20, anchor='nw')
        self.v3 = tk.StringVar()
        self.l1 = tk.Label(self.root, textvariable=self.v3, width=70, font='Arial 10 bold')
        self.l2 = tk.Label(self.root, text="请输入归队人员（输入人员将加入到本周或下周值班<如果无，可不填> :", width=65, bg='SpringGreen')
        self.l3 = tk.Label(self.root, text='请输入即将休假人员（输入人员将在本周或下周从值班人员中剔除<如果无，可不填>) :', width=65, bg='LightPink')
        self.v1 = tk.StringVar()
        self.v2 = tk.StringVar()
        # 用于显示值班人员或者调整后得标签
        self.l4 = tk.Label(self.root, textvariable=self.v1, bg='cyan', font='Arial 10', anchor='nw')
        self.l5 = tk.Label(self.root, textvariable=self.v2, bg='gold', font='Arial 10', anchor='nw')
        self.v1.set("当前可值班人员为：%s" % self.name_nomal)
        self.v2.set("当前休假人员为：%s" % self.name_holiday)
        # 两个文本输入框，返回和休假
        self.e1 = tk.Entry(self.root, width=15)
        self.e2 = tk.Entry(self.root, width=15)
        # 人员变动后必须及时调整curent值班序列，否则多周后将变动后持续出错
        self.b1 = tk.Button(self.root, text="确 定", width=6, command=self.back_work)
        self.b2 = tk.Button(self.root, text="确 定", width=6, command=self.go_holiday)
        self.b3 = tk.Button(self.root, text='排 班', font='Arial 18 bold', width=6, height=3, command=self.arr_duty)

        # 标签l1的显示内容：今日值班人员

        self.to = self.curduty + self.today_duty_name()

        self.scroll = tk.Scrollbar()
        self.scroll.place(x=590, y=195, width=20, height=316)
        # 关联文本框
        self.scroll.config(command=self.t.yview)
        self.t.config(yscrollcommand=self.scroll.set)

        self.v3.set(self.to)
        self.l1.place(x=20, y=60, anchor='nw')
        self.l2.place(x=20, y=85, anchor='nw')
        self.l3.place(x=20, y=110, anchor='nw')
        self.l5.place(x=20, y=135, anchor='nw')
        self.l4.place(x=20, y=162, anchor='nw')

        self.b1.place(x=585, y=80, anchor='nw')
        self.b2.place(x=585, y=110, anchor='nw')
        self.b3.place(x=650, y=400, anchor='nw')

        self.e1.place(x=485, y=85, anchor='nw')
        self.e2.place(x=485, y=110, anchor='nw')

        self.t.place(x=30, y=195)
        self.t.see('end')
        self.t.update()

        self.root.mainloop()

    def read_date(self):
        with open('date_file.txt', 'r') as f:
            date = f.read()
            date = datetime.date(*map(int, date.split('-')))
        today_ch = self.today.strftime("%Y{y}%m{m}%d{d}").format(y="年", m='月', d='日')
        # a = self.arr_duty()
        # print(a)
        date_welcome = "今天是 %s " % str(today_ch)
        return date, date_welcome

    # 增加新人，调入
    def add_person(self):

        pass

    # 调走或离职
    def del_person(self):
        pass

    # 本周值班，下周离队
    def after_work_go(self, go_rest):
        data = f.read_data()
        data['after_work_go'] = True
        # 重新读入初始值班顺序
        self.name_nomal, self.name_weekend = f.read_curent()
        self.a = 0
        # 清空文本
        self.t.delete(1.0, "end")
        self.t.insert("end", "本周值班人员：\r\n")
        self.list_duty()  # 此处会更改当前值班序列

        self.name_nomal.remove(go_rest)
        self.name_weekend.remove(go_rest)
        self.name_holiday.append(go_rest)

        data['after_work_go_name_nomal'] = self.name_nomal
        data['after_work_go_name_weekend'] = self.name_weekend
        f.write_data(data)

    # 请假休假
    def go_holiday(self):
        go_rest = self.e2.get()
        # 将go_rest保存，再次大开始调用
        data = f.read_data()
        data["go_rest"] = go_rest
        f.write_data(data)
        if go_rest not in self.name_nomal and len(go_rest) != 0:
            tk.messagebox.showinfo(title="输入有误", message="您输入的名称错误或其正在休假中，请重新输入即将休假人员")
            go_rest = ''
        elif go_rest in self.name_nomal:
            go = tk.messagebox.askyesno(title='提示',
                                        message='休假人员是否本周值完班再休假？'
                                                '（注：如果休假人员本周本来就不用值班，选择《是》将不会被加入到本周值班列表中。）')
            # 本周值完班后再休假
            if go:
                # 如果执行本周值完班再休假，将此情况写入缓存，本周再次打开时（today<=date)，再一次自动调用本周值完班再离队，当下周或
                # 下几周（today>date)打开时,首先将after_work_go改为false(这样 update时间后，不会再次跳入，本周值完班再休假)，
                # 如果是下周打开，直接读入第二周离队状态，如果是下几周后，读入离队状态从第二周开始loop
                self.after_work_go(go_rest)
                self.v1.set("当前可值班人员更改为：%s" % self.name_nomal)
                self.v2.set("当前休假人更改员为：%s" % self.name_holiday)
                self.t.insert("end", "下周值班人员：\r\n")
                self.list_duty()



            else:
                # 重新读入初始值班顺序
                self.name_nomal, self.name_weekend = f.read_curent()
                # 清空文本
                self.t.delete(1.0, "end")
                self.a = 0
                self.t.insert("end", "本周值班人员：\r\n")
                self.name_nomal.remove(go_rest)
                self.name_weekend.remove(go_rest)
                f.write_curent(self.name_nomal, self.name_weekend)
                self.name_holiday.append(go_rest)
                data = f.read_data()
                data['name_holiday'] = self.name_holiday
                f.write_data(data)
                self.v1.set("当前可值班人员更改为：%s" % self.name_nomal)
                self.v2.set("当前休假人更改员为：%s" % self.name_holiday)
                self.list_duty()
                self.to = self.curduty + self.today_duty_name()
                self.v3.set(self.to)
                self.t.insert("end", "下周值班人员：\r\n")
                self.list_duty()

        else:
            pass

    # 下周归队
    def work_next(self):
        data = f.read_data()
        data['back_work_next'] = True
        print("执行back_work_next")
        print(data['back_work_next'])
        f.write_data(data)
        data = f.read_data()
        print(data)
        # 重新读入初始值班顺序
        self.name_nomal, self.name_weekend = f.read_curent()
        # 清空文本
        self.t.delete(1.0, "end")
        self.t.insert("end", "本周值班人员：\r\n")
        # 程序打开时，已经调用了一次排班，self.a变为7，这里重新排班需要重置回0
        self.a = 0
        self.list_duty()

        # (还未返回的下一次序列)将当前序列写入缓存（下次试试能不能用多进程解决这个问题）
        data = f.read_data()
        data['cache_name_nomal'] = self.name_nomal
        data['cache_name_weekend'] = self.name_weekend
        f.write_data(data)

    def back_work_current(self, re_back):
        data = f.read_data()
        data['back_work_next'] = False
        f.write_data(data)
        # 重新读入初始值班顺序
        self.name_nomal, self.name_weekend = f.read_curent()  # 当休假返回时，重复读入
        self.name_holiday.remove(re_back)
        data = f.read_data()
        data['name_holiday'] = self.name_holiday
        f.write_data(data)
        f.add_list(re_back, self.name_nomal, self.name_weekend, self.name_holiday)
        self.v1.set("当前休假人更改员为：%s" % self.name_holiday)
        self.v2.set("当前可值班人员更改为：%s" % self.name_nomal)
        # 重写本周列表
        f.write_curent(self.name_nomal, self.name_weekend)
        self.a = 0
        # 清空文本
        self.t.delete(1.0, "end")
        self.t.insert("end", "本周值班人员：\r\n")
        self.list_duty()
        self.to = self.curduty + self.today_duty_name()
        self.v3.set(self.to)
        self.t.insert("end", "下周值班人员：\r\n")
        self.list_duty()

    def back_work(self):
        re_back = self.e1.get()
        data = f.read_data()
        data['re_back'] = re_back
        f.write_data(data)
        if re_back not in self.name_holiday and len(re_back) != 0:
            tk.messagebox.showinfo(title="输入有误", message="您输入的名称错误或其已在值班人员列表，请重新输入正确的返回人员")
            re_back = ''
        elif re_back in self.name_holiday:
            accept_re = tk.messagebox.askyesno(title='提示',
                                               message='休假返回人员是否从本周开始值班？（<是>：本周开始值班|<否>：下周开始值班）')
            # 休假归队人员本周开始值班
            if accept_re:
                self.back_work_current(re_back)

            # 休假归队人员下周开始值班
            else:
                self.work_next()

                # 调用后值班顺序已经改变，重新读入修改后写入current，避免归队后紧接着休假，读入下一周序列
                # 此列表相当于休假归队，本周就开始值班的列表
                self.name_nomal, self.name_weekend = f.read_curent()
                print('出实话读入', self.name_weekend)
                f.add_list(re_back, self.name_nomal, self.name_weekend, self.name_holiday)
                print('0次,', self.name_weekend)
                # 此时读入缓存内容接着执行下面操作，curent列表将不会被改变
                self.name_nomal, self.name_weekend = f.read_data()['cache_name_nomal'], f.read_data()[
                    'cache_name_weekend']
                print('1次', self.name_weekend)
                self.name_holiday.remove(re_back)
                print("下一次", f.read_data()['back_work_next'])
                f.add_list(re_back, self.name_nomal, self.name_weekend, self.name_holiday)
                self.v1.set("当前休假人更改员为：%s" % self.name_holiday)
                self.v2.set("当前可值班人员更改为：%s" % self.name_nomal)
                self.t.insert("end", "下周值班人员：\r\n")
                # 此时为值班列表为休假返回第一周未参加值班，第二周参加值班的值班序列列表
                data = f.read_data()
                data['back_work_next_name_nomal'] = self.name_nomal
                data['back_work_next_name_weekend'] = self.name_weekend
                f.write_data(data)
                print('2次，', self.name_weekend)
                print("adfadsfasdf", data['back_work_next'])
                self.list_duty()

    # 排班
    def arr_duty(self):
        # 清空文本
        # self.t.delete(1.0, "end")
        self.t.insert("end", '\r\n\r\n***********************************'
                             '*********************************************\r\n下一周值班人员：\r\n')
        self.list_duty()

    # 按照周循环调整值班列表顺序
    def loop_list(self):
        for i in range(self.a, self.a + 5):
            # 日期
            day = self.monday + datetime.timedelta(days=i)

            duty = self.name_nomal.pop(0)
            self.name_nomal.append(duty)
        for i in range(self.a + 5, self.a + 7):
            day = self.monday + datetime.timedelta(days=i)
            duty = self.name_weekend.pop(0)
            self.name_weekend.append(duty)
        self.a = self.a + 7

    def list_duty(self):
        # # 提示local variable 'today_duty' referenced before assignment,
        global today_duty

        for i in range(self.a, self.a + 5):
            day = self.monday + datetime.timedelta(days=i)
            duty = self.name_nomal.pop(0)

            if day == self.today:
                today_duty = self.week[i - self.a] + ",今日值班员为【%s】,祝您生活愉快！！！ ^=^ " % duty
            day = str(day) + "-" + self.week[i - self.a] + " ---- 值班人员为：" + duty + "\n\r"
            self.name_nomal.append(duty)
            self.t.insert('end', day)
            self.t.see('end')
            self.t.update()

        for i in range(self.a + 5, self.a + 7):
            day = self.monday + datetime.timedelta(days=i)
            duty = self.name_weekend.pop(0)
            if day == self.today:
                today_duty = self.week[i - self.a] + ",今日值班员为【%s】,祝您生活愉快！！！ ^=^ " % duty
            day = str(day) + "-" + self.week[i - self.a] + " ---- 值班人员为：" + duty + '\n\r'
            self.name_weekend.append(duty)
            self.t.insert('end', day)
            self.t.see('end')
            self.t.update()
        self.a = self.a + 7

    def today_duty_name(self):
        global today_duty
        data = f.read_data()
        data['name_nomal'] = self.name_nomal
        data['name_weekend'] = self.name_weekend
        f.write_data(data)
        for i in range(self.a, self.a + 5):
            day = self.monday + datetime.timedelta(days=i)
            duty = self.name_nomal.pop(0)
            if day == self.today:
                today_duty = self.week[i - self.a] + ",今日值班员为【%s】,祝您生活愉快！！！ ^=^ " % duty
            self.name_nomal.append(duty)
        for i in range(self.a + 5, self.a + 7):
            day = self.monday + datetime.timedelta(days=i)
            duty = self.name_weekend.pop(0)
            if day == self.today:
                today_duty = self.week[i - self.a] + ",今日值班员为【%s】,祝您生活愉快！！！ ^=^ " % duty
            self.name_weekend.append(duty)
        date = f.read_data()
        self.name_nomal = date['name_nomal']
        self.name_weekend = date['name_weekend']
        return today_duty

        # 初始化是调用，添加休假人员

    def add_holiday(self):
        h_name = e1.get()
        if h_name not in self.name_nomal_sequence and h_name != '':
            tk.messagebox.showinfo(title='输入错误', message='您输入的名称错误，请重新输入！')
        elif h_name == '':
            current_holiday_name.set("当前休假人员：" + str(self.name_holiday))
            self.name_nomal = self.name_nomal_sequence
            self.name_weekend = self.name_weekend_sequence
            current_duty_name.set('当前值班人员为：' + str(self.name_nomal))
            data = f.read_data()
            data['name_holiday'] = self.name_holiday
            f.write_data(data)

        elif h_name in self.name_nomal_sequence:
            self.name_holiday.append(h_name)
            current_holiday_name.set("当前休假人员：" + str(self.name_holiday))
            self.name_nomal_sequence.remove(h_name)
            self.name_weekend_sequence.remove(h_name)
            self.name_nomal = self.name_nomal_sequence
            self.name_weekend = self.name_weekend_sequence
            current_duty_name.set('当前值班人员为：' + str(self.name_nomal))
            data = f.read_data()
            data['name_holiday'] = self.name_holiday
            f.write_data(data)

    # 初始化时，列出本周正常值班人员
    def list_nomal(self):
        monday_name = e2.get()
        if monday_name not in self.name_nomal:
            tk.messagebox.showinfo(title='输入错误', message='您输入的名称错误，或其在休假列表中，请重新输入')
        elif monday_name in self.name_nomal:
            monday_index = self.name_nomal.index(monday_name)
            current_nomal = []
            for i in range(len(self.name_nomal)):
                try:
                    n = self.name_nomal.pop(monday_index)
                    current_nomal.append(n)
                except:
                    break
            for i in range(len(self.name_nomal)):
                current_nomal.append(self.name_nomal[i])
            self.name_nomal = current_nomal
            tk.messagebox.showinfo(title="确认", message='工作日值班列表已初始化')

    def list_weekend(self):
        saturday_name = e3.get()
        if saturday_name not in self.name_weekend:
            tk.messagebox.showinfo(title='输入错误', message='您输入的名称错误，或其在休假列表中，请重新输入')
        elif saturday_name in self.name_weekend:
            saturday_index = self.name_weekend.index(saturday_name)
            current_weekend = []
            for i in range(len(self.name_weekend)):
                try:
                    n = self.name_weekend.pop(saturday_index)
                    current_weekend.append(n)
                except:
                    break
            for i in range(len(self.name_weekend)):
                current_weekend.append(self.name_weekend[i])
            self.name_weekend = current_weekend
            tk.messagebox.showinfo(title="确认", message='周末值班列表已初始化')

    def write_current_reset(self):
        if e2.get() == '' or e3.get() == '':
            tk.messagebox.showinfo(title='错误', message='本周一或本周六值班人员未输入，初始化失败,请按照要求输入相应人员！')
        else:
            f.write_curent(self.name_nomal, self.name_weekend)
            self.reset()

    def build_window(self):
        global e1, e2, e3, current_holiday_name, current_duty_name, window
        window = tk.Toplevel()
        width = 600
        height = 300
        screenwidth = window.winfo_screenwidth()
        screenheight = window.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - 700) / 2)
        # 设置窗口大小不可改变
        window.resizable(width=False, height=False)
        window.geometry(alignstr)
        window.title("初始化")
        current_holiday_name = tk.StringVar()
        current_duty_name = tk.StringVar()
        l1 = tk.Label(window, textvariable=current_holiday_name,  width=80)
        l2 = tk.Label(window, textvariable=current_duty_name, width=80)
        l3 = tk.Label(window, text="请输入当前休假人员，系统将自动将其加入休假列表^=^",bg='gold', width=43)
        l4 = tk.Label(window, text='请输入本周星期一值班人员:', width=50)
        l5 = tk.Label(window, text='请输入本周星期六值班人员：', width=50)
        e1 = tk.Entry(window, width=15)
        e2 = tk.Entry(window, width=15)
        e3 = tk.Entry(window, width=15)
        b1 = tk.Button(window, text="添加", command=self.add_holiday)
        b2 = tk.Button(window, text="确定", command=self.list_nomal)
        b3 = tk.Button(window, text="确定", command=self.list_weekend)
        b4 = tk.Button(window,
                       text="确认本周值班无误后点击我",
                       command=self.write_current_reset,
                       width= 40,
                       height=2)

        l1.place(x=20, y=20, anchor='nw')
        l2.place(x=20, y=40, anchor='nw')
        l3.place(x=20, y=80, anchor='nw')
        l4.place(x=20, y=130, anchor='nw')
        l5.place(x=20, y=180, anchor='nw')
        e1.place(x=340, y=80, anchor='nw')
        e2.place(x=340, y=130, anchor='nw')
        e3.place(x=340, y=180, anchor='nw')
        b1.place(x=440, y=80)
        b2.place(x=440, y=130)
        b3.place(x=440, y=180)
        b4.place(x=180, y=230)
        current_holiday_name.set("当前休假人员：" + str(self.name_holiday))
        current_duty_name.set("当前值班人员：")

    def shut_open(self):
        window.destroy()
        self.root.wm_deiconify()
        self.root.update()

    # 初始化
    def init_name(self):
        yes = tk.messagebox.askyesno(title='注意',
                                     message='初始化将以本周值班为基准，对后续值班进行编排，确定请选择【是】，返回'
                                             '请选择【否】')
        # 如果是，将当前值班正常和周末值班列表请空，获取输入的当前休假人员，将其添加到休假人员列表
        if yes:
            tk.messagebox.showinfo(title='提示',
                                         message='初始化需首先确定休假人员，如果无休假人员，请直接点击【添加】按钮')
            self.name_nomal = []
            self.name_weekend = []
            self.name_holiday = []
            self.build_window()
            self.root.withdraw()
            window.protocol('WM_DELETE_WINDOW', self.shut_open)
            window.mainloop()
        # 如果否，pass
        else:
            pass

    # 重置
    def reset(self):
        self.root.destroy()
        run()

    # 退出
    def quit_program(self):
        self.root.destroy()

    # 将当前内容保存到txt
    def save(self):
        cotent = self.t.get('0.0', 'end')
        with open('duty_content.txt', 'w') as f:
            f.write(cotent)
        os.system('duty_content.txt')

    # 打开帮助文档
    def open_help_file(self):
        os.system('help.txt')

    # 联系方式
    def cotact(self):
        tk.messagebox.showinfo(title="联系我哈",
                               message="电话：0752—575222转34517\r\nEmail:54027901@163.com")

    # 关于
    def about(self):

        window = tk.Toplevel()
        window.title("关于")
        width = 400
        height = 600
        screenwidth = window.winfo_screenwidth()
        screenheight = window.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - 700) / 2)
        # 设置窗口大小不可改变
        window.resizable(width=False, height=False)
        window.geometry(alignstr)

        w_l1 = tk.Label(window, text=""
                                     "\r\n关于软件\r\n"
                                     "   写这个软件的目的，完全出于学习和探索，所有代码全部开源，\r\n"
                                     "并已上传至Github,方便有需要的朋友下载使用，并且非常欢迎各位\r\n"
                                     "同仁一起交流学习。\r\n"
                                     "\r\n")
        w_l2 = tk.Label(window, text=""
                                     "关于作者\r\n"
                                     "大家好，我是Jason，一个爱好广泛的男人，阔以上九天摘月，\r\n"
                                     "也能下五洋捉鳖，喜欢潜水，滑翔伞，登山.... 俗话说的好，\r\n"
                                     "不会烘培的飞行员不是好户外人，不会玩音乐的水族爱好者不是\r\n"
                                     "好厨师，不会画画的极限爱好者不是好程序员，吼吼吼~~")
        w_l3 = tk.Label(window, text="\r\n加好友加关注")

        canvas = tk.Canvas(window, width=360, height=150)
        canvas.place(x=20, y=400, anchor='nw')
        img1 = tk.PhotoImage(file="imge/public.gif")
        img2 = tk.PhotoImage(file="imge/asistant.gif")
        canvas.create_image(35, 15, anchor='nw', image=img1)
        canvas.create_image(200, 15, anchor="nw", image=img2)
        w_l1.pack()
        w_l2.pack()
        w_l3.pack()
        window.mainloop()


def run():
    arange_duty = ArangeDuty()


if __name__ == '__main__':
    run()
