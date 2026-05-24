import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.widgets import Button

TYPE_COLORS = {
    "running": "royalblue",
    "trail_running": "forestgreen",
    "walking": "darkorange",
    "cycling": "crimson",
}

AVAILABLE_PANELS = {
    "vo2":      ("vo2_max",     "VO₂ Max (ml/kg/min)", "VO₂ Max Progression",   lambda e: e.get("vo2_max", 0) > 0),
    "distance": ("distance_km", "Distance (km)",        "Distance per Activity", lambda e: e.get("distance_km", 0) > 0),
    "hr":       ("avg_hr",      "Avg Heart Rate (bpm)", "Average Heart Rate",    lambda e: e.get("avg_hr")),
}


def ask_panels() -> list[str]:
    """Interactively asks the user which panels to show."""
    print("\nWhat would you like to plot?")
    print("  1  VO₂ Max progression")
    print("  2  Distance per activity")
    print("  3  Average heart rate")
    print()
    raw = input("Enter numbers separated by commas (e.g. 1,3) or press Enter for all: ").strip()

    mapping = {"1": "vo2", "2": "distance", "3": "hr"}
    if not raw:
        return list(mapping.values())

    selected = [mapping[t.strip()] for t in raw.split(",") if t.strip() in mapping]
    return selected or list(mapping.values())


def _draw_panel(ax, entries, ylabel, title, idx, total):
    ax.clear()
    ts, vals, typs = zip(*entries)

    ax.plot(ts, vals, color="steelblue", linestyle="-", linewidth=1.5, zorder=2)

    seen = set()
    for t, v, typ in zip(ts, vals, typs):
        color = TYPE_COLORS.get(typ, "gray")
        ax.scatter(t, v, color=color, zorder=3, label=typ if typ not in seen else None)
        seen.add(typ)

    ax.set_title(f"{title}", fontsize=13, fontweight="bold")
    ax.set_ylabel(ylabel)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")
    ax.grid(True, alpha=0.3)

    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(handles, labels, title="Activity type", fontsize=8)

    ax.figure.suptitle(
        f"Garmin Activity Dashboard  —  {idx + 1} / {total}",
        fontsize=12, color="gray",
    )
    ax.figure.canvas.draw()


def plot_dashboard(input_list: list[dict], panels: list[str] | None = None) -> None:
    sorted_data = sorted(
        [e for e in input_list if e.get("time")],
        key=lambda x: x["time"],
    )

    if not sorted_data:
        print("🚫 No activity data to plot.")
        return

    times = [e["time"] for e in sorted_data]
    types = [e["type"] for e in sorted_data]

    requested = panels or list(AVAILABLE_PANELS.keys())
    active_panels = []
    for key in requested:
        field, ylabel, title, pred = AVAILABLE_PANELS[key]
        entries = [(t, e[field], typ) for t, e, typ in zip(times, sorted_data, types) if pred(e)]
        if entries:
            active_panels.append((entries, ylabel, title))
        else:
            print(f"  — No data for '{title}', skipping.")

    if not active_panels:
        print("🚫 No plottable data found.")
        return

    fig, ax = plt.subplots(figsize=(13, 6))
    plt.subplots_adjust(bottom=0.18)

    current = [0]

    def draw(idx):
        entries, ylabel, title = active_panels[idx]
        _draw_panel(ax, entries, ylabel, title, idx, len(active_panels))
        btn_prev.ax.set_visible(len(active_panels) > 1)
        btn_next.ax.set_visible(len(active_panels) > 1)

    ax_prev = plt.axes([0.25, 0.04, 0.18, 0.06])
    ax_next = plt.axes([0.57, 0.04, 0.18, 0.06])
    btn_prev = Button(ax_prev, "← Previous")
    btn_next = Button(ax_next, "Next →")

    def on_prev(_):
        current[0] = (current[0] - 1) % len(active_panels)
        draw(current[0])

    def on_next(_):
        current[0] = (current[0] + 1) % len(active_panels)
        draw(current[0])

    btn_prev.on_clicked(on_prev)
    btn_next.on_clicked(on_next)

    draw(0)
    plt.show()


# Backwards-compatible alias
plot_vo2_max_values = plot_dashboard
