import argparse
import getpass
import os
import sys

import garmin_service as GS
import fit_sdk_parser as FSP
import visualisation


def main():
    parser = argparse.ArgumentParser(
        description="Download and visualize Garmin activities",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--email", default=os.getenv("GARMIN_EMAIL"), help="Garmin account email (or set GARMIN_EMAIL env var)")
    parser.add_argument("--number", type=int, default=50, help="Number of recent activities to fetch")
    parser.add_argument("--gui", action="store_true", help="Launch tkinter GUI instead of CLI")
    args = parser.parse_args()

    if args.gui:
        import gui
        gui.GarminDownloaderGUI().run()
        return

    email = args.email or input("Garmin email: ")
    password = os.getenv("GARMIN_PASSWORD") or getpass.getpass("Garmin password: ")

    service = GS.GarminService(email, password)
    results = service.download_activities(number=args.number)

    if not results:
        print("No supported activities found.")
        sys.exit(0)

    FSP.Parser(results).parse_vo2_max_values()
    selected_panels = visualisation.ask_panels()
    visualisation.plot_dashboard(results, panels=selected_panels)


if __name__ == "__main__":
    main()
