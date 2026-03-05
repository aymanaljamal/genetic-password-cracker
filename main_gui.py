

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import random
import os
import csv
import math
from datetime import datetime


# =================== CONFIG ===================
PASSCODE_LENGTH = 16
EXPERIMENT_CONFIGS = [
    {"name": "Default",      "pop_size": 100, "mutation_rate": 0.01, "tournament_size": 5},
    {"name": "Large Pop",    "pop_size": 300, "mutation_rate": 0.01, "tournament_size": 5},
    {"name": "High Mutation","pop_size": 100, "mutation_rate": 0.05, "tournament_size": 5},
    {"name": "Small Tour",   "pop_size": 100, "mutation_rate": 0.01, "tournament_size": 3},
]
CHARSET = "01"  # Binary password


# =================== UTILS ===================
def generate_random_passcode(length):
    return ''.join(random.choice(CHARSET) for _ in range(length))


def fitness(individual, target):
    return sum(a == b for a, b in zip(individual, target))


def tournament_selection(population, target, k):
    selected = random.sample(population, k)
    return max(selected, key=lambda ind: fitness(ind, target))


def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:]


def mutate(individual, mutation_rate):
    return ''.join(
        (random.choice(CHARSET) if random.random() < mutation_rate else ch)
        for ch in individual
    )


def genetic_algorithm(target, pop_size, mutation_rate, tournament_size,
                      max_generations=5000, verbose=False, callback=None):
    length = len(target)
    population = [generate_random_passcode(length) for _ in range(pop_size)]
    convergence_data = []

    for gen in range(1, max_generations + 1):
        population.sort(key=lambda ind: fitness(ind, target), reverse=True)
        best = population[0]
        best_fit = fitness(best, target)
        convergence_data.append(best_fit)

        if callback:
            callback(gen, best, best_fit, len(target))

        if best == target:
            return best, convergence_data, gen

        new_population = [best]  # elitism
        while len(new_population) < pop_size:
            p1 = tournament_selection(population, target, tournament_size)
            p2 = tournament_selection(population, target, tournament_size)
            child = mutate(crossover(p1, p2), mutation_rate)
            new_population.append(child)
        population = new_population

    population.sort(key=lambda ind: fitness(ind, target), reverse=True)
    return population[0], convergence_data, max_generations


# =================== GUI ===================
class GeneticAlgoGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🧬 Password Cracker — Genetic Algorithm")
        self.geometry("1100x780")
        self.minsize(900, 650)
        self.configure(bg="#0f1117")
        self.resizable(True, True)

        # State
        self.target_passcode = tk.StringVar(value="")
        self.running = False
        self.current_thread = None
        self.results_summary = []
        self.all_convergence = {}

        self._build_ui()
        self._generate_target()

    # ──────────────────────────────────────────
    #  UI CONSTRUCTION
    # ──────────────────────────────────────────
    def _build_ui(self):
        # ── Top header ──
        header = tk.Frame(self, bg="#0f1117")
        header.pack(fill="x", padx=20, pady=(16, 0))

        tk.Label(header, text="🧬", font=("Segoe UI Emoji", 28),
                 bg="#0f1117", fg="#00ff9f").pack(side="left")
        tk.Label(header, text=" Genetic Password Cracker",
                 font=("Consolas", 22, "bold"),
                 bg="#0f1117", fg="#e0e0e0").pack(side="left", padx=8)

        # Version badge
        tk.Label(header, text="GUI v1.0", font=("Consolas", 10),
                 bg="#1e2235", fg="#888", padx=8, pady=3,
                 relief="flat").pack(side="right", padx=4)

        # ── Target section ──
        tgt_frame = tk.Frame(self, bg="#161b2e", bd=0, relief="flat")
        tgt_frame.pack(fill="x", padx=20, pady=(12, 0))
        tgt_frame.configure(highlightbackground="#2a3050", highlightthickness=1)

        tk.Label(tgt_frame, text="  Target Password",
                 font=("Consolas", 11, "bold"),
                 bg="#161b2e", fg="#7ecfff").pack(anchor="w", padx=12, pady=(8, 2))

        row = tk.Frame(tgt_frame, bg="#161b2e")
        row.pack(fill="x", padx=12, pady=(0, 10))

        self.target_display = tk.Label(
            row, textvariable=self.target_passcode,
            font=("Courier New", 15, "bold"),
            bg="#0d1120", fg="#00ff9f",
            padx=14, pady=8, anchor="w",
            relief="flat"
        )
        self.target_display.pack(side="left", fill="x", expand=True)

        btn_gen = tk.Button(row, text="⟳  New Target",
                            font=("Consolas", 10, "bold"),
                            bg="#1c3a5e", fg="#7ecfff",
                            activebackground="#2a5080", activeforeground="#fff",
                            bd=0, padx=14, pady=8, cursor="hand2",
                            command=self._generate_target)
        btn_gen.pack(side="right", padx=(8, 0))

        # ── Configs selector ──
        cfg_outer = tk.Frame(self, bg="#0f1117")
        cfg_outer.pack(fill="x", padx=20, pady=(10, 0))

        tk.Label(cfg_outer, text="Experiments to run:",
                 font=("Consolas", 10), bg="#0f1117", fg="#aaa").pack(anchor="w")

        cfg_grid = tk.Frame(cfg_outer, bg="#0f1117")
        cfg_grid.pack(fill="x", pady=4)

        self.cfg_vars = {}
        for i, cfg in enumerate(EXPERIMENT_CONFIGS):
            var = tk.BooleanVar(value=True)
            self.cfg_vars[cfg["name"]] = var
            cb = tk.Checkbutton(
                cfg_grid,
                text=f"  {cfg['name']}  (pop={cfg['pop_size']}, mut={cfg['mutation_rate']}, tour={cfg['tournament_size']})",
                variable=var,
                font=("Consolas", 10),
                bg="#161b2e", fg="#ccc",
                selectcolor="#1e2a40",
                activebackground="#161b2e", activeforeground="#fff",
                relief="flat", padx=10, pady=5,
                cursor="hand2"
            )
            cb.grid(row=i // 2, column=i % 2, sticky="w", padx=6, pady=2)

        # ── Control buttons ──
        ctrl = tk.Frame(self, bg="#0f1117")
        ctrl.pack(fill="x", padx=20, pady=(10, 0))

        self.btn_run = tk.Button(ctrl, text="▶  Run Experiments",
                                 font=("Consolas", 12, "bold"),
                                 bg="#00aa6c", fg="#fff",
                                 activebackground="#00cc80", activeforeground="#fff",
                                 bd=0, padx=20, pady=10, cursor="hand2",
                                 command=self._start_experiments)
        self.btn_run.pack(side="left")

        self.btn_stop = tk.Button(ctrl, text="■  Stop",
                                  font=("Consolas", 12, "bold"),
                                  bg="#aa2222", fg="#fff",
                                  activebackground="#cc3333", activeforeground="#fff",
                                  bd=0, padx=16, pady=10, cursor="hand2",
                                  state="disabled",
                                  command=self._stop_experiments)
        self.btn_stop.pack(side="left", padx=8)

        self.btn_clear = tk.Button(ctrl, text="🗑  Clear Log",
                                   font=("Consolas", 11),
                                   bg="#1e2235", fg="#aaa",
                                   activebackground="#2a3050", activeforeground="#fff",
                                   bd=0, padx=14, pady=10, cursor="hand2",
                                   command=self._clear_log)
        self.btn_clear.pack(side="right")

        # ── Progress bar ──
        prog_frame = tk.Frame(self, bg="#0f1117")
        prog_frame.pack(fill="x", padx=20, pady=(8, 0))

        self.progress_label = tk.Label(prog_frame, text="Ready",
                                       font=("Consolas", 10),
                                       bg="#0f1117", fg="#666")
        self.progress_label.pack(anchor="w")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("green.Horizontal.TProgressbar",
                         troughcolor="#1a1e2e", background="#00cc80",
                         thickness=8)

        self.progress = ttk.Progressbar(prog_frame, style="green.Horizontal.TProgressbar",
                                        orient="horizontal", length=400, mode="determinate")
        self.progress.pack(fill="x", pady=4)

        # ── Main paned area: log + chart ──
        paned = tk.PanedWindow(self, orient="horizontal",
                               bg="#0f1117", sashwidth=6, sashrelief="flat")
        paned.pack(fill="both", expand=True, padx=20, pady=10)

        # Log panel
        log_frame = tk.Frame(paned, bg="#161b2e",
                             highlightbackground="#2a3050", highlightthickness=1)
        paned.add(log_frame, minsize=380)

        tk.Label(log_frame, text="  Execution Log",
                 font=("Consolas", 11, "bold"),
                 bg="#161b2e", fg="#7ecfff").pack(anchor="w", padx=8, pady=(8, 2))

        self.log = scrolledtext.ScrolledText(
            log_frame,
            font=("Courier New", 10),
            bg="#0a0d18", fg="#c8d0e0",
            insertbackground="#00ff9f",
            selectbackground="#1e3a5a",
            relief="flat", bd=0,
            wrap="none",
            state="disabled"
        )
        self.log.pack(fill="both", expand=True, padx=6, pady=(0, 8))

        # Tag colours for log
        self.log.tag_config("green",  foreground="#00ff9f")
        self.log.tag_config("cyan",   foreground="#7ecfff")
        self.log.tag_config("yellow", foreground="#ffd866")
        self.log.tag_config("red",    foreground="#ff6b6b")
        self.log.tag_config("dim",    foreground="#555e7a")
        self.log.tag_config("white",  foreground="#e0e0e0")

        # Canvas (convergence chart)
        chart_frame = tk.Frame(paned, bg="#161b2e",
                               highlightbackground="#2a3050", highlightthickness=1)
        paned.add(chart_frame, minsize=300)

        tk.Label(chart_frame, text="  Convergence Chart",
                 font=("Consolas", 11, "bold"),
                 bg="#161b2e", fg="#7ecfff").pack(anchor="w", padx=8, pady=(8, 2))

        self.canvas = tk.Canvas(chart_frame, bg="#0a0d18",
                                highlightthickness=0, relief="flat")
        self.canvas.pack(fill="both", expand=True, padx=6, pady=(0, 8))
        self.canvas.bind("<Configure>", lambda e: self._redraw_chart())

        # ── Bottom summary bar ──
        self.summary_bar = tk.Label(self, text="No experiments run yet.",
                                    font=("Consolas", 10),
                                    bg="#161b2e", fg="#888",
                                    anchor="w", padx=14, pady=6)
        self.summary_bar.pack(fill="x", side="bottom")

    # ──────────────────────────────────────────
    #  ACTIONS
    # ──────────────────────────────────────────
    def _generate_target(self):
        self.target_passcode.set(generate_random_passcode(PASSCODE_LENGTH))
        self._log(f"New target generated: {self.target_passcode.get()}\n", "cyan")
        self.all_convergence.clear()
        self.results_summary.clear()
        self._redraw_chart()

    def _start_experiments(self):
        selected = [cfg for cfg in EXPERIMENT_CONFIGS if self.cfg_vars[cfg["name"]].get()]
        if not selected:
            messagebox.showwarning("No Config", "Please select at least one experiment configuration.")
            return

        self.running = True
        self.results_summary.clear()
        self.all_convergence.clear()
        self.btn_run.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.progress["value"] = 0

        self._log("\n" + "═" * 60 + "\n", "dim")
        self._log(f" Starting {len(selected)} experiment(s)  —  {datetime.now().strftime('%H:%M:%S')}\n", "white")
        self._log(f" Target: {self.target_passcode.get()}\n", "yellow")
        self._log("═" * 60 + "\n", "dim")

        self.current_thread = threading.Thread(
            target=self._run_all_experiments,
            args=(selected,),
            daemon=True
        )
        self.current_thread.start()

    def _stop_experiments(self):
        self.running = False
        self._log("\n⚠ Stop requested by user.\n", "red")

    def _clear_log(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")

    # ──────────────────────────────────────────
    #  EXPERIMENT RUNNER (background thread)
    # ──────────────────────────────────────────
    def _run_all_experiments(self, configs):
        target = self.target_passcode.get()
        total = len(configs)

        for idx, cfg in enumerate(configs):
            if not self.running:
                break
            self._run_single(target, cfg, idx, total)
            self._update_progress(int((idx + 1) / total * 100))

        self.after(0, self._on_experiments_done)

    def _run_single(self, target, cfg, idx, total):
        self._log(f"\n▶ [{idx+1}/{total}] {cfg['name']}\n", "cyan")
        self._log(f"   pop={cfg['pop_size']}  mut={cfg['mutation_rate']}  tour={cfg['tournament_size']}\n", "dim")

        start = time.time()
        gen_counter = [0]

        def cb(gen, best, best_fit, length):
            gen_counter[0] = gen
            if gen % 50 == 0 or best_fit == length:
                msg = f"   gen {gen:>5}  best_fit={best_fit}/{length}  [{best}]\n"
                tag = "green" if best_fit == length else "white"
                self._log(msg, tag)
                # update chart live
                if cfg["name"] in self.all_convergence:
                    self.after(0, self._redraw_chart)

        best, conv, gens = genetic_algorithm(
            target=target,
            pop_size=cfg["pop_size"],
            mutation_rate=cfg["mutation_rate"],
            tournament_size=cfg["tournament_size"],
            callback=cb
        )
        elapsed = time.time() - start
        success = best == target

        self.all_convergence[cfg["name"]] = conv
        self.results_summary.append({
            "config": cfg["name"],
            "generations": gens,
            "time": elapsed,
            "success": success
        })

        status = "✅ SUCCESS" if success else "❌ FAILED"
        color = "green" if success else "red"
        self._log(f"   {status}  —  {gens} generations  —  {elapsed:.2f}s\n", color)
        self.after(0, self._redraw_chart)

    def _on_experiments_done(self):
        self.running = False
        self.btn_run.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.progress["value"] = 100
        self.progress_label.config(text="Done ✓", fg="#00ff9f")
        self._log("\n" + "═" * 60 + "\n", "dim")
        self._log(" All experiments completed!\n", "yellow")
        self._print_summary()
        self._redraw_chart()

    def _print_summary(self):
        self._log("\n📊 Summary Table\n", "cyan")
        self._log(f"  {'Config':<16} {'Generations':>12} {'Time':>8}  {'Result'}\n", "white")
        self._log("  " + "-" * 48 + "\n", "dim")
        best_gens = min((r["generations"] for r in self.results_summary if r["success"]), default=None)
        for r in self.results_summary:
            marker = "★" if (r["success"] and r["generations"] == best_gens) else " "
            tag = "green" if r["success"] else "red"
            self._log(
                f" {marker} {r['config']:<16} {r['generations']:>12} {r['time']:>7.2f}s  "
                f"{'SUCCESS' if r['success'] else 'FAILED'}\n", tag
            )
        # update summary bar
        n_success = sum(1 for r in self.results_summary if r["success"])
        bar_text = f"  {n_success}/{len(self.results_summary)} experiments succeeded"
        if best_gens is not None:
            best = next(r for r in self.results_summary if r["success"] and r["generations"] == best_gens)
            bar_text += f"  |  Best: {best['config']} ({best_gens} gen, {best['time']:.2f}s)"
        self.summary_bar.config(text=bar_text, fg="#00ff9f" if n_success else "#ff6b6b")

    # ──────────────────────────────────────────
    #  CHART
    # ──────────────────────────────────────────
    COLORS = ["#00ff9f", "#7ecfff", "#ffd866", "#ff6b6b",
              "#c792ea", "#ff9f43", "#a8e063", "#48dbfb"]

    def _redraw_chart(self):
        c = self.canvas
        c.delete("all")
        W = c.winfo_width()
        H = c.winfo_height()
        if W < 10 or H < 10 or not self.all_convergence:
            return

        PAD_L, PAD_R, PAD_T, PAD_B = 52, 20, 20, 50
        plot_w = W - PAD_L - PAD_R
        plot_h = H - PAD_T - PAD_B

        # Background
        c.create_rectangle(0, 0, W, H, fill="#0a0d18", outline="")
        c.create_rectangle(PAD_L, PAD_T, PAD_L + plot_w, PAD_T + plot_h,
                           fill="#10152a", outline="#1e2a40")

        max_x = max(len(v) for v in self.all_convergence.values())
        max_y = PASSCODE_LENGTH

        # Grid lines
        for yi in range(0, max_y + 1, max(1, max_y // 8)):
            y = PAD_T + plot_h - (yi / max_y) * plot_h
            c.create_line(PAD_L, y, PAD_L + plot_w, y,
                          fill="#1a2030", dash=(3, 6))
            c.create_text(PAD_L - 6, y, text=str(yi),
                          font=("Courier New", 8), fill="#445", anchor="e")

        # X axis label
        c.create_text(PAD_L + plot_w // 2, H - 10,
                      text="Generation", font=("Consolas", 9), fill="#556")

        # Plots
        for i, (name, data) in enumerate(self.all_convergence.items()):
            color = self.COLORS[i % len(self.COLORS)]
            pts = []
            for gx, val in enumerate(data):
                x = PAD_L + (gx / max(max_x - 1, 1)) * plot_w
                y = PAD_T + plot_h - (val / max_y) * plot_h
                pts.extend([x, y])
            if len(pts) >= 4:
                c.create_line(*pts, fill=color, width=2, smooth=True)
            # Legend
            lx = PAD_L + 12
            ly = PAD_T + 10 + i * 18
            c.create_rectangle(lx, ly, lx + 14, ly + 10, fill=color, outline="")
            c.create_text(lx + 18, ly + 5, text=name,
                          font=("Consolas", 9), fill=color, anchor="w")

    # ──────────────────────────────────────────
    #  HELPERS
    # ──────────────────────────────────────────
    def _log(self, msg, tag="white"):
        def _write():
            self.log.config(state="normal")
            self.log.insert("end", msg, tag)
            self.log.see("end")
            self.log.config(state="disabled")
        self.after(0, _write)

    def _update_progress(self, value):
        def _set():
            self.progress["value"] = value
            self.progress_label.config(
                text=f"Running... {value}%",
                fg="#ffd866"
            )
        self.after(0, _set)


# =================== ENTRY ===================
if __name__ == "__main__":
    app = GeneticAlgoGUI()
    app.mainloop()