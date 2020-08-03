"""
Conversion functions for the NATO Phonetic Alphabet.
"""

# To save a lot of typing the code words are presented here
# as a dict, but feel free to change this if you'd like.
ALPHANUM_TO_NATO = {
    "A": "ALFA",
    "B": "BRAVO",
    "C": "CHARLIE",
    "D": "DELTA",
    "E": "ECHO",
    "F": "FOXTROT",
    "G": "GOLF",
    "H": "HOTEL",
    "I": "INDIA",
    "J": "JULIETT",
    "K": "KILO",
    "L": "LIMA",
    "M": "MIKE",
    "N": "NOVEMBER",
    "O": "OSCAR",
    "P": "PAPA",
    "Q": "QUEBEC",
    "R": "ROMEO",
    "S": "SIERRA",
    "T": "TANGO",
    "U": "UNIFORM",
    "V": "VICTOR",
    "W": "WHISKEY",
    "X": "XRAY",
    "Y": "YANKEE",
    "Z": "ZULU",
    "0": "ZERO",
    "1": "ONE",
    "2": "TWO",
    "3": "TREE",
    "4": "FOUR",
    "5": "FIVE",
    "6": "SIX",
    "7": "SEVEN",
    "8": "EIGHT",
    "9": "NINER",
}


def transmit(message: str) -> str:
    """
    Convert a message to a NATO code word transmission.
    """
    # <- implement your function
    message = [char for char in message]
    ans = ""
    for i in message:
        in_ans = ALPHANUM_TO_NATO.get(i.upper(), None)
        if in_ans:
            ans += in_ans
            ans += " "
    return ans[:-1]


def receive(transmission: str) -> str:
    """
    Convert a NATO code word transmission to a message.
    """
    # <- implement your function
    NEW_ALPHANUM_TO_NATO = dict(zip(ALPHANUM_TO_NATO.values(), ALPHANUM_TO_NATO.keys()))
    transmission = transmission.split(" ")
    ans = ""
    for i in transmission:
        ans += NEW_ALPHANUM_TO_NATO.get(i, "")
    return ans


from logging import exception
from tkinter import *
from tkinter import messagebox
import sqlite3


class user_create:
    def __init__(self, root):
        self.root = root
        self.root.title("Create User")
        self.root.geometry("720x340+300+180")
        self.root.maxsize(720, 340)
        self.root.config(bg="#021e2f")
        # self.root.iconbitmap("npcilogo.ico")
        # Frame
        frame1 = Frame(self.root, bg="white")
        frame1.place(x=10, y=10, width=700, height=320)
        title = Label(
            frame1,
            text="Create User",
            font=("Times New Roman", 20, "bold"),
            bg="white",
            fg="red",
        ).place(x=290, y=5)

        # login
        self.name, self.username, self.password, self.mobile = (
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar(),
        )
        fname1 = Label(
            frame1,
            text="Full Name",
            font=("Times New Roman", 16, "bold"),
            bg="white",
            fg="Black",
        ).place(x=20, y=60)
        self.txt_fname1 = Entry(
            frame1, textvariable=self.name, font=("Times New Roman", 15), bg="lightgray"
        ).place(x=180, y=63, width=480, height=30)
        fmobile = Label(
            frame1,
            text="User Name",
            font=("Times New Roman", 16, "bold"),
            bg="white",
            fg="Black",
        ).place(x=20, y=110)
        self.txt_fmobile = Entry(
            frame1,
            textvariable=self.mobile,
            font=("Times New Roman", 15),
            bg="lightgray",
        ).place(x=180, y=213, width=480, height=30)
        fusername = Label(
            frame1,
            text="Password",
            font=("Times New Roman", 16, "bold"),
            bg="white",
            fg="Black",
        ).place(x=20, y=160)
        self.txt_fusername = Entry(
            frame1,
            textvariable=self.username,
            font=("Times New Roman", 15),
            bg="lightgray",
        ).place(x=180, y=113, width=480, height=30)
        fpass = Label(
            frame1,
            text="Mobile No.",
            font=("Times New Roman", 16, "bold"),
            bg="white",
            fg="Black",
        ).place(x=20, y=210)
        self.txt_fpass = Entry(
            frame1,
            textvariable=self.password,
            font=("Times New Roman", 15),
            bg="lightgray",
        ).place(x=180, y=163, width=480, height=30)
        btn_save = Button(
            frame1,
            text="      Save      ",
            command=self.reg_save,
            font=("Times New Roman", 15),
            bg="white",
            fg="red",
            bd=1,
            cursor="hand2",
        ).place(x=150, y=260)
        btn_reset = Button(
            frame1,
            text="      Reset      ",
            font=("Times New Roman", 15),
            bg="white",
            fg="red",
            bd=1,
            cursor="hand2",
        ).place(x=300, y=260)
        btn_close = Button(
            frame1,
            text="      Return      ",
            command=self.return_home,
            font=("Times New Roman", 15),
            bg="white",
            fg="red",
            bd=1,
            cursor="hand2",
        ).place(x=450, y=260)

    def return_home(self):
        self.root.destroy()
        import Home

    def reg_save(self):
        if (
            self.name.get() == ""
            or self.username.get() == ""
            or self.password.get() == ""
            or self.mobile.get() == ""
        ):
            messagebox.showerror("Error", "All Fields Required", parent=self.root)
        else:
            try:
                print(self.name.get(), self.username.get(),
                      self.password.get(),
                      self.mobile.get(),)
                conn = sqlite3.connect("npcidbms")
                crr = conn.cursor()
                crr.execute(
                    "CREATE TABLE IF NOT EXISTS login ( fname text NOT NULL,uname TEXT,pass TEXT,mobile TEXT) "
                )
                crr.execute(
                    "insert into login(fname,uname,pass,mobile) values(?,?,?,?)",
                    (
                        self.name.get(),
                        self.username.get(),
                        self.password.get(),
                        self.mobile.get(),
                    ),
                )
                crr.close()
                messagebox.showerror(
                    "Error", "Registration Sucessful", parent=self.root
                )
            except Exception as es:
                messagebox.showerror(
                    "Error", f"Error Due to:{str(es)}", parent=self.root
                )


root = Tk()
obj = user_create(root)
root.mainloop()
