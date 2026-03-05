import tkinter as tk
from tkinter import messagebox
import requests
import random

def ip_lookup():
    ip_address = entry_ip.get().strip()
    
    # Update button state and clear previous results
    btn_lookup.config(text="Looking up...", state=tk.DISABLED)
    root.update()
    
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    
    try:
        # If ip_address is empty, ip-api will pull the current machine's IP
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "fail":
            messagebox.showerror("Error", "Invalid IP.")
        else:
            details = [
                f"IP:        {data.get('query', 'N/A')}",
                f"Country:   {data.get('country', 'N/A')}",
                f"Region:    {data.get('regionName', 'N/A')}",
                f"City:      {data.get('city', 'N/A')}",
                f"ISP:       {data.get('isp', 'N/A')}",
                f"Timezone:  {data.get('timezone', 'N/A')}",
                f"Latitude:  {data.get('lat', 'N/A')}",
                f"Longitude: {data.get('lon', 'N/A')}",
            ]
            
            result_text.insert(tk.END, "\n".join(details))
            
    except requests.exceptions.Timeout:
        messagebox.showerror("Timeout", "The request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Connection Error", f"Network error occurred:\n{e}")
    finally:
        result_text.config(state=tk.DISABLED)
        btn_lookup.config(text="Lookup", state=tk.NORMAL)

# --- GUI Setup ---
root = tk.Tk()
root.title("NidoIPLookup")
root.geometry("450x380")
root.configure(bg="#050505")
root.resizable(False, False)

# Canvas for particles
canvas = tk.Canvas(root, bg="#050505", highlightthickness=0)
canvas.place(x=0, y=0, width=450, height=380)

# Background Particles
class Particle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = random.randint(0, 450)
        self.y = random.randint(0, 380)
        # Smooth, slow random velocities
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.radius = random.uniform(1.0, 2.5)
        color = random.choice(["#ff6600", "#ffaa00", "#cc5200"])
        self.id = canvas.create_oval(
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius,
            fill=color, outline="")

    def move(self):
        self.x += self.vx
        self.y += self.vy
        
        # Smoothly bounce off walls
        if self.x < 0 or self.x > 450: 
            self.vx *= -1
            self.x += self.vx * 2 # prevent sticking
        if self.y < 0 or self.y > 380: 
            self.vy *= -1
            self.y += self.vy * 2 # prevent sticking
            
        self.canvas.coords(self.id, 
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius)

# Create fewer particles for a cleaner look
particles = [Particle(canvas) for _ in range(50)]

def update_particles():
    for p in particles:
        p.move()
    root.after(30, update_particles)

update_particles()

# Title Label
title_label = tk.Label(root, text="NidoIPLookup", font=("Segoe UI", 16, "bold"), bg="#050505", fg="#ff6600")
title_label.place(relx=0.5, y=30, anchor=tk.CENTER)

# Instruction Label
label_ip = tk.Label(root, text="Enter IP Address (leave blank for your IP):", font=("Segoe UI", 10), bg="#050505", fg="#e0e0e0")
label_ip.place(x=40, y=65)

# Entry Field
entry_ip = tk.Entry(root, font=("Consolas", 12), width=35, bg="#2b2b2b", fg="#ffaa00", insertbackground="#ffaa00", relief=tk.FLAT)
entry_ip.place(relx=0.5, y=105, anchor=tk.CENTER, width=370, height=30)

# Lookup Button
btn_lookup = tk.Button(root, text="Lookup", command=ip_lookup, font=("Segoe UI", 10, "bold"), 
                       bg="#ff6600", fg="#050505", activebackground="#cc5200", activeforeground="#050505", 
                       relief=tk.FLAT, cursor="hand2")
btn_lookup.place(relx=0.5, y=155, anchor=tk.CENTER, width=120, height=35)

# Results Text Box
result_text = tk.Text(root, font=("Consolas", 11), state=tk.DISABLED, 
                      bg="#1e1e1e", fg="#ffaa00", relief=tk.FLAT, padx=10, pady=10)
result_text.place(relx=0.5, y=265, anchor=tk.CENTER, width=370, height=160)

# Bind Enter key to trigger lookup
root.bind('<Return>', lambda event: ip_lookup())

# Run the app
root.mainloop()
