import tkinter as tk

from src.presentation.app.jankyPaintApp import JankyPaintApp


def main():
    root = tk.Tk()
    root.geometry(
        "1200x800"
    )

    root.minsize(
        1000,
        700,
    )
    JankyPaintApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()