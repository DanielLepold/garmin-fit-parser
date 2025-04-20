from garmin_fit_sdk import Decoder, Stream
import fit_reader

class Parser:
    """
    A class to parse .fit file data and extract VO2 Max values from Garmin activity files.

    Attributes:
        input_list (list[dict]): A list of dictionaries representing activities.
                                 Each dictionary should contain keys such as 'name', 'data', and optionally 'path'.
        vo2_max_value (float): Temporary storage for the extracted VO2 Max value during parsing.
    """

    def __init__(self, input_list: list[dict]):
        """
        Initializes the Parser with a list of input activity data.

        Args:
            input_list (list[dict]): List of activities with keys such as 'name' and 'data'
                                     where 'data' is the in-memory binary content of a .fit file.
        """
        self.input_list: list[dict] = input_list
        self.vo2_max_value = 0

    def _mesg_listener(self, mesg_num: int, message: dict):
        """
        Internal callback method used during decoding to listen for VO2 Max messages.

        Args:
            mesg_num (int): The message type number from the FIT protocol.
            message (dict): The message content dictionary.
        """
        if mesg_num == 140:  # 140 = VO2 Max message
            if 7 in message:  # Field 7 = VO2 Max raw value
                raw_value = message[7]
                self.vo2_max_value = raw_value * 3.5 / 65536  # Convert raw to VO2 Max

    def parse_vo2_max_values(self):
        """
        Parses all input .fit data entries and extracts VO2 Max values using the SDK.

        Updates each entry in `self.input_list` by adding a new key `vo2_max` with the extracted value.

        Returns:
            Parser: Returns self to allow method chaining.
        """
        for entry in self.input_list:
            self.vo2_max_value = 0  # Reset before parsing each file

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
                print(f"  ❌ VO2 Max not found or zero in {entry.get('path', entry['name'])}")

        return self
