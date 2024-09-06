import pydicom
from pydicom.dataset import Dataset, FileDataset
from datetime import datetime
from pydicom.uid import generate_uid
import requests


def create_dicom_sr(dicom_file, resultados, output_path):
    ds = pydicom.dcmread(dicom_file)
    file_meta = pydicom.Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.88.11'  # UID para SR
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

    # Criar o dataset para o SR
    sr = FileDataset(output_path, {}, file_meta=file_meta, preamble=b"\0" * 128)
    sr.is_little_endian = True
    sr.is_implicit_VR = False

    # Atributos obrigatórios
    sr.PatientID = ds.PatientID
    sr.PatientName = ds.PatientName
    sr.StudyInstanceUID = ds.StudyInstanceUID
    sr.SeriesInstanceUID = ds.SeriesInstanceUID
    sr.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
    sr.SOPClassUID = file_meta.MediaStorageSOPClassUID
    sr.ContentDate = datetime.now().strftime('%Y%m%d')
    sr.ContentTime = datetime.now().strftime('%H%M%S')
    sr.Modality = 'SR'
    sr.SeriesDescription = 'Structured Report'
    sr.SeriesNumber = 999
    sr.InstanceNumber = 1

    # Adicionar atributos obrigatórios para o SR
    sr.CompletionFlag = 'COMPLETE'
    sr.VerificationFlag = 'VERIFIED'
    sr.DocumentTitle = 'Structured Report'
    sr.ValueType = 'TEXT'

    # Estrutura do ContentSequence
    sr.ContentSequence = []
    for key, value in resultados.items():
        item = Dataset()
        item.ValueType = 'TEXT'
        item.ConceptNameCodeSequence = [Dataset()]
        item.ConceptNameCodeSequence[0].CodeValue = '121071'
        item.ConceptNameCodeSequence[0].CodingSchemeDesignator = 'DCM'
        item.ConceptNameCodeSequence[0].CodeMeaning = key
        item.TextValue = str(value)
        sr.ContentSequence.append(item)

    # Salvar o arquivo DICOM SR
    sr.save_as(output_path)
    print(f"DICOM SR salvo em {output_path}")


def send_to_pacs(dicom_sr_path):
    ORTHANC_URL = "http://localhost:8042/instances"
    ORTHANC_USERNAME = "orthanc"
    ORTHANC_PASSWORD = "orthanc"
    with open(dicom_sr_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(ORTHANC_URL, auth=(ORTHANC_USERNAME, ORTHANC_PASSWORD), files=files)
        if response.status_code == 200:
            print(f"Arquivo {dicom_sr_path} enviado com sucesso para o PACS.\n")
        else:
            print(f"Falha ao enviar {dicom_sr_path} para o PACS. Status code: {response.status_code}")
            print(f"Resposta do servidor: {response.text}")

def good_dicom(dicom_sr_path):
    try:
        ds = pydicom.dcmread(dicom_sr_path)
        print("Arquivo DICOM válido.")
        print(ds)
    except Exception as e:
        print(f"Erro ao ler o arquivo DICOM: {e}")