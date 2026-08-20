import tkinter as tk
from tkinter import colorchooser, messagebox
from PIL import Image, ImageDraw

class JankyPaint95:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("JankyPaint 95 - Lore Asset Creator")
        self.root.configure(bg="#c0c0c0") # Classic Windows 95 Gray
        
        # --- App State ---
        self.brush_color: str = "black"
        self.brush_size: int = 5
        self.is_drawing: bool = False
        self.last_x: int = 0
        self.last_y: int = 0
        
        # --- Layer System ---
        self.canvas_width: int = 400
        self.canvas_height: int = 400
        self.layers: list[Image.Image] = [] # Holds PIL Images for export
        self.active_layer_idx: int = 0
        
        self.setup_gui()
        self.add_layer() # Create Layer 1 by default

    def setup_gui(self):
        # 1. Toolbar (Left Side)
        toolbar = tk.Frame(self.root, bg="#c0c0c0", relief=tk.RAISED, bd=2)
        toolbar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        tk.Label(toolbar, text="TOOLS", bg="#c0c0c0", font=("Arial", 9, "bold")).pack(pady=5)
        
        tk.Button(toolbar, text="🖌️ Brush", command=self.use_brush, bg="#d4d0c8").pack(fill=tk.X, pady=2)
        tk.Button(toolbar, text="🧼 Eraser", command=self.use_eraser, bg="#d4d0c8").pack(fill=tk.X, pady=2)
        tk.Button(toolbar, text="🎨 Color", command=self.choose_color, bg="#d4d0c8").pack(fill=tk.X, pady=2)
        
        tk.Label(toolbar, text="Size:", bg="#c0c0c0").pack(pady=5)
        self.size_slider = tk.Scale(toolbar, from_=1, to=30, orient=tk.HORIZONTAL, bg="#c0c0c0")
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(fill=tk.X)
        
        tk.Button(toolbar, text="💾 Save PNG", command=self.save_png, bg="#d4d0c8", font=("Arial", 9, "bold")).pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # 2. Layer Panel (Right Side)
        layer_panel = tk.Frame(self.root, bg="#c0c0c0", relief=tk.SUNKEN, bd=2)
        layer_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        tk.Label(layer_panel, text="LAYERS", bg="#c0c0c0", font=("Arial", 9, "bold")).pack(pady=5)
        
        self.layer_listbox = tk.Listbox(layer_panel, height=10, bg="white", selectbackground="navy")
        self.layer_listbox.pack(padx=5, pady=5)
        self.layer_listbox.bind('<<ListboxSelect>>', self.select_layer)
        
        tk.Button(layer_panel, text="➕ Add Layer", command=self.add_layer, bg="#d4d0c8").pack(fill=tk.X, padx=5)

        # 3. Canvas (Center)
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white", cursor="crosshair", relief=tk.SUNKEN, bd=2)
        self.canvas.pack(padx=10, pady=10)
        
        # Bind Mouse Events
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

    # --- Tool Functions ---
    def use_brush(self):
        self.brush_color = "black"

    def use_eraser(self):
        self.brush_color = "white" # Acts as eraser on canvas

    def choose_color(self):
        color = colorchooser.askcolor(color=self.brush_color)[1]
        if color:
            self.brush_color = color

    # --- Layer Functions ---
    def add_layer(self):
        layer_name = f"Layer {len(self.layers) + 1}"
        # Create a transparent PIL image for this layer (explicit color tuple cast for Pylance)
        new_pil_layer = Image.new("RGBA", (self.canvas_width, self.canvas_height), (0, 0, 0, 0)) # type: ignore
        self.layers.append(new_pil_layer)
        
        self.layer_listbox.insert(tk.END, layer_name)
        self.layer_listbox.selection_clear(0, tk.END)
        self.layer_listbox.selection_set(tk.END)
        self.active_layer_idx = len(self.layers) - 1

    def select_layer(self, event):
        selection = self.layer_listbox.curselection()
        if selection:
            self.active_layer_idx = selection[0]

    # --- Drawing Functions ---
    def start_draw(self, event):
        self.is_drawing = True
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        if not self.is_drawing: 
            return
        
        current_x, current_y = event.x, event.y
        size = int(self.size_slider.get()) # Ensure integer width for Pillow/Tkinter
        
        # 1. Draw on Tkinter Canvas (Visual)
        tag = f"layer_{self.active_layer_idx}"
        self.canvas.create_line(self.last_x, self.last_y, current_x, current_y, 
                                fill=self.brush_color, width=size, 
                                capstyle=tk.ROUND, smooth=tk.TRUE, tags=tag)
        
        # 2. Draw on PIL Image (Background export layer)
        draw = ImageDraw.Draw(self.layers[self.active_layer_idx])
        rgba_color = (0, 0, 0, 0) if self.brush_color == "white" else self.hex_to_rgba(self.brush_color)
        draw.line([self.last_x, self.last_y, current_x, current_y], fill=rgba_color, width=size, joint="curve") # type: ignore
        
        self.last_x, self.last_y = current_x, current_y

    def stop_draw(self, event):
        self.is_drawing = False

    # --- Utility Functions ---
    def hex_to_rgba(self, hex_color: str) -> tuple[int, int, int, int]:
        if hex_color in ["black", "white"]:
            return (0, 0, 0, 255) if hex_color == "black" else (255, 255, 255, 255)
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) + (255,) # type: ignore

    def save_png(self):
        # Flatten all PIL layers into one image
        final_image = Image.new("RGBA", (self.canvas_width, self.canvas_height), (0, 0, 0, 0)) # type: ignore
        for layer in self.layers:
            final_image = Image.alpha_composite(final_image, layer)
        
        filename = "new_lore_entity.png"
        final_image.save(filename)
        messagebox.showinfo("Success", f"Saved successfully as {filename}! Ready for the simulator.")

if __name__ == "__main__":
    root = tk.Tk()
    app = JankyPaint95(root)
    root.mainloop()