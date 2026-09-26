import random
import tkinter as tk
import time
import WordExplosion
from wonderwords import RandomWord

WAIT_PERIOD = 50
MOVE_PIXELS = 3

def handle_any_key(event):
    global y, success, y_at_success
    current_string = event.widget.get()+event.char
    if moving_text == current_string:
        success=True
        y_at_success = y
        y = screen_height

# Initialize the generator
rw = RandomWord()

# Set up the main window
root = tk.Tk()
root.title("Falling Word")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("400x500")

# Create a canvas to draw on
canvas = tk.Canvas(root, width=screen_width-10, height=screen_height-10, bg="black")
canvas.pack(fill="both", expand=True)

app = WordExplosion.TextExplosionApp(root, canvas)

entry = tk.Entry(root, width=30, background="white")
entry.pack(pady=10)
entry.bind("<Key>", handle_any_key)
canvas_entry_id = canvas.create_window(600, 600, window=entry)

success = False
x = 100
y = 0
new_score = 0
total_score = 0
best_score = 0
moving_text = rw.word()
text_id = canvas.create_text(x, y, text=moving_text, fill="white", font=("Arial", 14))
score_id = canvas.create_text(screen_width - 40, screen_height-40, text=str(total_score),
                              fill="white", font=("Arial", 16))
# Starting vertical position
y_pos = 20

def fall():
    global y, success, y_at_success
    global text_id
    global moving_text

    canvas.move(text_id, 0, MOVE_PIXELS)  # Move 3 pixels down
    y += MOVE_PIXELS

    if y < screen_height-70:
        root.after(WAIT_PERIOD, fall)  # Repeat every WAIT milliseconds
    else:
        if success :
            global new_score, total_score, best_score
            canvas.configure(background="green")
            speed_score = ((screen_height + 40 - y_at_success)/screen_height)*100
            difficulty_score = (len(moving_text)/12)*100
            new_score = int((speed_score*0.8) + (difficulty_score*0.2))
            total_score+=new_score
            success = False
            WordExplosion.TextExplosionApp.trigger_explosion(app, text_id, moving_text)
        else:
            canvas.configure(background="red")
            canvas.update()
            time.sleep(2)
        best_score += 100
        canvas.itemconfig(score_id, text=str(total_score) + "/" + str(best_score))
        canvas.coords(score_id, screen_width - 100, screen_height - 100)
        canvas.update()
        canvas.delete(text_id)
        entry.delete(0, tk.END)
        canvas.configure(background="black")
        moving_text = rw.word()
        text_id = canvas.create_text(x, y, text=moving_text, fill="white", font=("Arial", 14))
        # Reset to top at a new X position when it hits the bottom
        canvas.coords(text_id, random.randint(50, screen_width-50), 0)
        y = 0
        root.after(WAIT_PERIOD, fall)

# Start the animation loop
fall()
root.mainloop()