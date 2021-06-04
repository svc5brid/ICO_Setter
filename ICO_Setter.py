from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter.font import BOLD
import hashlib
import re
import datetime

con = sqlite3.connect("ICO_Setter.db")
cur = con.cursor()
try:
    # Table作成をやってみる。
    cur.execute("""CREATE TABLE Users (Name text, ID blog, Password blog)""")
except:
    pass
try:
    # Table作成をやってみる。
    cur.execute("""CREATE TABLE DailyTasks (Date integer, DayWeek integer, TaskID integer, States integer, User integer)""")
except:
    pass
try:
    # Table作成をやってみる。
    cur.execute("""CREATE TABLE AllTasks (ID integer, Name text, Details text, ParentsTask integer, Repetition integer, Repetition2 integer, Repetition3 text, TimeRequired integer, Power integer, ICOrule integer)""")
except:
    pass
con.commit()
con.close()

editwindow = None
class main():
    def __init__(self) -> None:
        global root
        root = Tk()
        root.title("NewWindow")
        # root.geometry('1300x700')
        root.configure(background="#DBFEB8")
        TitleLabel = ttk.Label(root, text="タスクを練り上げしもの", background="#C5EDAC", foreground="#000", font=("游明朝 Demibold", "24"))
        ReloadButton = ttk.Button(root, text="更新", command=lambda:[self.Reload()])
        EditButton = ttk.Button(root, text="編集", command=lambda:[self.Edit()])
        RecentButton = ttk.Button(root, text="振り分け履歴", command=lambda:[self.Recent()])
        ReloadButton.grid(row = 0, column=2)
        EditButton.grid(row=0, column=3)
        RecentButton.grid(row=0, column=4)
        TitleLabel.grid(row = 0, column=0)
        MenuBar = Menu(root)
        root.config(menu=MenuBar)
        FileMenu = Menu(MenuBar, tearoff=0)
        MenuBar.add_cascade(label="ファイル", menu=FileMenu)
        SettingMenu = Menu(MenuBar, tearoff=0)
        MenuBar.add_cascade(label="設定", menu=SettingMenu)
        FileMenu.add_command(label="更新", command=lambda:[self.Reload()])
        FileMenu.add_command(label="編集", command=lambda:[self.Edit()])
        FileMenu.add_command(label="振り分け履歴", command=lambda:[self.Recent()])
        FileMenu.add_command(label="exit", command=lambda:[root.destroy()])
        SettingMenu.add_command(label="せってー")

        TodayFrame = ttk.Labelframe(root, text="Today", height=600, width=400)
        TomorrowFrame = ttk.Labelframe(root, text="Tomorrow", height=600, width=400)
        MonthFrame = ttk.Labelframe(root, text="Monthly", height=290, width=400)
        WeekFrame = ttk.Labelframe(root, text="Weekly", height=290, width=400)
        TodayFrame.grid(row=1, column=0, padx=10, pady=10, rowspan=2)
        TomorrowFrame.grid(row = 1, column = 1, padx=10, pady=10, rowspan=2)
        MonthFrame.grid(row = 2, column = 2, padx=10, pady=10, columnspan=3)
        WeekFrame.grid(row = 1, column = 2, padx=10, pady=10, columnspan=3)
        TodayFrame.grid_propagate(0)
        TomorrowFrame.grid_propagate(0)
        MonthFrame.grid_propagate(0)
        WeekFrame.grid_propagate(0)

        label = ttk.Label(TodayFrame, text="今日")
        label1 = ttk.Label(TomorrowFrame, text="今日")
        label2 = ttk.Label(WeekFrame, text="今日")
        label3 = ttk.Label(MonthFrame, text="今日")
        label.grid(row=1, column=1)
        label1.grid(row=1, column=1)
        label2.grid(row=1, column=1)
        label3.grid(row=1, column=1)
        
        root.mainloop()

    def Reload(self):
        print("Reload")
    
    def Edit(self):
        if editwindow == None or not editwindow.winfo_exists():
            Edit = EditWindow(root)
        else:
            print("windowが存在しているため作成しない")
    
    def Recent(self):
        print("Recent")


class EditWindow():
    def __init__(self, root) -> None:
        global editwindow
        editwindow = Toplevel()
        editwindow.title("Edit")
        editwindow.configure(background="#DBFEB8")
        # editwindow.attributes("-topmost", True)
        # editwindow.grab_set()
        self.TitleText = StringVar(value="データ編集")
        self.TitleLabel = ttk.Label(editwindow,  text="データ編集", background="#C5EDAC", foreground="#000", font=("游明朝 Demibold", "24"))
        self.TitleLabel.grid(row=0, column=0)
        self.MainFrame = ttk.Labelframe(editwindow, text="データ編集", width=700, height=300)
        self.MainFrame.grid(row=1, column=1, rowspan=4, padx=10, pady=10)
        self.MainFrame.grid_propagate(0)
        ButtonAdd = ttk.Button(editwindow, text="追加(Add)", command=lambda:[self.ChangeMethod("追加")])
        ButtonChange = ttk.Button(editwindow, text="変更(Change)", command=lambda:[self.ChangeMethod("変更")])
        ButtonDelete = ttk.Button(editwindow, text="削除(Delete)", command=lambda:[self.ChangeMethod("削除")])
        ButtonAdmin = ttk.Button(editwindow, text="管理(Admin)", command=lambda:[self.AdminEnter()])
        ButtonAdd.grid(row = 1, column=0, padx=10, pady=10)
        ButtonChange.grid(row = 2, column=0, padx=10, pady=10)
        ButtonDelete.grid(row = 3, column=0, padx=10, pady=10)
        ButtonAdmin.grid(row = 4, column=0, padx=10, pady=10)
        self.createformclass = None
        
    def ChangeMethod(self, labeltitle):
        if self.createformclass == None:
            self.createformclass = CreateForm(labeltitle, self.MainFrame)
        self.createformclass.main(labeltitle, self.MainFrame)
    def AdminEnter(self):
        AdminEntrance = Toplevel(editwindow)
        AdminEntrance.title("管理者ログイン")
        AdminEntrance.configure(background="#DBFEB8")
        AdminEntrance.attributes("-topmost", True)
        AdminEntrance.grab_set()
        Label1 = ttk.Label(AdminEntrance, text="ユーザーID")
        Label2 = ttk.Label(AdminEntrance, text="パスワード")
        UserIDEntry = ttk.Entry(AdminEntrance)
        PasswordEntry = ttk.Entry(AdminEntrance)
        ReturnButton = ttk.Button(AdminEntrance, text="取り消し", command=lambda:[AdminEntrance.destroy()])
        SubmitButton = ttk.Button(AdminEntrance, text="ログイン", command=lambda:[self.AdminLogin(UserIDEntry.get(), PasswordEntry.get(), AdminEntrance)])
        Label1.grid(row=0, column=0, padx=10, pady=5)
        Label2.grid(row=1, column=0, padx=10, pady=5)
        UserIDEntry.grid(row=0, column=1, padx=10, pady=5)
        PasswordEntry.grid(row=1, column=1, padx=5, pady=5)
        ReturnButton.grid(row=2, column=0, padx=10, pady=5)
        SubmitButton.grid(row=2, column=1, padx=5, pady=5)
    def AdminLogin(self, ID, Password, window):
        if ID == "":
            messagebox.showinfo("エラー", "IDを入力してください")
            return
        if Password == "":
            messagebox.showinfo("エラー", "IDを入力してください")
            return
        MID = ID.encode()
        MHP = Password.encode()

        HashedID = hashlib.sha256(MID).hexdigest()
        HashedPassword = hashlib.sha256(MHP).hexdigest()
        con = sqlite3.connect("ICO_Setter.db")
        cur = con.cursor()
        # cur.execute(f"INSERT INTO Users values ('svc5brid', '{HashedID}', '{HashedPassword}')")
        try:
            sql = f"select ID, Password, Name from Users where ID = '{HashedID}'"
            cur.execute(sql)
            AuthenticationInfo = cur.fetchall()
            if AuthenticationInfo[0][1] == HashedPassword:
                messagebox.showinfo("認証成功", f"ようこそ、{AuthenticationInfo[0][2]}さん。")
                window.destroy()
                root.lower()
                self.AdminWindow()
            else:
                messagebox.showinfo("認証失敗", "IDまたはパスワードが\n間違っています")
        except:
            messagebox.showinfo("認証失敗", "IDまたはパスワードが\n間違っています")
            return
        # con.commit()
        con.close()
        # print(AuthenticationInfo)

        # if AuthenticationInfo[0][1] == HashedPassword:
        #     messagebox.showinfo("認証成功しました。", "やったね！")
        # データベースから、入力されたユーザーIDとそれに付随するパスワードを取得
        # ユーザーIDが取得できなければ、returnとIDが違うということを表示
        # ユーザーIDが取得できた場合、照合。
        # 照合できたら次の画面（関数）に行く。出来なかった場合、returnとパスワードが違うということを表示
        pass
    def AdminWindow(self):
        print("This is Admin")
        pass
class CreateForm():
    def __init__(self, labeltitle, MainFrame = None) -> None:
        try:
            self.TitleEntry.grid_forget()
        except:
            pass
        if MainFrame == None:
            MainFrame = self.Mainframe
            self.Mainframe.configure(text=labeltitle)
        else:
            MainFrame.configure(text=labeltitle)
            self.Mainframe = MainFrame
        LabelText = ("タイトル※", "詳細情報", "親タスク", "繰り返し", "所要時間(分)", "力仕事", "担当者の有無")
        self.Labels = []
        for i in range(len(LabelText)):
            self.Labels.append(0)
            self.Labels[i] = ttk.Label(MainFrame, text=LabelText[i])
            if i < 3: 
                self.Labels[i].grid(row = i, column=0, pady = 5, padx = 5)
            elif i == 3:
                self.Labels[i].grid(row = i-3, column=2, pady = 5, padx = 5, rowspan = 2)
            elif i == 5 or i == 6:
                self.Labels[i].grid(row = i-2, column = 0, pady = 5, padx = 5)
            else:
                self.Labels[i].grid(row = i-2, column=2, pady = 5, padx = 5)
        self.Titles = self.GetTitles()
        Boxes = []
        for i in self.Titles.keys():
            Boxes.append(i)
        Boxes = tuple(Boxes)
        if labeltitle == "追加":
            self.TitleEntry = ttk.Entry(MainFrame, width=35)
            self.ParentsEntry = ttk.Combobox(MainFrame, width=32)
            self.ParentsEntry["values"] = Boxes
            self.ParentsEntry.grid(row = 2, column=1, pady = 5, padx = 5)
        elif labeltitle == "変更":
            self.ParentsEntry = ttk.Combobox(MainFrame, width=32)
            self.ParentsEntry["values"] = Boxes
            self.ParentsEntry.grid(row = 2, column=1, pady = 5, padx = 5)
            self.TitleEntry = ttk.Combobox(MainFrame, width=32)
            self.TitleEntry["values"] = Boxes
        else:
            self.ParentsEntry = ttk.Entry(MainFrame, width=35)
            self.ParentsEntry.grid(row = 2, column=1, pady = 5, padx = 5)
            self.TitleEntry = ttk.Combobox(MainFrame, width=32)
            self.TitleEntry["values"] = Boxes
        self.DetailsEntry = Text(MainFrame, width=30, height=10)
        self.RepetitionFrame = ttk.Frame(MainFrame)
        self.RepetitionValue = IntVar(value=0)
        
        self.NoRepetition = ttk.Radiobutton(self.RepetitionFrame, text="繰り返し無し", variable=self.RepetitionValue, value=0, command=lambda:[self.ChangeRepetitions("None")])
        self.Weekly = ttk.Radiobutton(self.RepetitionFrame, text="週単位繰り返し", variable=self.RepetitionValue, value=1, command=lambda:[self.ChangeRepetitions("Weekly")])
        self.Monthly = ttk.Radiobutton(self.RepetitionFrame, text="月単位繰り返し", variable=self.RepetitionValue, value=2, command=lambda:[self.ChangeRepetitions("Monthly")])
        self.NoRepetition.grid(row=0, column=0)
        self.Weekly.grid(row=1, column=0)
        self.Monthly.grid(row=2, column=0)
        self.WeekFrame = ttk.Labelframe(self.RepetitionFrame, text="曜日を選択")
        self.States = [BooleanVar(value=False),BooleanVar(value=False),BooleanVar(value=False),BooleanVar(value=False),BooleanVar(value=False),BooleanVar(value=False),BooleanVar(value=False),IntVar(value=0),BooleanVar(value=False),BooleanVar(value=False)]
        self.States1 = ttk.Checkbutton(self.WeekFrame, text="日(Sun)", variable=self.States[0])
        self.States2 = ttk.Checkbutton(self.WeekFrame, text="月(Mon)", variable=self.States[1])
        self.States3 = ttk.Checkbutton(self.WeekFrame, text="火(Tue)", variable=self.States[2])
        self.States4 = ttk.Checkbutton(self.WeekFrame, text="水(Wed)", variable=self.States[3])
        self.States5 = ttk.Checkbutton(self.WeekFrame, text="木(Thu)", variable=self.States[4])
        self.States6 = ttk.Checkbutton(self.WeekFrame, text="金(Fri)", variable=self.States[5])
        self.States7 = ttk.Checkbutton(self.WeekFrame, text="土(Sat)", variable=self.States[6])
        self.States1.pack()
        self.States2.pack()
        self.States3.pack()
        self.States4.pack()
        self.States5.pack()
        self.States6.pack()
        self.States7.pack()
        # self.WeekFrame.grid(row=0, column=1, rowspan=3)
        self.RepetitionPeriodFrame = ttk.Labelframe(self.RepetitionFrame, text="周期を選択")
        self.Period1 = ttk.Radiobutton(self.RepetitionPeriodFrame, text="0(毎週(月))", variable=self.States[7], value=0)
        self.Period2 = ttk.Radiobutton(self.RepetitionPeriodFrame, text="1(隔週(月))", variable=self.States[7], value=1)
        self.Period3 = ttk.Radiobutton(self.RepetitionPeriodFrame, text="2(隔2週)", variable=self.States[7], value=2)
        self.Period1.pack()
        self.Period2.pack()
        self.Period3.pack()
        self.MonthDayLabel = ttk.Labelframe(self.RepetitionFrame, text="日付を入力")
        self.MonthDay = ttk.Entry(self.MonthDayLabel, width=10)
        self.MonthDay.pack(padx=5, pady=5)
        # self.RepetitionPeriodFrame.grid(row=0, column=2, rowspan=3)
        self.LeedTime = ttk.Entry(MainFrame)
        self.Power = ttk.Checkbutton(MainFrame, variable=self.States[8])
        self.Person = ttk.Checkbutton(MainFrame, variable=self.States[9])
        self.TitleEntry.grid(row = 0, column=1, pady = 5, padx = 5)
        self.DetailsEntry.grid(row = 1, column=1, pady = 5, padx = 5)

        
        self.RepetitionFrame.grid(row = 0, column=3, pady = 5, padx = 5, rowspan=2)
        self.LeedTime.grid(row = 2, column=3, pady = 5, padx = 5)
        self.Power.grid(row = 3, column=1, pady = 5, padx = 5)
        self.Person.grid(row = 4, column=1, pady = 5, padx = 5)
        self.Maintenance(labeltitle, MainFrame)
        
    def main(self, labeltitle, MainFrame):
        self.RepetitionFrame.grid_forget()
        self.__init__(labeltitle, MainFrame)

    def Maintenance(self, labeltitle, MainFrame):
        if labeltitle == "追加":
            ConfirmButtonText = "内容の確認"
        else:
            ConfirmButtonText = "表示"

        ConfirmButton = ttk.Button(MainFrame, text=ConfirmButtonText, command=lambda:[self.DBEdit(labeltitle, MainFrame)])
        ConfirmButton.grid(row = 4, column = 3)
        if labeltitle != "追加":
            self.NoRepetition["state"] = "disable"
            self.Weekly["state"] = "disable"
            self.Monthly["state"] = "disable"
            self.ParentsEntry["state"] = "disable"
            self.Power["state"] = "disable"
            self.Person["state"] = "disable"
            self.LeedTime["state"] = "disable"


        

    def DBEdit(self, labeltitle, MainFrame):
        if labeltitle == "追加":
            a = self.DataGet()
            try:
                b = re.match(r'^Error.*', a)
            except:
                b = None
            if  b != None:
                
                messagebox.showerror("エラー" , a)
                root.lower()
            else:
                a[2] = a[2].replace("\n", "*kaigyo*")
                l1 = 0
                for i in range(7):
                    if a[5][i] == True:
                        l1 += 10**i
                a[5] = l1
                yesno = messagebox.askyesno("確認", "保存しますか？")
                root.lower()
                if yesno == True:
                    print("保存します")
                    c = self.WriteToDB("AllTasks", None, tuple(a))
                    try:
                        b = re.match(r'^Error.*', c)
                    except:
                        b = None
                    if b != None:
                        messagebox.showerror("エラー" , c)
                        root.lower()
                    else:
                        messagebox.showinfo("完了", c)
                        root.lower()
                        self.RepetitionFrame.grid_forget()
                        self.__init__("追加")
                    
                else:
                    print("保存しないです")
        elif labeltitle == "変更":
            ID = self.Titles[self.TitleEntry.get()]
            print(ID)
            Values = self.DataEntry(ID)
            print(Values)
            self.NoRepetition["state"] = "active"
            self.Weekly["state"] = "active"
            self.Monthly["state"] = "active"
            self.ParentsEntry["state"] = "active"
            self.Power["state"] = "active"
            self.Person["state"] = "active"
            self.LeedTime["state"] = "active"
            self.DetailsEntry.delete(1.0, "end")
            self.DetailsEntry.insert(1.0, Values[2])
            if Values[4] == 0:
                Method = "None"
            elif Values[4] == 1:
                Method = "Weekly"
            else:
                Method = "Monthly"
            self.RepetitionValue.set(Values[4])
            self.ChangeRepetitions(Method)
            self.ParentsEntry.insert(0, Values[3])
            self.LeedTime.insert(0, Values[7])
            # self.States["value"] = Values[8]
            self.States[9] = BooleanVar(value=Values[9])
            # コンボボックスの値を取得、タイトルの中のIDを見つける、IDを渡して入力する関数を実行する、実行出来たらフォーム解放。
            pass
        else:
            pass
        # メソッドの切り分け→追加だった場合、すべての値を取得、データの精査、書き込み
        # メソッドがそれ以外だった場合、とりあえずタイトルからIDを取得、ほかの情報をフォームに入力する。
        # 削除だった場合、すべてのフォームを無効にして削除するかどうかウインドウを出す。
    def DataEntry(self, ID):
        # IDを受け取り、そのほかの値を取得して表示する関数
        # try:
        con = sqlite3.connect("ICO_Setter.db")
        cur = con.cursor()
        sql = f"SELECT * FROM AllTasks WHERE ID = '{ID}'"
        cur.execute(sql)
        Raw = cur.fetchall()
        con.commit()
        con.close()
        Raw = list(Raw[0])
        print(Raw)
        Raw[2] = Raw[2].replace("*kaigyo*", "\n")
        if Raw[8] == 0:
            Raw[8] = False
        else:
            Raw[8] = True
        if Raw[9] == 0:
            Raw[9] = False
        else:
            Raw[9] = True
        return Raw
        # except:
        #     return

    def GetTitles(self):
        # タイトルを取得し、コンボボックスに入力する値を準備する関数 辞書型で返す。
        try:
            con = sqlite3.connect("ICO_Setter.db")
            cur = con.cursor()
            sql = "SELECT ID, Name FROM AllTasks"
            cur.execute(sql)
            Raw = cur.fetchall()
            con.commit()
            con.close()
            result = {}
            for i in range(len(Raw)):
                result[Raw[i][1]] = Raw[i][0]
            return result
        except:
            return

    def DataGet(self):
        time = str(datetime.datetime.now().year)+str(datetime.datetime.now().month)+str(datetime.datetime.now().day)+str(datetime.datetime.now().hour)+str(datetime.datetime.now().minute)+str(datetime.datetime.now().second)+str(datetime.datetime.now().microsecond)
        timehash = hash(time)
        Data = []
        Data.append(timehash)
        # タイトルが空白でないことを確認してデータ取得
        Raw = self.TitleEntry.get()
        if re.match(r'^\s*$', Raw) == None:
            # print(Raw)
            Data.append(Raw)
        else:
            # 空白だった場合、エラーを返す。
            return "Error:タイトルは入力必須です。"
        # 詳細と親タスクの情報を取得
        Details = self.DetailsEntry.get("1.0", "end"+"-1c")
        
        Data.append(Details)

        # print(self.ParentsEntry.get())
        Data.append(self.ParentsEntry.get())
        # print(self.RepetitionValue.get())
        Data.append(self.RepetitionValue.get())
        WeekofDay = []
        for i in range(len(self.States)):
            if i <= 6:
                WeekofDay.append(self.States[i].get())
            elif i == 7:
                if self.RepetitionValue.get() == 1 and (WeekofDay[0] == False and WeekofDay[1] == False and WeekofDay[2] == False and WeekofDay[3] == False and WeekofDay[4] == False and WeekofDay[5] == False and WeekofDay[6] == False):
                    print("ここ通ってます")
                    return "Error:曜日を選択してください"
                elif self.RepetitionValue.get() == 2 and re.match(r'^\s*$', self.MonthDay.get()) != None:
                    return "Error:日にちを入力してください"
                elif self.RepetitionValue.get() == 2:
                    Data.append(self.MonthDay.get())
                else:
                    Data.append(WeekofDay)
                Data.append(self.States[i].get())
                if re.match(r'^\s*$', self.LeedTime.get()) != None:
                    return "Error:所要時間を入力してください"
                Data.append(self.LeedTime.get())
            else:
                Data.append(self.States[i].get())
        return Data


    def ChangeRepetitions(self, RepetitionsName):
        try:
            self.RepetitionPeriodFrame.grid_forget()
        except:
            pass
        try:
            self.WeekFrame.grid_forget()
        except:
            pass
        try:
            self.MonthDayLabel.grid_forget()
        except:
            pass
        if RepetitionsName == "None":
            return
        elif RepetitionsName == "Weekly":
            self.WeekFrame.grid(row=0, column=1, rowspan=3)
            self.RepetitionPeriodFrame.grid(row=0, column=2, rowspan=3)
        else:
            self.RepetitionPeriodFrame.grid(row=0, column=1, rowspan=2)
            self.MonthDayLabel.grid(row=2, column=1, pady=5)
    def WriteToDB(self, DBName, WriteName, WriteLists):
        try:
            con = sqlite3.connect("ICO_Setter.db")
            cur = con.cursor()
            sql = f"INSERT INTO {DBName} values {WriteLists}"
            cur.execute(sql)
            con.commit()
            con.close()
            return "完了しました。"
        except:
            return "Error:何らかのエラーが発生しました。\nデータは保存されていません。"

        
if __name__ == "__main__":
    main()
