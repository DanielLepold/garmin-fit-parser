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
    A service class to handle authentication and downloading Garmin activity data.

    This class uses the `garminconnect` library to log in to a Garmin Connect account and download
    activity metadata and original .fit files as in-memory binary data.

    Attributes:
        client (Garmin): Authenticated Garmin client.
    """

    def __init__(self, email_address: str, password: str):
        """
        Initializes the GarminService and authenticates the Garmin client.

        Args:
            email_address (str): Garmin account email address.
            password (str): Garmin account password.

        Raises:
            GarminConnectConnectionError: When connection to Garmin Connect fails.
            GarminConnectAuthenticationError: When authentication fails (wrong credentials).
            GarminConnectTooManyRequestsError: When the client is rate-limited by Garmin.
            Exception: For any other unexpected error during login.
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
        """
        Downloads a specified number of activities from the authenticated Garmin account.

        This method filters activities by type (`running`, `trail_running`, `walking`, `cycling`)
        and returns metadata along with the raw .fit file content in memory.

        Args:
            number (int): Number of recent activities to download.

        Returns:
            list[dict]: A list of activity dictionaries containing:
                - id (int): The activity ID.
                - name (str): The name of the activity.
                - type (str): Activity type (e.g., running, walking).
                - time (datetime): Local start time of the activity.
                - data (bytes): Raw binary content of the .fit file.
                - vo2_max (float): Placeholder for VO2 Max value (default 0, to be parsed later).
        """
        activities = self.client.get_activities(0, number)
        result: list[dict[str, Any]] = []

        for activity in activities:
            activity_type = activity.get("activityType", {}).get("typeKey", "").lower()
            if activity_type not in {"running", "trail_running", "walking", "cycling"}:
                continue

            activity_id = activity.get("activityId")
            activity_name = activity.get("activityName", "Unnamed Activity")
            activity_time = activity.get("startTimeLocal")

            print(f"⬇️  Downloading: {activity_name}, "
                  f"ID: {activity_id}, "
                  f"Type: {activity_type}, "
                  f"Time: {activity_time}")

            try:
                fit_data = self.client.download_activity(
                    activity_id,
                    dl_fmt=self.client.ActivityDownloadFormat.ORIGINAL
                )

                start_time_dt = datetime.strptime(activity_time, "%Y-%m-%d %H:%M:%S") if activity_time else None

                summary = {
                    "id": activity_id,
                    "name": activity_name,
                    "type": activity_type,
                    "time": start_time_dt,
                    "data": fit_data,
                    "vo2_max": 0
                }
                result.append(summary)

            except Exception as e:
                print(f"❌ Failed to download activity {activity_id}: {e}")

        return result
