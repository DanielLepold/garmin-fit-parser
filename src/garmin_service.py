from typing import Any
from datetime import datetime

from garminconnect import (
  Garmin,
  GarminConnectConnectionError,
  GarminConnectAuthenticationError,
  GarminConnectTooManyRequestsError
)


class GarminService:
  """
  A service class to handle authentication and downloading Garmin activities.
  """

  def __init__(self, email_address: str, password: str):
    """
    Initializes and authenticates the Garmin client.

    Args:
        email_address (str): Garmin account email.
        password (str): Garmin account password.

    Raises:
        Exception: If login fails.
        :rtype: object
    """
    try:
      self.client = Garmin(email_address, password)
      self.client.login()
      print("✅ Successfully logged in to Garmin Connect!")
    except GarminConnectConnectionError:
      print("❌ Connection error: Unable to connect to Garmin Connect.")
      raise
    except GarminConnectAuthenticationError:
      print("❌ Authentication failed: Invalid email or password.")
      raise
    except GarminConnectTooManyRequestsError:
      print("❌ Too many requests: Rate limited by Garmin Connect.")
      raise
    except Exception as e:
      print(f"❌ Unknown error occurred during login: {e}")
      raise

  def download_activities(self, number: int) -> list[dict]:
    activities = self.client.get_activities(0, number)
    result: list[dict[str, Any]] = []

    for activity in activities:
        activity_type = activity.get("activityType", {}).get("typeKey","").lower()
        if activity_type not in {"running", "trail_running", "walking", "cycling"}:
          continue

        activity_id = activity.get("activityId")
        activity_name = activity.get("activityName", "Unnamed Activity")
        activity_time = activity.get("startTimeLocal") #"2025-04-16 17:23:45",

        print(f"⬇️  Downloading: {activity_name}, "
              f" ID: {activity_id},"
              f" Type: {activity_type},"
              f" Time: {activity_time}")

        try:
            fit_data = self.client.download_activity(
                activity_id,
                dl_fmt=self.client.ActivityDownloadFormat.ORIGINAL
            )

            start_time_str = activity.get( "startTimeLocal") #Time: 2025-01-19 11:23:20
            start_time_dt = datetime.strptime(start_time_str,"%Y-%m-%d %H:%M:%S") if start_time_str else None

            summary = {
              "id": activity.get("activityId"),
              "name": activity.get("activityName", "Unnamed Activity"),
              "type": activity_type,
              "time": start_time_dt,
              "data" : fit_data,
              "vo2_max" : 0
            }
            result.append(summary)

        except Exception as e:
                print(f"❌ Failed to save file {activity_id}: {e}")

    return result
