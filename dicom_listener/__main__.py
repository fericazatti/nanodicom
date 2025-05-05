# omniqa_api/dicom_listener/__main__.py
from pynetdicom import AE, evt, AllStoragePresentationContexts
from dicom_listener.listener import handle_event, CONFIG

handlers = [(evt.EVT_C_STORE, handle_event)]

ae = AE(ae_title=CONFIG["DICOM_AET"])
for context in AllStoragePresentationContexts:
    ae.add_supported_context(context.abstract_syntax)

ae.start_server(('0.0.0.0', CONFIG["DICOM_PORT"]), evt_handlers=handlers)