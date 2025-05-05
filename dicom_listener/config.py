import os
from dotenv import load_dotenv
from pathlib import Path

# Ruta absoluta al archivo .env y su carpeta contenedora
env_path = Path(__file__).resolve().parent.parent / ".env"
base_dir = env_path.parent

# Cargar .env
load_dotenv(dotenv_path=env_path)

def resolve_path(env_var, default_subdir):
    value = os.getenv(env_var)
    if value:
        return (base_dir / value).resolve()
    else:
        return (base_dir / default_subdir).resolve()

def get_config():
    return {
        "DICOM_AET": os.getenv("DICOM_AET"),
        "DICOM_PORT": int(os.getenv("DICOM_PORT", 11112)),
        "DICOM_TIMEOUT": int(os.getenv("DICOM_TIMEOUT", 10)),
        "DICOM_STORAGE_PATH": str(resolve_path("DICOM_STORAGE_PATH", "data/dicom")),
        "DICOM_ZIP_OUTPUT_PATH": str(resolve_path("DICOM_ZIP_OUTPUT_PATH", "data/zips")),
        "DICOM_SEND_TO_API": os.getenv("DICOM_SEND_TO_API", "false").lower() == "true",
        "DICOM_API_URL": os.getenv("DICOM_API_URL"),
        "DICOM_API_METHOD": os.getenv("DICOM_API_METHOD", "POST")
    }
