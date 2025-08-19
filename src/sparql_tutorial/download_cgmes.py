import argparse
import io
import logging
import zipfile
from pathlib import Path

import httpx

data = {
    "docs": "https://www.entsoe.eu/Documents/CIM_documents/Grid_Model_CIM/ENTSOE_CGMES_v2.4.15_7Aug2014_HTML.zip",
    "test_data":  "https://www.entsoe.eu/Documents/CIM_documents/Grid_Model_CIM/TestConfigurations_packageCASv2.0.zip"
}

parser = argparse.ArgumentParser()
parser.add_argument("which", choices=data)
parser.add_argument("--output", "-o", type=Path, required=True)
args = parser.parse_args()

logger = logging.Logger("download_data")
logger.setLevel(level=logging.INFO)
logging.basicConfig(level=logging.INFO)

resp = httpx.get(data[args.which], follow_redirects=True)
resp.raise_for_status()
logger.info("Extracting data to '%s'...", args.output)
zipfile.ZipFile(io.BytesIO(resp.content)).extractall(args.output)

logger.info("Looking for zip files to extract (in case there are zipped zip-files):")
for file in Path(args.output).glob("**/*.zip"):
    logger.info("Extracting data from '%s'...", file)
    with file.open("rb") as f:
        zipfile.ZipFile(f).extractall(file.parent / file.stem)
