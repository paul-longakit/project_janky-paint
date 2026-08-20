import tkinter as tk

from presentation.editor.tkinter_app import JankyPaintApp


def main():
    root = tk.Tk()

    JankyPaintApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()