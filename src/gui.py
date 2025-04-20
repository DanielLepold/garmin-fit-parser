import tkinter as tk
from tkinter import simpledialog, messagebox
import garmin_service as GS
import fit_sdk_parser as FSP
import visualisation

class GarminDownloaderGUI:
    """
    A simple GUI class to interactively download Garmin activities using tkinter dialogs.

    This class prompts the user for email, password, and number of activities,
    then downloads the activities via the GarminService, parses VO2 max values from
    the activity data, and finally visualizes the VO2 max progression.

    Attributes:
        email (str): Garmin account email address entered by the user.
        password (str): Garmin account password entered by the user.
        number (int): Number of recent activities to download.
    """

    def __init__(self):
        """
        Initializes the GarminDownloaderGUI with default None values.
        """
        self.email = None
        self.password = None
        self.number = None

    def run(self):
        """
        Runs the GUI workflow:

        1. Prompts user for email, password, and number of activities.
        2. Displays a summary confirmation.
        3. Downloads the selected number of activities from Garmin.
        4. Parses VO₂ Max values from the downloaded FIT files.
        5. Displays a line chart of VO₂ Max progression.

        Raises:
            Shows an error message using tkinter if any required input is missing.
        """
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

        # Show summary confirmation
        summary = f"""Summary:
                  Email: {self.email}
                  Password: {'*' * len(self.password)}
                  Number of Activities: {self.number}"""
        messagebox.showinfo("Summary", summary)

        # Download activities and process them
        results = GS.GarminService(
            email_address=self.email,
            password=self.password
        ).download_activities(number=self.number)

        FSP.Parser(results).parse_vo2_max_values()

        visualisation.plot_vo2_max_values(results)
