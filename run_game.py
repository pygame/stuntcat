try:
    import Tkinter as tk
    import tkinterMsgbox as tk_msg
except ImportError:
    import tkinter as tk
    import tkinter.messagebox as tk_msg
from stuntcat import Game


def main():
    try:
        Game().mainloop()
    except Exception:
        import traceback
        tk.Tk().withdraw()
        tk_msg.showerror('Error', traceback.format_exc())


if __name__ == '__main__':
    main()

