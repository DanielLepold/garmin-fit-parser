import matplotlib.pyplot as plt

def plot_vo2_max_values(input_list: list[dict]):
  """
      Plots VO₂ Max progression over time, differentiating activity types with colored points.

      This function filters out entries that do not contain a valid VO₂ Max value (> 0),
      sorts the remaining entries by date, and plots the VO₂ Max trend line. Each data point
      is colored according to its activity type (e.g., running, cycling). A legend is shown
      to indicate which color corresponds to which activity.

      Args:
          input_list (list[dict]): A list of activity dictionaries. Each dictionary must contain:
              - "time" (datetime): The timestamp of the activity.
              - "vo2_max" (float): The VO₂ Max value.
              - "type" (str): The type of activity (e.g., "running", "walking").

      Notes:
          - If no valid VO₂ Max values are found, a warning is printed and nothing is plotted.
          - The activity types are color-coded:
              - Running: blue
              - Trail running: green
              - Walking: orange
              - Cycling: red
              - Any unknown type defaults to gray.

      Example:
          plot_vo2_max_values(my_activity_list)
  """
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
