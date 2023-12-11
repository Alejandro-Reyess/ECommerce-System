import tkinter as tk
from view.system_view import AuthenticationView


def main():
    root = tk.Tk()
    AuthenticationView(root)
    root.mainloop()


if __name__ == "__main__":
    main()
