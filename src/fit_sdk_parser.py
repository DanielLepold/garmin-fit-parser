from garmin_fit_sdk import Decoder, Stream
import fit_reader

class Parser:
    def __init__(self, input_list: list[dict]):
        self.input_list:  list[dict] = input_list
        self.vo2_max_value = 0

    def _mesg_listener(self, mesg_num, message):
      if mesg_num == 140:
        if 7 in message:
          raw_value = message[7]
          self.vo2_max_value  = raw_value * 3.5 / 65536

    def parse_vo2_max_values(self):
      for entry in self.input_list:
        self.vo2_max_value = 0  # reset before each file

        print(f"📂 Processing: {entry['name']}")
        fit_bytes_io = fit_reader.extract_fit_stream(entry["data"])
        stream = Stream.from_bytes_io(fit_bytes_io)
        decoder = Decoder(stream)
        _, errors = decoder.read(mesg_listener=self._mesg_listener)
        stream.close()

        if errors:
          print(f"  ⚠️ Errors while decoding {entry['name']}: {errors}")

        if self.vo2_max_value and self.vo2_max_value > 0:
          entry["vo2_max"] = self.vo2_max_value
        else:
          print(f"  ❌ VO2 Max not found or zero in {entry['path']}")

      return self

