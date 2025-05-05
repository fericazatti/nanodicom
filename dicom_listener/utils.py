# dicom_listener/utils.py

import os
import zipfile
import shutil
import requests
from pathlib import Path
import logging
from .config import get_config

logger = logging.getLogger("OMNIQA-DICOM")
CONFIG = get_config()

def zip_and_optionally_send(study_uid, file_list):
    zip_path = Path(CONFIG["DICOM_ZIP_OUTPUT_PATH"]) / f"{study_uid}.zip"
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            for file in file_list:
                arcname = Path(file).name
                zf.write(file, arcname=arcname)
        logger.info(f"ZIP generado: {zip_path}")
    except Exception as e:
        logger.error(f"Error al generar ZIP: {e}")
        return

    if CONFIG["DICOM_SEND_TO_API"] and CONFIG["DICOM_API_URL"]:
        try:
            with open(zip_path, 'rb') as f:
                files = {'file': (zip_path.name, f, 'application/zip')}
                if CONFIG["DICOM_API_METHOD"].upper() == "POST":
                    response = requests.post(CONFIG["DICOM_API_URL"], files=files)
                else:
                    response = requests.put(CONFIG["DICOM_API_URL"], files=files)

            if response.status_code == 200:
                logger.info("Archivo ZIP enviado correctamente a la API")
            else:
                logger.warning(f"Fallo al enviar a API: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error enviando ZIP a la API: {e}")
