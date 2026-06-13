import sys
import tkinter as tk
import os

class ControlPanel:
    def __init__(self, window, timer_app):
        self.window = window
        self.timer_app = timer_app
        self.window.title("42 Timer - Controls")
        self.window.geometry("260x280+320+60") 
        self.window.resizable(False, False)
        
        self.bg_color = "#1E1E24"
        self.btn_bg = "#2E2E38"
        self.input_bg = "#3E3E4A"
        self.accent = "#00BABC"
        self.window.configure(bg=self.bg_color)
        
        self.window.protocol("WM_DELETE_WINDOW", self.timer_app.toggle_controls)
        
        tk.Label(window, text="TIMER CONTROLS", font=("Helvetica", 10, "bold"), bg=self.bg_color, fg=self.accent).pack(pady=(10, 5))
        
        self.pause_btn = tk.Button(window, text="Pause", font=("Helvetica", 10, "bold"), bg=self.btn_bg, fg="white", bd=0, width=20, pady=4, command=self.toggle_pause)
        self.pause_btn.pack(pady=3)
        
        self.skip_btn = tk.Button(window, text="Trigger Lock Countdown", font=("Helvetica", 9), bg="#EA4335", fg="white", bd=0, width=20, pady=2, command=self.timer_app.trigger_grace_period)
        self.skip_btn.pack(pady=3)
        
        tk.Label(window, text="QUICK PRESETS", font=("Helvetica", 10, "bold"), bg=self.bg_color, fg=self.accent).pack(pady=(15, 5))
        self.scale_frame = tk.Frame(window, bg=self.bg_color)
        self.scale_frame.pack()
        
        for mins in [15, 30, 45, 60]:
            btn = tk.Button(self.scale_frame, text=f"{mins}m", font=("Helvetica", 9), bg=self.btn_bg, fg="white", bd=0, padx=6, command=lambda m=mins: self.timer_app.set_scale(m))
            btn.pack(side="left", padx=3)

        tk.Label(window, text="CUSTOM PARAMETERS", font=("Helvetica", 10, "bold"), bg=self.bg_color, fg=self.accent).pack(pady=(15, 5))
        self.input_frame = tk.Frame(window, bg=self.bg_color)
        self.input_frame.pack(padx=10)
        
        tk.Label(self.input_frame, text="Mins:", font=("Helvetica", 9), bg=self.bg_color, fg="white").grid(row=0, column=0, sticky="w", pady=2)
        self.time_entry = tk.Entry(self.input_frame, width=12, bg=self.input_bg, fg="white", bd=0, insertbackground="white")
        self.time_entry.insert(0, "30")
        self.time_entry.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(self.input_frame, text="Cmd:", font=("Helvetica", 9), bg=self.bg_color, fg="white").grid(row=1, column=0, sticky="w", pady=2)
        self.cmd_entry = tk.Entry(self.input_frame, width=12, bg=self.input_bg, fg="white", bd=0, insertbackground="white")
        self.cmd_entry.insert(0, "ft_lock")
        self.cmd_entry.grid(row=1, column=1, padx=5, pady=2)
        
        self.apply_btn = tk.Button(window, text="Apply Custom Settings", font=("Helvetica", 9, "bold"), bg=self.accent, fg="black", bd=0, width=20, pady=4, command=self.apply_custom)
        self.apply_btn.pack(pady=12)

    def toggle_pause(self):
        self.timer_app.is_paused = not self.timer_app.is_paused
        self.pause_btn.config(text="Resume" if self.timer_app.is_paused else "Pause", 
                              fg=self.accent if self.timer_app.is_paused else "white")

    def apply_custom(self):
        self.timer_app.lock_command = self.cmd_entry.get().strip()
        try:
            mins = int(self.time_entry.get().strip())
            if mins > 0:
                self.timer_app.set_scale(mins)
        except ValueError:
            pass


class FloatingTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("42 - 30:00")
        self.root.attributes("-topmost", True)
        self.root.geometry("240x110+60+60") 
        self.root.resizable(False, False)
        
        self.bg_color = "#1E1E24"
        self.text_color = "#00BABC"
        self.warn_color = "#EA4335"
        self.btn_bg = "#2E2E38"
        self.root.configure(bg=self.bg_color)
        
        self.work_time = 30 * 60
        self.grace_time = 5 * 60
        self.is_grace_period = False
        self.is_paused = False
        self.lock_command = "ft_lock"
        
        self.controls_visible = False
        self.controls_window = None
        self.control_app = None
        
        self.status_label = tk.Label(root, text="FOCUSING SESSION", font=("Helvetica", 8, "bold"), bg=self.bg_color, fg="white")
        self.status_label.pack(pady=(8, 2))
        
        self.display_label = tk.Label(root, text="30:00", font=("Helvetica", 22, "bold"), bg=self.bg_color, fg=self.text_color)
        self.display_label.pack()

        self.config_btn = tk.Button(root, text="⚙ Config", font=("Helvetica", 8, "bold"), bg=self.btn_bg, fg="white", bd=0, padx=10, command=self.toggle_controls)
        self.config_btn.pack(pady=(4, 0))
        
        self.root.protocol("WM_DELETE_WINDOW", self.quit_program)
        
        self.tick()

    def toggle_controls(self):
        if not self.controls_visible:
            self.controls_window = tk.Toplevel(self.root)
            self.control_app = ControlPanel(self.controls_window, self)
            
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            self.controls_window.geometry(f"260x280+{x + 250}+{y}")
            
            self.config_btn.config(bg=self.text_color, fg="black")
            self.controls_visible = True
        else:
            if self.controls_window:
                self.controls_window.destroy()
            self.config_btn.config(bg=self.btn_bg, fg="white")
            self.controls_visible = False

    def set_scale(self, minutes):
        self.is_grace_period = False
        self.work_time = minutes * 60
        self.grace_time = 5 * 60
        self.status_label.config(text="FOCUSING SESSION", fg="white")
        self.display_label.config(fg=self.text_color)
        self.update_display_text(self.work_time)

    def trigger_grace_period(self):
        self.work_time = 0
        if not self.is_grace_period:
            self.is_grace_period = True
            self.status_label.config(text="⚠️ LOCK WARNING ACTIVE", fg=self.warn_color)
            self.display_label.config(fg=self.warn_color)
            self.root.lift()

    def lock_cluster_pc(self):
        print(f"🔒 Triggering lock behavior string command: {self.lock_command}")
        if os.system(self.lock_command) != 0:
            os.system(f"zsh -i -c '{self.lock_command}'")
        sys.exit(0)

    def update_display_text(self, seconds_left):
        mins, secs = divmod(seconds_left, 60)
        time_str = f"{mins:02d}:{secs:02d}"
        self.display_label.config(text=time_str)
        self.root.title(f"42 - {time_str}")

    def tick(self):
        if not self.is_paused:
            if not self.is_grace_period:
                if self.work_time > 0:
                    self.update_display_text(self.work_time)
                    self.work_time -= 1
                else:
                    self.trigger_grace_period()
            else:
                if self.grace_time > 0:
                    self.update_display_text(self.grace_time)
                    self.grace_time -= 1
                else:
                    self.lock_cluster_pc()
        
        self.root.after(1000, self.tick)

    def quit_program(self):
        self.root.destroy()
        sys.exit(0)


if __name__ == "__main__":
    root_timer = tk.Tk()
    timer_app = FloatingTimer(root_timer)
    root_timer.mainloop()