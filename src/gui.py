import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
import garmin_service as GS
import fit_sdk_parser as FSP
import visualisation

class GarminDownloaderGUI:
    def __init__(self):
        self.email = None
        self.password = None
        self.number = None

    def run(self):
        root = tk.Tk()
        root.withdraw()

        self.email = simpledialog.askstring("Email", "Enter your email:")
        if not self.email:
            messagebox.showerror("Error", "Email is required.")
            return

        self.password = simpledialog.askstring("Password", "Enter your password:", show='*')
        if not self.password:
            messagebox.showerror("Error", "Password is required.")
            return

        self.number = simpledialog.askinteger("Number", "Number of activities to download:")
        if self.number is None:
            messagebox.showerror("Error", "Number is required.")
            return

        # Summary
        summary = f"""Summary:
                  Email: {self.email}
                  Password: {'*' * len(self.password)}
                  Number of Activities: {self.number}"""
        messagebox.showinfo("Summary", summary)

        results = GS.GarminService(email_address=self.email,
                                    password=self.password).download_activities(number=self.number)

        FSP.Parser(results).parse_vo2_max_values()

        visualisation.plot_vo2_max_values(results)
