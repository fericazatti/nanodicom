# dicom_listener/listener.py

from pynetdicom import AE, evt, AllStoragePresentationContexts
from pydicom.dataset import Dataset
from pathlib import Path
import logging
from .config import get_config
from .utils import zip_and_optionally_send
import traceback

CONFIG = get_config()

# Setup logging
logger = logging.getLogger("OMNIQA-DICOM")
logging.basicConfig(level=logging.INFO)
RECEIVED_STUDIES = {}

def handle_event(event):
    try:
        ds = event.dataset
        ds.file_meta = event.file_meta
        study_uid = ds.StudyInstanceUID
        output_path = Path(CONFIG["DICOM_STORAGE_PATH"]) / study_uid
        output_path.mkdir(parents=True, exist_ok=True)
        filename = output_path / f"{ds.SOPInstanceUID}.dcm"
        ds.save_as(str(filename), write_like_original=False)
        logger.info(f"Recibido: {filename}")
        RECEIVED_STUDIES.setdefault(study_uid, []).append(str(filename))

        # Si ya se recibió al menos una imagen, se procesa el estudio
        if len(RECEIVED_STUDIES[study_uid]) >= 1:
            zip_and_optionally_send(study_uid, RECEIVED_STUDIES[study_uid])
            traceback.print_exc()  # <--- esto mostrará la excepción completa
            RECEIVED_STUDIES.pop(study_uid, None)

        return 0x0000  # Success
    except Exception as e:
        logger.error(f"Error procesando evento C-STORE: {e}")
        return 0xC210  # Failure

def run_listener():
    ae = AE(ae_title=CONFIG["DICOM_AET"])
    ae.supported_contexts = AllStoragePresentationContexts

    handlers = [(evt.EVT_C_STORE, handle_event)]
    logger.info(f"Iniciando servidor DICOM en puerto {CONFIG['DICOM_PORT']} con AET {CONFIG['DICOM_AET']}")
    print(f"Iniciando servidor DICOM en puerto {CONFIG['DICOM_PORT']} con AET {CONFIG['DICOM_AET']}")
    ae.start_server(("0.0.0.0", CONFIG["DICOM_PORT"]), evt_handlers=handlers, block=True)
    logger.info("Servidor DICOM iniciado y escuchando...")
    print("Servidor DICOM iniciado y escuchando...")