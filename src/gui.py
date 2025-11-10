# src/gui.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .caesar import encrypt, decrypt
from .fileio import read_text, write_text

def _get_shift(val: str) -> int:
    try:
        return int(val) % 26
    except ValueError:
        raise ValueError("Shift must be an integer between 0 and 25.")

def run_gui() -> int:
    root = tk.Tk()
    root.title("caesar-lite")
    root.minsize(760, 460)

    # ---------------- Dark Theme ----------------
    BG = "#1e1e1e"        # window background
    BG2 = "#2b2b2b"       # panels / tabs
    FG = "#ffffff"        # text
    ACCENT = "#3a86ff"    # accent (buttons/selected tab)
    ENTRY_BG = "#2d2d2d"  # text areas
    BORDER = "#3a3a3a"

    root.configure(bg=BG)
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(".", background=BG, foreground=FG)
    style.configure("TFrame", background=BG)
    style.configure("TLabel", background=BG, foreground=FG)
    style.configure("TButton", padding=6, relief="flat", background=ACCENT, foreground=FG)
    style.map("TButton",
              background=[("active", "#2b6dff"), ("pressed", "#2256cc")],
              relief=[("pressed", "groove")])

    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure("TNotebook.Tab", background=BG2, foreground=FG, padding=(12, 7), borderwidth=0)
    style.map("TNotebook.Tab",
              background=[("selected", ACCENT)],
              foreground=[("selected", "#ffffff")])

    style.configure("Separator.TFrame", background=BORDER)

    # --------------- Notebook -------------------
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=10, pady=10)

    text_tab = ttk.Frame(nb)
    file_tab = ttk.Frame(nb)
    nb.add(text_tab, text="Text")
    nb.add(file_tab, text="File")

    # ---------------- Text Tab ------------------
    top = ttk.Frame(text_tab)
    top.pack(fill="x", pady=(2, 8))

    ttk.Label(top, text="Shift (0–25):").pack(side="left")
    shift_var = tk.StringVar(value="3")
    sp = ttk.Spinbox(top, from_=0, to=25, textvariable=shift_var, width=5)
    sp.pack(side="left", padx=8)

    btn_encrypt = ttk.Button(top, text="Encrypt")
    btn_decrypt = ttk.Button(top, text="Decrypt")
    btn_encrypt.pack(side="left", padx=4)
    btn_decrypt.pack(side="left", padx=4)

    # paned: input | output
    paned = ttk.PanedWindow(text_tab, orient="horizontal")
    paned.pack(fill="both", expand=True)

    def make_text_area(parent, label):
        frame = ttk.Frame(parent)
        lbl = ttk.Label(frame, text=label)
        lbl.pack(anchor="w", padx=2, pady=(0, 4))
        txt = tk.Text(
            frame, wrap="word", height=15,
            bg=ENTRY_BG, fg=FG, insertbackground=FG,
            relief="flat", highlightthickness=1, highlightbackground=BORDER
        )
        txt.pack(fill="both", expand=True)
        return frame, txt

    left_frame, txt_in = make_text_area(paned, "Input")
    right_frame, txt_out = make_text_area(paned, "Output")

    paned.add(left_frame, weight=1)
    paned.add(right_frame, weight=1)

    def process_text(mode: str):
        try:
            s = _get_shift(shift_var.get())
            fn = encrypt if mode == "enc" else decrypt
            result = fn(txt_in.get("1.0", "end-1c"), s)
            txt_out.delete("1.0", "end")
            txt_out.insert("1.0", result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    btn_encrypt.configure(command=lambda: process_text("enc"))
    btn_decrypt.configure(command=lambda: process_text("dec"))

    # thin separator line
    ttk.Frame(text_tab, style="Separator.TFrame", height=1).pack(fill="x", pady=8)

    # ---------------- File Tab ------------------
    grid = ttk.Frame(file_tab)
    grid.pack(fill="x", pady=6)

    in_path = tk.StringVar()
    out_path = tk.StringVar()
    shift_file_var = tk.StringVar(value="3")

    ttk.Label(grid, text="Input file:").grid(row=0, column=0, sticky="w", padx=4, pady=6)
    ent_in = ttk.Entry(grid, textvariable=in_path, width=60)
    ent_in.grid(row=0, column=1, padx=6)
    ttk.Button(grid, text="Browse...", command=lambda: _browse_in(in_path, out_path)).grid(row=0, column=2, padx=4)

    ttk.Label(grid, text="Output file:").grid(row=1, column=0, sticky="w", padx=4, pady=6)
    ent_out = ttk.Entry(grid, textvariable=out_path, width=60)
    ent_out.grid(row=1, column=1, padx=6)
    ttk.Button(grid, text="Save as...", command=lambda: _browse_out(out_path)).grid(row=1, column=2, padx=4)

    ttk.Label(grid, text="Shift (0–25):").grid(row=2, column=0, sticky="w", padx=4, pady=(10, 0))
    sp2 = ttk.Spinbox(grid, from_=0, to=25, textvariable=shift_file_var, width=5)
    sp2.grid(row=2, column=1, sticky="w", padx=6, pady=(10, 0))

    btn_row = ttk.Frame(file_tab)
    btn_row.pack(fill="x", pady=12)
    ttk.Button(btn_row, text="Encrypt File", command=lambda: _process_file("enc")).pack(side="left", padx=6)
    ttk.Button(btn_row, text="Decrypt File", command=lambda: _process_file("dec")).pack(side="left", padx=6)

    def _browse_in(invar: tk.StringVar, outvar: tk.StringVar):
        path = filedialog.askopenfilename(title="Select input file")
        if path:
            invar.set(path)
            if not outvar.get():
                if path.endswith(".enc.txt"):
                    outvar.set(path.replace(".enc.txt", ".dec.txt"))
                else:
                    outvar.set(path + ".enc.txt")

    def _browse_out(outvar: tk.StringVar):
        path = filedialog.asksaveasfilename(title="Save output as")
        if path:
            outvar.set(path)

    def _process_file(mode: str):
        try:
            s = _get_shift(shift_file_var.get())
            inp = in_path.get().strip()
            outp = out_path.get().strip()
            if not inp:
                raise ValueError("Please choose an input file.")
            if not outp:
                raise ValueError("Please choose an output file.")
            data = read_text(inp)
            fn = encrypt if mode == "enc" else decrypt
            result = fn(data, s)
            write_text(outp, result)
            messagebox.showinfo("Success", f"Written: {outp}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    root.mainloop()
    return 0

if __name__ == "__main__":
    raise SystemExit(run_gui())
