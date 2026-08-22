import tkinter as tk

from src.presentation.app.jankyPaintApp import JankyPaintApp


def main():
    root = tk.Tk()

    JankyPaintApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()