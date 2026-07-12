import os

MODALITY_URLS = {
    "mammography": os.environ.get("MAMMOGRAPHY_URL", "http://mammography:8000"),
    "histopathology": os.environ.get("HISTOPATHOLOGY_URL", "http://histopathology:8000"),
    "genomics": os.environ.get("GENOMICS_URL", "http://genomics:8000"),
}
FUSION_URL = os.environ.get("FUSION_URL", "http://fusion:8000")
