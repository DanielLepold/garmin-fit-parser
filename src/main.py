import gui


if __name__ == "__main__":
  # Entry point of the program.
  #
  # This block is executed when the script is run directly.
  # It creates an instance of the GarminDownloaderGUI class and
  # launches the GUI flow for downloading and processing Garmin activities.

  gui = gui.GarminDownloaderGUI()
  gui.run()
