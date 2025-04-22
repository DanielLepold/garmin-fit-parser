import zipfile
import io
from typing import Optional


def extract_fit_stream(fit_data: bytes) -> Optional[io.BytesIO]:
  """
  Extracts and returns a BytesIO stream of the .fit file from the given data.
  If not a zip, returns the raw data wrapped in BytesIO.
  """
  if zipfile.is_zipfile(io.BytesIO(fit_data)):
    with zipfile.ZipFile(io.BytesIO(fit_data)) as z:
      for zip_info in z.infolist():
        if zip_info.filename.endswith(".fit"):
          with z.open(zip_info) as extracted_file:
            return io.BytesIO(extracted_file.read())
  else:
    return io.BytesIO(fit_data)

  return None
