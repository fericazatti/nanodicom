# OMNIQA DICOM Listener

Este proyecto implementa un **servidor DICOM SCP** utilizando `pynetdicom`, que recibe archivos DICOM, los guarda en disco y opcionalmente comprime el estudio en un `.zip` para enviarlo a una API externa.

---

## 📦 Requisitos

- Docker
- Archivo `.env` en la raíz del proyecto
- Estructura de carpetas como se indica más abajo

---

## ⚙️ Archivo `.env` (ejemplo)

```env
# DICOM listener
DICOM_AET=TEST
DICOM_PORT=11112
DICOM_TIMEOUT=15

# Ruta de almacenamiento local
DICOM_STORAGE_PATH=/app/data/dicom
DICOM_ZIP_OUTPUT_PATH=/app/data/zips

# Envío opcional a API
DICOM_SEND_TO_API=true
DICOM_API_URL=http://localhost:5000/api/upload/upload
DICOM_API_METHOD=POST
```

> 🧠 Si `DICOM_SEND_TO_API=false`, el listener simplemente guardará el archivo `.zip` y no intentará conectarse a ninguna API.

---

## 🐳 Docker

### 1. Crear imagen

Se crea a partir del arhchivo `Dockerfile`:

Y luego construir la imagen con:

```bash
docker build -t dicom-listener .
```

---

### 2. Ejecutar contenedor

```bash
docker run -d \
  --name dicom-listener \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/data:/app/data \
  -p 11112:11112 \
  dicom-listener
```

- Monta el archivo `.env` de configuración.
- Monta `./data` del host como `/app/data` en el contenedor.
- Expone el puerto 11112 para asociaciones DICOM.

---

## 📂 Estructura de directorios sugerida

```
omniqa_api/
├── dicom_listener/
│   ├── __main__.py
│   ├── config.py
│   ├── listener.py
│   ├── utils.py
├── data/
│   ├── dicom/      # Archivos DICOM temporales
│   └── zips/       # Archivos ZIP de salida
├── .env
├── Dockerfile
├── requirements.txt
```

---

## ✅ Logs esperados

Cuando se recibe una imagen correctamente, deberías ver algo como:

```
INFO:OMNIQA-DICOM:Recibido: /app/data/dicom/<study_uid>/<image_uid>.dcm
INFO:OMNIQA-DICOM:ZIP generado: /app/data/zips/<study_uid>.zip
```

Y si `DICOM_SEND_TO_API=true`:

```
INFO:OMNIQA-DICOM:Archivo enviado exitosamente a la API
```