import tkinter as tk
from tkinter import ttk
import time
import threading

color = input("Enter circle color: ")
bgcolor = input("Enter background color: ")

window = tk.Tk()
window.title("Move")
window.geometry("800x500")

loading_screen = None


def move_circle(event=None):
    key = event.keysym if event else None

    x1, y1, x2, y2 = canvas.bbox(circle)
    circle_center_x = (x1 + x2) / 2
    circle_center_y = (y1 + y2) / 2
    circle_radius = (x2 - x1) / 2

    move_speed = movespeeds[speed_var.get()]
    if key == "Left" and circle_center_x - circle_radius >= 0:
        canvas.move(circle, -move_speed, 0)
    elif key == "Right" and circle_center_x + circle_radius <= canvas.winfo_width():
        canvas.move(circle, move_speed, 0)
    elif key == "Up" and circle_center_y - circle_radius >= 0:
        canvas.move(circle, 0, -move_speed)
    elif key == "Down" and circle_center_y + circle_radius <= canvas.winfo_height():
        canvas.move(circle, 0, move_speed)
    elif key == "Home" and circle_center_x - circle_radius >= 0 and circle_center_y - circle_radius >= 0:
        canvas.move(circle, -move_speed, -move_speed)
    elif key == "Prior" and circle_center_x + circle_radius <= canvas.winfo_width() and circle_center_y - circle_radius >= 0:
        canvas.move(circle, move_speed, -move_speed)
    elif key == "Next" and circle_center_x + circle_radius <= canvas.winfo_width() and circle_center_y + circle_radius <= canvas.winfo_height():
        canvas.move(circle, move_speed, move_speed)
    elif key == "End" and circle_center_x - circle_radius >= 0 and circle_center_y + circle_radius <= canvas.winfo_height():
        canvas.move(circle, -move_speed, move_speed)
    elif key == "Escape":
        window.quit()


def set_canvas_size(size):
    global loading_screen

    if loading_screen and loading_screen.winfo_exists():
        loading_screen.destroy()

    loading_screen = tk.Toplevel(window)
    loading_screen.title("Loading...")
    loading_screen.geometry("300x100")
    loading_label = tk.Label(loading_screen, text="Loading...")
    loading_label.pack()

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(loading_screen, variable=progress_var, maximum=100, mode='determinate')
    progress_bar.pack()

    def load_canvas_size():
        canvas_width, canvas_height = canvas_sizes[size]
        window.geometry(f"{canvas_width}x{canvas_height}")
        canvas.config(width=canvas_width, height=canvas_height)

        loading_screen.destroy()

    def update_progress():
        for i in range(101):
            progress_var.set(i)
            window.update_idletasks()
            time.sleep(0.02)

        load_canvas_size()

    threading.Thread(target=update_progress).start()


canvas = tk.Canvas(window, width=800, height=500, bg=bgcolor)

circle_center_x = 400
circle_center_y = 125
circle_radius = 50
circle = canvas.create_oval(
    circle_center_x - circle_radius,
    circle_center_y - circle_radius,
    circle_center_x + circle_radius,
    circle_center_y + circle_radius,
    fill=color)

canvas.pack()

speeds = {"slow": 15, "normal": 30, "fast": 50}
movespeeds = speeds.copy()
speed_var = tk.StringVar(value="normal")

speed_menu = tk.OptionMenu(window, speed_var, *speeds.keys(), command=lambda _: show_loading("speed"))
speed_menu.pack()

canvas_sizes = {
    "small": (800, 500),
    "normal": (1200, 600),
    "big": (1600, 800),
}
canvas_var = tk.StringVar(value="normal")

canvas_menu = tk.OptionMenu(window, canvas_var, *canvas_sizes.keys(), command=lambda size: show_loading("size"))
canvas_menu.pack()


def show_loading(event_type):
    global loading_screen

    if loading_screen and loading_screen.winfo_exists():
        loading_screen.destroy()

    loading_screen = tk.Toplevel(window)
    loading_screen.title("Loading...")
    loading_screen.geometry("450x200")
    loading_label = tk.Label(loading_screen, text="Loading...")
    loading_label.pack()

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(loading_screen, variable=progress_var, maximum=50, mode='determinate')
    progress_bar.pack()



    def update_progress():
        for i in range(51):
            progress_var.set(i)
            window.update_idletasks()
            time.sleep(0.02)

        if event_type == "size":
            set_canvas_size(canvas_var.get())
        elif event_type == "speed":
            move_circle()

        loading_screen.destroy()

    threading.Thread(target=update_progress).start()


window.bind("<Left>", move_circle)
window.bind("<Right>", move_circle)
window.bind("<Up>", move_circle)
window.bind("<Down>", move_circle)
window.bind("<Home>", move_circle)
window.bind("<Prior>", move_circle)
window.bind("<Next>", move_circle)
window.bind("<End>", move_circle)
window.bind("<Escape>", move_circle)

window.mainloop()