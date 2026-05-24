import os
from typing import Any, Callable, Optional
from datetime import datetime

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
)

TOKEN_DIR = os.path.expanduser("~/.garminconnect")

SUPPORTED_ACTIVITY_TYPES = {"running", "trail_running", "walking", "cycling"}


class GarminService:
    """Handles authentication and activity downloading from Garmin Connect."""

    def __init__(self, email_address: str, password: str, prompt_mfa: Optional[Callable] = None):
        """
        Authenticates with Garmin Connect, using cached tokens when available.

        On first login (or after token expiry), Garmin may trigger 2FA. The
        prompt_mfa callback is called to retrieve the code; defaults to a
        terminal prompt. Tokens are saved to ~/.garminconnect after a fresh
        login so subsequent runs skip 2FA entirely.

        Args:
            email_address: Garmin account email.
            password: Garmin account password.
            prompt_mfa: Optional callable that returns the MFA code string.
        """
        mfa_callback = prompt_mfa or (lambda: input("Enter Garmin 2FA code: "))

        try:
            self.client = Garmin(email_address, password, prompt_mfa=mfa_callback)
            self._login_with_token_fallback()
        except GarminConnectConnectionError:
            print("❌ Connection error: Unable to reach Garmin Connect.")
            raise
        except GarminConnectAuthenticationError:
            print("❌ Authentication failed: check email and password.")
            raise
        except GarminConnectTooManyRequestsError:
            print("❌ Rate limited by Garmin Connect. Try again later.")
            raise
        except Exception as e:
            print(f"❌ Login error: {e}")
            raise

    def _login_with_token_fallback(self):
        try:
            self.client.login(TOKEN_DIR)
            print("✅ Logged in using saved tokens")
        except Exception:
            self.client.login()
            os.makedirs(TOKEN_DIR, exist_ok=True)
            self.client.garth.dump(TOKEN_DIR)
            print("✅ Logged in and saved tokens for next time")

    def download_activities(self, number: int) -> list[dict]:
        """
        Downloads recent activities filtered by supported types.

        Args:
            number: How many recent activities to fetch from the API.

        Returns:
            List of activity dicts with metadata and raw .fit binary.
        """
        activities = self.client.get_activities(0, number)
        result: list[dict[str, Any]] = []

        for activity in activities:
            activity_type = activity.get("activityType", {}).get("typeKey", "").lower()
            if activity_type not in SUPPORTED_ACTIVITY_TYPES:
                continue

            activity_id = activity.get("activityId")
            activity_name = activity.get("activityName", "Unnamed Activity")
            activity_time = activity.get("startTimeLocal")

            print(f"⬇️  {activity_name} ({activity_type}, {activity_time})")

            try:
                fit_data = self.client.download_activity(
                    activity_id,
                    dl_fmt=self.client.ActivityDownloadFormat.ORIGINAL,
                )
                start_time = (
                    datetime.strptime(activity_time, "%Y-%m-%d %H:%M:%S")
                    if activity_time
                    else None
                )
                result.append({
                    "id": activity_id,
                    "name": activity_name,
                    "type": activity_type,
                    "time": start_time,
                    "data": fit_data,
                    "vo2_max": 0,
                    "distance_km": round(activity.get("distance", 0) / 1000, 2),
                    "duration_min": round(activity.get("duration", 0) / 60, 1),
                    "avg_hr": activity.get("averageHR"),
                    "max_hr": activity.get("maxHR"),
                    "calories": activity.get("calories"),
                    "elevation_gain": activity.get("elevationGain"),
                })
            except Exception as e:
                print(f"❌ Failed to download activity {activity_id}: {e}")

        return result
