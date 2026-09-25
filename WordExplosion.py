import tkinter as tk
import random
import math


class TextExplosionApp:
    def __init__(self, root, canvas):
        self.root = root
        self.root.title("Tkinter Text Explosion")

        self.canvas = canvas
        # Configuration
        self.particles = []

    def trigger_explosion(self, text_id, moving_text):
        # Origin point of the explosion
        origin_x, origin_y = self.canvas.coords(text_id)

        # Colors for the particles
        colors = ["#FF3333", "#FF9933", "#FFFF33", "#33FF33", "#3399FF", "#FF33FF"]

        # Generate letter particles traveling outward
        for i, char in enumerate(moving_text):
            # Calculate an angle for each letter to disperse radially
            angle = (i / len(moving_text)) * 2 * math.pi + random.uniform(-0.5, 0.5)
            speed = random.uniform(4, 8)

            # Create a canvas text item for each single character
            char_id = self.canvas.create_text(
                origin_x + (i - len(moving_text) / 2) * 30,  # Offset initial X position slightly per letter
                origin_y,
                text=char,
                font=("Helvetica", 48, "bold"),
                fill=random.choice(colors)
            )

            # Store particle properties: ID, velocity X, velocity Y, and lifetime/alpha
            self.particles.append({
                "id": char_id,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "gravity": 0.2,  # Simulates falling downward after explosion
                "life": 40  # Frames until it fades out completely
            })

        # Start the animation loop
        self.update_particles()

    def update_particles(self):
        still_animating = False

        for p in self.particles[:]:
            if p["life"] > 0:
                # Apply velocities and gravity
                p["vy"] += p["gravity"]
                self.canvas.move(p["id"], p["vx"], p["vy"])

                # Decrement particle life
                p["life"] -= 1
                still_animating = True

                # Optional: Shrink text font size as it dies to simulate fading out
                current_font = ("Helvetica", max(int(p["life"] * 1.2), 8), "bold")
                self.canvas.itemconfig(p["id"], font=current_font)
            else:
                # Remove particle from canvas when dead
                self.canvas.delete(p["id"])
                self.particles.remove(p)

        # Schedule next frame if particles are still active
        if still_animating:
            self.root.after(20, self.update_particles)
