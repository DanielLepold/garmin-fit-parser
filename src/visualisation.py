import matplotlib.pyplot as plt

def plot_vo2_max_values(input_list: list[dict]):
  filtered_data = [
    entry for entry in input_list
    if entry.get("vo2_max") and entry["vo2_max"] > 0
  ]

  if not filtered_data:
    print("🚫 No VO₂ Max values to plot.")


  type_colors = {
    "running": "blue",
    "trail_running": "green",
    "walking": "orange",
    "cycling": "red"
  }

  sorted_data = sorted(filtered_data, key=lambda x: x["time"])
  times = [entry["time"] for entry in sorted_data]
  values = [entry["vo2_max"] for entry in sorted_data]
  types = [entry["type"] for entry in sorted_data]

  plt.figure(figsize=(12, 5))
  plt.plot(times, values, color="darkblue", linestyle='-', label="VO₂ Max")

  for time, value, typ in zip(times, values, types):
    plt.scatter(time, value, color=type_colors.get(typ, "gray"), label=typ)

  seen = set()
  handles = []
  labels = []
  for typ in types:
    if typ not in seen:
      seen.add(typ)
      color = type_colors.get(typ, "gray")
      handles.append(
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color,
                   label=typ))
      labels.append(typ)

  plt.legend(handles, labels, title="Activity Type")
  plt.title("VO₂ Max Progression by Activity Type")
  plt.xlabel("Date")
  plt.ylabel("VO₂ Max")
  plt.xticks(rotation=90, ha='right')
  plt.grid(True)
  plt.tight_layout()
  plt.show()
