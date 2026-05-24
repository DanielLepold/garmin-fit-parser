from garmin_fit_sdk import Decoder, Stream
import utils


class Parser:
    """Parses in-memory .fit files and extracts VO2 Max values."""

    def __init__(self, input_list: list[dict]):
        self.input_list = input_list
        self._vo2_max_value = 0.0

    def _mesg_listener(self, mesg_num: int, message: dict):
        if mesg_num == 140 and 7 in message:  # 140 = VO2 Max, field 7 = raw value
            self._vo2_max_value = message[7] * 3.5 / 65536

    def parse_vo2_max_values(self) -> "Parser":
        """Decodes each .fit entry and attaches the extracted VO2 Max to the dict."""
        for entry in self.input_list:
            self._vo2_max_value = 0.0

            print(f"📂 Parsing: {entry['name']}")

            fit_stream = utils.extract_fit_stream(entry["data"])
            if fit_stream is None:
                print(f"  ⚠️ Could not extract .fit data from {entry['name']}")
                continue

            stream = Stream.from_bytes_io(fit_stream)
            decoder = Decoder(stream)
            _, errors = decoder.read(mesg_listener=self._mesg_listener)
            stream.close()

            if errors:
                print(f"  ⚠️ Decode errors in {entry['name']}: {errors}")

            if self._vo2_max_value > 0:
                entry["vo2_max"] = round(self._vo2_max_value, 1)
            else:
                print(f"  — VO2 Max not found in {entry['name']}")

        return self
