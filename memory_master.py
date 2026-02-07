import json
import random
import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk, simpledialog, messagebox

from PIL import Image, ImageTk

# נתיבים
DATA_FILE = Path.cwd() / "memory_master_data.json"
SHAPES_FOLDER = Path.cwd() / "training_shapes"
IMAGE_FOLDER = Path.cwd() / "training_images"
WORDS_FILE = Path.cwd() / "my_dictionary.txt"


class MemoryMasterUltimate:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Master Pro - Full Feedback Edition")
        self.root.geometry("1100x950")

        self.current_user = None
        self.target_set = []
        self.user_choices = []

        self.load_all_data()
        self.show_login_screen()

        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def load_all_data(self):
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.all_data = json.load(f)
            except:
                self.all_data = {"רמי": {"levels": {"צורות": 1, "תמונות": 1, "מילים": 1, "מספרים": 1}}}
        else:
            users = ["רמי", "אתי", "ליאור"]
            self.all_data = {u: {"levels": {"צורות": 1, "תמונות": 1, "מילים": 1, "מספרים": 1}} for u in users}
            self.save_data()

    def add_new_user(self):
        new_name = simpledialog.askstring("משתמש חדש", "הקלד שם משתמש:")
        if new_name:
            if new_name in self.all_data:
                messagebox.showwarning("שגיאה", "משתמש זה כבר קיים!")
            else:
                # יצירת פרופיל חדש עם רמות התחלתיות
                self.all_data[new_name] = {"levels": {"צורות": 1, "תמונות": 1, "מילים": 1, "מספרים": 1}}
                self.save_data()
                self.show_login_screen()  # רענון המסך כדי שהשם יופיע ברשימה

    def show_login_screen(self):
        for w in self.root.winfo_children(): w.destroy()
        self.current_user = None
        frame = tk.Frame(self.root)
        frame.pack(expand=True)
        tk.Label(frame, text="Memory Master Pro", font=("Arial", 32, "bold")).pack(pady=30)

        self.user_var = tk.StringVar()
        user_list = list(self.all_data.keys())
        combo = ttk.Combobox(frame, textvariable=self.user_var, values=user_list, state="readonly", font=("Arial", 16))
        combo.pack(pady=10, ipady=5)
        if user_list: combo.current(0)

        # כפתור כניסה
        tk.Button(frame, text="כניסה", command=self.login, bg="#27ae60", fg="white", font=("Arial", 16, "bold"),
                  width=15).pack(pady=10)

        # כפתור הוספת משתמש חדש (החזרתי אותו!)
        tk.Button(frame, text="➕ משתמש חדש", command=self.add_new_user, bg="#3498db", fg="white",
                  font=("Arial", 12)).pack(pady=5)

        tk.Button(frame, text="צפה בהישגים", command=self.show_achievements, bg="#9b59b6", fg="white").pack(pady=10)

    def login(self):
        if self.user_var.get():
            self.current_user = self.user_var.get()
            self.setup_main_layout()

    def setup_main_layout(self):
        for w in self.root.winfo_children(): w.destroy()

        # 1. סרגל עליון
        self.top_bar = tk.Frame(self.root, bg="#ecf0f1", pady=10)
        self.top_bar.pack(fill="x", side="top")
        tk.Label(self.top_bar, text=f"משתמש: {self.current_user}", font=("Arial", 12, "bold"), bg="#ecf0f1").pack(
            side="right", padx=20)
        self.mode_var = tk.StringVar(value="צורות")
        for m in ["צורות", "תמונות", "מספרים", "מילים"]:
            tk.Radiobutton(self.top_bar, text=m, variable=self.mode_var, value=m, bg="#ecf0f1",
                           command=self.update_lvl_display).pack(side="left", padx=15)

        # 2. סרגל תחתון קבוע
        self.footer = tk.Frame(self.root, bg="#34495e", pady=10)
        self.footer.pack(fill="x", side="bottom")
        tk.Button(self.footer, text="יציאה ושמירה", command=self.exit_app, bg="#e74c3c", fg="white",
                  font=("Arial", 10, "bold"), width=12).pack(side="left", padx=20)
        tk.Button(self.footer, text="לוח הישגים", command=self.show_achievements, bg="#9b59b6", fg="white",
                  font=("Arial", 10), width=12).pack(side="left", padx=10)
        tk.Button(self.footer, text="החלף משתמש", command=self.show_login_screen, bg="#95a5a6", fg="white",
                  font=("Arial", 10), width=12).pack(side="right", padx=20)
        tk.Button(self.footer, text="גרף התקדמות", command=self.show_progress_graph, bg="#2980b9", fg="white",
                  font=("Arial", 10)).pack(side="left", padx=10)

        # 3. אזור תצוגה
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)
        self.lvl_lbl = tk.Label(self.main_container, text="", font=("Arial", 14, "bold"), pady=10);
        self.lvl_lbl.pack()
        self.display_area = tk.Frame(self.main_container, bg="white", height=400, relief="sunken", bd=2)
        self.display_area.pack(pady=10, padx=40, fill="both", expand=True)
        self.display_area.pack_propagate(False)

        # 4. כפתור התחלה ומשוב מפורט
        self.action_frame = tk.Frame(self.main_container, pady=10);
        self.action_frame.pack(fill="x")
        tk.Button(self.action_frame, text="התחל תרגיל", command=self.run_exercise, bg="#3498db", fg="white",
                  font=("Arial", 16, "bold"), width=15).pack(pady=5)

        # לייבלים לדיווח תוצאות (החלק שחזר)
        self.score_lbl = tk.Label(self.main_container, text="", font=("Arial", 22, "bold"), fg="blue");
        self.score_lbl.pack()
        self.pass_lbl = tk.Label(self.main_container, text="", font=("Arial", 12), fg="green");
        self.pass_lbl.pack()
        self.fail_lbl = tk.Label(self.main_container, text="", font=("Arial", 12), fg="red");
        self.fail_lbl.pack()

        self.update_lvl_display()

    def update_lvl_display(self):
        m = self.mode_var.get();
        l = self.all_data[self.current_user]["levels"].get(m, 1)
        self.lvl_lbl.config(text=f"אימון {m} | רמה: {l}")

    def run_exercise(self):
        for w in self.display_area.winfo_children(): w.destroy()
        self.score_lbl.config(text="");
        self.pass_lbl.config(text="");
        self.fail_lbl.config(text="")

        mode = self.mode_var.get();
        lvl = int(self.all_data[self.current_user]["levels"].get(mode, 1))

        if mode in ["צורות", "תמונות"]:
            folder = SHAPES_FOLDER if mode == "צורות" else IMAGE_FOLDER
            all_files = list(folder.glob("*.png")) + list(folder.glob("*.jpg"))
            if not all_files: return
            picked = random.sample(all_files, min(lvl, len(all_files)))
            inner_f = tk.Frame(self.display_area, bg="white");
            inner_f.pack(expand=True)
            for p in picked:
                img = ImageTk.PhotoImage(Image.open(p).resize((150, 150)))
                lbl = tk.Label(inner_f, image=img, bg="white", highlightthickness=2, highlightbackground="#bdc3c7")
                lbl.image = img;
                lbl.pack(side="right", padx=10)
            self.target_set = [p.name for p in picked]
            self.root.after(max(2000, len(self.target_set) * 1500), self.ask_selection_grid)
        elif mode == "מילים":
            # לוגיקת מילים (עובדת)
            pool = ["כיסא", "שולחן", "מים"]
            if WORDS_FILE.exists():
                with open(WORDS_FILE, "r", encoding="utf-8") as f: pool = [line.strip() for line in f if line.strip()]
            self.target_set = random.sample(pool, min(lvl, len(pool)))
            tk.Label(self.display_area, text=" | ".join(self.target_set), font=("Arial", 35), bg="white").pack(
                expand=True)
            self.root.after(max(2000, len(self.target_set) * 1500), self.ask_recall_text)
        elif mode == "מספרים":
            # לוגיקת מספרים (עובדת)
            self.target_set = [str(random.randint(10, 99)) for _ in range(lvl)]
            tk.Label(self.display_area, text=" - ".join(self.target_set), font=("Arial", 45, "bold"), bg="white").pack(
                expand=True)
            self.root.after(max(2000, len(self.target_set) * 1500), self.ask_recall_text)

    def ask_recall_text(self):
        for w in self.display_area.winfo_children(): w.destroy()
        ans = simpledialog.askstring("תשובה", "הקלד מה שראית (פסיק מפריד):")
        self.user_choices = [a.strip() for a in ans.split(",")] if ans else []
        self.finish()

    def ask_selection_grid(self):
        for w in self.display_area.winfo_children(): w.destroy()
        mode = self.mode_var.get();
        folder = SHAPES_FOLDER if mode == "צורות" else IMAGE_FOLDER
        all_imgs = list(folder.glob("*.png")) + list(folder.glob("*.jpg"))
        grid_items = [folder / n for n in self.target_set] + random.sample(
            [f for f in all_imgs if f.name not in self.target_set], min(len(all_imgs) - len(self.target_set), 8))
        random.shuffle(grid_items)
        container = tk.Frame(self.display_area, bg="white");
        container.pack(expand=True)
        self.user_choices = []
        for i, p in enumerate(grid_items):
            img = ImageTk.PhotoImage(Image.open(p).resize((110, 110)))
            btn = tk.Button(
                container,
                image=img,
                bg="white",
                activebackground="#d6eaf8",
                relief="flat",
                bd=0
            )
            btn.config(command=lambda path=p, b=btn: self.toggle(path.name, b));
            btn.image = img
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)
        tk.Button(self.display_area, text="בדוק", command=self.finish, bg="orange", font=("Arial", 12, "bold")).pack(
            pady=10)

    def toggle(self, name, btn):
        if name in self.user_choices:
            self.user_choices.remove(name)
            btn.config(relief="flat", bd=0, bg="white")
        else:
            self.user_choices.append(name)
            btn.config(relief="solid", bd=4, bg="#d6eaf8")

    def finish(self):
        # ניקוי אזור התצוגה כדי להציג משוב
        for w in self.display_area.winfo_children(): w.destroy()

        num_shown = len(self.target_set)
        correct = [c for c in self.user_choices if c in self.target_set]
        missed = [m for m in self.target_set if m not in self.user_choices]
        wrong_picks = [w for w in self.user_choices if w not in self.target_set]

        score = (len(correct) / num_shown) * 100 if num_shown > 0 else 0

        # עדכון משוב ויזואלי (התיקון המבוקש)
        self.score_lbl.config(text=f"ציון: {score:.0f}%")
        self.pass_lbl.config(text=f"נכון: {', '.join(correct) if correct else 'אין'}")

        fail_msg = ""
        if missed: fail_msg += f"פספסת: {', '.join(missed)} "
        if wrong_picks: fail_msg += f"טעות בבחירה: {', '.join(wrong_picks)}"
        self.fail_lbl.config(text=fail_msg)

        mode = self.mode_var.get()
        if score == 100 and len(self.user_choices) == num_shown:
            self.all_data[self.current_user]["levels"][mode] += 1
        elif score < 50 and self.all_data[self.current_user]["levels"][mode] > 1:
            self.all_data[self.current_user]["levels"][mode] -= 1

        self.save_data()
        self.update_lvl_display()

    def show_achievements(self):
        win = tk.Toplevel(self.root);
        win.title("הישגים");
        win.geometry("600x400")
        cols = ("שם", "צורות", "תמונות", "מילים", "מספרים")
        tree = ttk.Treeview(win, columns=cols, show="headings")
        for c in cols: tree.heading(c, text=c); tree.column(c, width=100, anchor="center")
        tree.pack(fill="both", expand=True, padx=20, pady=20)
        for u, d in self.all_data.items():
            l = d.get("levels", {})
            tree.insert("", "end",
                        values=(u, l.get("צורות", 1), l.get("תמונות", 1), l.get("מילים", 1), l.get("מספרים", 1)))

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(self.all_data, f, indent=4, ensure_ascii=False)

    def exit_app(self):
        self.save_data();
        self.root.destroy();
        sys.exit()

    def show_progress_graph(self):
        # יצירת חלון חדש (Toplevel) שלא מפריע לחלון הראשי
        graph_win = tk.Toplevel(self.root)
        graph_win.title(f"גרף התקדמות - {self.current_user}")
        graph_win.geometry("500x400")
        graph_win.configure(bg="#f8f9fa")

        tk.Label(graph_win, text=f"רמות נוכחיות: {self.current_user}", font=("Arial", 16, "bold"), bg="#f8f9fa").pack(
            pady=10)

        # יצירת משטח ציור
        canvas = tk.Canvas(graph_win, width=400, height=250, bg="white", highlightthickness=1,
                           highlightbackground="#ccc")
        canvas.pack(pady=20)

        levels = self.all_data[self.current_user]["levels"]
        modes = list(levels.keys())
        values = list(levels.values())

        if not values: return

        # הגדרות לציור
        max_val = max(values) if max(values) > 0 else 1
        x_start = 50
        y_base = 220
        bar_width = 40
        spacing = 50

        for i, mode in enumerate(modes):
            # חישוב גובה העמודה (יחסי לרמה)
            bar_height = (values[i] / (max_val + 1)) * 180
            x0 = x_start + i * (bar_width + spacing)
            y0 = y_base - bar_height
            x1 = x0 + bar_width
            y1 = y_base

            # ציור העמודה
            color = ["#3498db", "#e74c3c", "#2ecc71", "#f1c40f"][i % 4]
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#2c3e50")

            # כיתוב הרמה מעל העמודה
            canvas.create_text(x0 + bar_width / 2, y0 - 10, text=str(values[i]), font=("Arial", 10, "bold"))

            # כיתוב שם המוד מתחת לעמודה
            canvas.create_text(x0 + bar_width / 2, y_base + 15, text=mode, font=("Arial", 10))

        tk.Button(graph_win, text="סגור", command=graph_win.destroy, bg="#95a5a6", fg="white").pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk();
    app = MemoryMasterUltimate(root);
    root.mainloop()
