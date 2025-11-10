# src/gui.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .caesar import encrypt, decrypt
from .fileio import read_text, write_text

def _get_shift(val: str) -> int:
    try:
        return int(val) % 26
    except ValueError:
        raise ValueError("Shift must be an integer.")

def run_gui() -> int:
    root = tk.Tk()
    root.title("caesar-lite")
    root.minsize(700, 420)

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)

    # ---------- Text Tab ----------
    text_tab = ttk.Frame(nb)
    nb.add(text_tab, text="Text")

    frm_top = ttk.Frame(text_tab, padding=8)
    frm_top.pack(fill="x")

    ttk.Label(frm_top, text="Shift (0–25):").pack(side="left")
    shift_var = tk.StringVar(value="3")
    sp = ttk.Spinbox(frm_top, from_=0, to=25, textvariable=shift_var, width=5)
    sp.pack(side="left", padx=6)

    btn_encrypt = ttk.Button(frm_top, text="Encrypt")
    btn_decrypt = ttk.Button(frm_top, text="Decrypt")
    btn_encrypt.pack(side="left", padx=6)
    btn_decrypt.pack(side="left", padx=6)

    paned = ttk.PanedWindow(text_tab, orient="horizontal")
    paned.pack(fill="both", expand=True, padx=8, pady=8)

    # Input
    left = ttk.Frame(paned)
    ttk.Label(left, text="Input").pack(anchor="w")
    txt_in = tk.Text(left, wrap="word", height=15)
    txt_in.pack(fill="both", expand=True)
    paned.add(left, weight=1)

    # Output
    right = ttk.Frame(paned)
    ttk.Label(right, text="Output").pack(anchor="w")
    txt_out = tk.Text(right, wrap="word", height=15, state="normal")
    txt_out.pack(fill="both", expand=True)
    paned.add(right, weight=1)

    def process_text(mode: str):
        try:
            s = _get_shift(shift_var.get())
            text = txt_in.get("1.0", "end-1c")
            fn = encrypt if mode == "enc" else decrypt
            result = fn(text, s)
            txt_out.delete("1.0", "end")
            txt_out.insert("1.0", result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    btn_encrypt.configure(command=lambda: process_text("enc"))
    btn_decrypt.configure(command=lambda: process_text("dec"))

    # ---------- File Tab ----------
    file_tab = ttk.Frame(nb, padding=8)
    nb.add(file_tab, text="File")

    in_path = tk.StringVar()
    out_path = tk.StringVar()
    shift_file_var = tk.StringVar(value="3")

    grid = ttk.Frame(file_tab)
    grid.pack(fill="x", pady=4)

    ttk.Label(grid, text="Input file:").grid(row=0, column=0, sticky="w")
    ent_in = ttk.Entry(grid, textvariable=in_path, width=60)
    ent_in.grid(row=0, column=1, padx=6)
    ttk.Button(grid, text="Browse...", command=lambda: _browse_in(in_path, out_path)).grid(row=0, column=2)

    ttk.Label(grid, text="Output file:").grid(row=1, column=0, sticky="w")
    ent_out = ttk.Entry(grid, textvariable=out_path, width=60)
    ent_out.grid(row=1, column=1, padx=6)
    ttk.Button(grid, text="Save as...", command=lambda: _browse_out(out_path)).grid(row=1, column=2)

    ttk.Label(grid, text="Shift (0–25):").grid(row=2, column=0, sticky="w", pady=(8,0))
    sp2 = ttk.Spinbox(grid, from_=0, to=25, textvariable=shift_file_var, width=5)
    sp2.grid(row=2, column=1, sticky="w", pady=(8,0))

    btn_row = ttk.Frame(file_tab)
    btn_row.pack(fill="x", pady=10)
    ttk.Button(btn_row, text="Encrypt File", command=lambda: _process_file("enc")).pack(side="left", padx=6)
    ttk.Button(btn_row, text="Decrypt File", command=lambda: _process_file("dec")).pack(side="left", padx=6)

    def _browse_in(invar: tk.StringVar, outvar: tk.StringVar):
        path = filedialog.askopenfilename(title="Select input file")
        if path:
            invar.set(path)
            # suggest output name
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
