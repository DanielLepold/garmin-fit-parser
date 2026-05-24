import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

import garmin_service as GS
import fit_sdk_parser as FSP
import visualisation


def _ask_panels_gui(root: tk.Tk) -> list[str]:
    """Checkbox dialog for selecting which panels to plot."""
    dialog = tk.Toplevel(root)
    dialog.title("What to plot?")
    dialog.resizable(False, False)

    options = [
        ("vo2",      "VO₂ Max progression"),
        ("distance", "Distance per activity"),
        ("hr",       "Average heart rate"),
    ]
    vars_ = {key: tk.BooleanVar(value=True) for key, _ in options}

    tk.Label(dialog, text="Select metrics to display:", font=("", 11)).pack(padx=20, pady=(16, 8))
    for key, label in options:
        tk.Checkbutton(dialog, text=label, variable=vars_[key], font=("", 10)).pack(anchor="w", padx=30)

    result = []

    def confirm():
        result.extend(key for key, _ in options if vars_[key].get())
        dialog.destroy()

    tk.Button(dialog, text="Plot", command=confirm, width=12).pack(pady=16)
    dialog.grab_set()
    root.wait_window(dialog)
    return result


class GarminDownloaderGUI:
    """Tkinter GUI for downloading and visualizing Garmin activities."""

    def run(self):
        root = tk.Tk()
        root.withdraw()

        email = simpledialog.askstring("Login", "Garmin email:")
        if not email:
            messagebox.showerror("Error", "Email is required.")
            return

        password = simpledialog.askstring("Login", "Garmin password:", show="*")
        if not password:
            messagebox.showerror("Error", "Password is required.")
            return

        number = simpledialog.askinteger("Activities", "Number of activities to download:", initialvalue=50)
        if number is None:
            messagebox.showerror("Error", "Number is required.")
            return

        def prompt_mfa():
            code = simpledialog.askstring("2FA", "Enter Garmin 2FA code:")
            return code or ""

        try:
            service = GS.GarminService(email, password, prompt_mfa=prompt_mfa)
            results = service.download_activities(number=number)
        except Exception as e:
            messagebox.showerror("Login failed", str(e))
            return

        if not results:
            messagebox.showinfo("Done", "No supported activities found.")
            return

        FSP.Parser(results).parse_vo2_max_values()
        selected = _ask_panels_gui(root)
        visualisation.plot_dashboard(results, panels=selected or None)
