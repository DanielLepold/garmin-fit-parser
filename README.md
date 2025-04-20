# Garmin fir parser

A lightweight Python tool for downloading recent Garmin activities, extracting **VO₂ Max** values from `.fit` files, and visualizing the progression by activity type.

---

## 📦 Features

- 🔐 Secure login via GUI (email & password)
- ⬇️ Downloads recent Garmin activities (Running, Trail Running, Walking, Cycling)
- 💾 Parses `.fit` data **in memory** – no need to save files locally
- 🧠 Extracts **VO₂ Max** values using `garmin_fit_sdk`
- 📊 Plots progression over time with points color-coded by activity type

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/garmin-vo2-extractor.git
cd garmin-vo2-extractor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python main.py
```

A GUI window will appear to input your credentials and choose how many recent activities to download.

---

## 🧩 Module Overview

### `main.py`

Entry point. Launches the GUI and coordinates the process:
- Login
- Activity download
- VO₂ Max extraction
- Plotting

---

### `gui.py`

Tkinter-based GUI interface.

- Prompts for:
  - Email
  - Password
  - Number of activities
- Calls `GarminService`, `Parser`, and the visualizer.

---

### `garmin_service.py`

Garmin Connect interface layer.

- Authenticates via `garminconnect`
- Downloads `.fit` files as binary
- Filters activities by supported types
- Returns in-memory data with activity metadata

---

### `fit_sdk_parser.py`

Parser for in-memory `.fit` files.

- Uses `garmin_fit_sdk` to decode
- Extracts **VO₂ Max** from message type `140`
- Attaches values back to each activity entry

---

### `visualisation.py`

Matplotlib-based chart rendering.

- Connects VO₂ Max values with a line (dark blue)
- Adds colored dots per activity type:
  - `running`: 🔵 blue
  - `trail_running`: 🟢 green
  - `walking`: 🟠 orange
  - `cycling`: 🔴 red
- Displays timeline-based progression

---

## 🖼 Sample Output

```
VO₂ Max Progression by Activity Type
```

![Sample Chart Placeholder](./sample_plot.png)

> Replace this with a real plot image if needed.

---

## 📁 Example Folder Structure

```
garmin-vo2-extractor/
├── main.py
├── gui.py
├── garmin_service.py
├── fit_sdk_parser.py
├── visualisation.py
├── requirements.txt
└── README.md
```

---

## 📦 Requirements

- Python 3.12.6
- Dependencies:
  - `garminconnect`
  - `garmin-fit-sdk`
  - `matplotlib`
  - `tkinter` *(usually bundled with Python)*

---

## 🛠 Packaging to EXE (Optional)

To package as a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

Output will be in `dist/main.exe`.

---

## ⚠️ Disclaimer

This project is **not affiliated with Garmin**. Use at your own discretion. All credentials are handled locally via GUI and not stored.

---

## 📄 License

MIT License © 2025 [Your Name]
