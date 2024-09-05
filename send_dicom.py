import os
import requests

# Configurações
ORTHANC_URL = "http://localhost:8042/instances"
ORTHANC_USERNAME = "orthanc"
ORTHANC_PASSWORD = "orthanc"
DICOM_DIRECTORY = "/home/matt/dicom_samples"  # Caminho para a pasta com os arquivos DICOM

def send_dicom(file_path):
    with open(file_path, 'rb') as f:
        response = requests.post(
            ORTHANC_URL,
            auth=(ORTHANC_USERNAME, ORTHANC_PASSWORD),
            files={'file': f}
        )
        return response.status_code, response.text

def main():
    for root, dirs, files in os.walk(DICOM_DIRECTORY):
        for file in files:
            if file.endswith(".dcm"):
                file_path = os.path.join(root, file)
                status_code, response_text = send_dicom(file_path)
                print(f"Enviando {file_path}: {status_code} - {response_text}")

if __name__ == "__main__":
    main()
