import read_xray_dicom as rxd
import os
import torchxrayvision as xrv
import torch, torchvision
import json
import sr_create_send as scs


def main():
    # Caminho para a pasta que contém os arquivos DICOM
    dicom_folder = "dicom_samples"

    json_results_folder = "json_results"
    dicom_sr_folder = "dicom_structured_reports"

    # Criar a pasta json_results se não existir
    os.makedirs(json_results_folder, exist_ok=True)

    # Criar a pasta dicom_structured_reports se não existir
    os.makedirs(dicom_sr_folder, exist_ok=True)

    # Listar todos os arquivos DICOM na pasta e subpastas
    dicom_files = []
    for root, dirs, files in os.walk(dicom_folder):
        for file in files:
            if file.endswith(".dcm"):
                dicom_files.append(os.path.join(root, file))

    idx = 1
    # Percorrer os arquivos DICOM e ler cada um
    for dicom_file in dicom_files:
        print(f"Lendo arquivo: {dicom_file}")
        img = rxd.read_xray_dcm(dicom_file)
            # Adicionar uma dimensão para o canal de cor
        img = img[None, ...]

        # Transformações necessárias
        transform = torchvision.transforms.Compose([
            xrv.datasets.XRayCenterCrop(),
            xrv.datasets.XRayResizer(224)
        ])

        # Aplicar as transformações
        img = transform(img)
        img = torch.from_numpy(img)

        # Carregar o modelo pré-treinado
        model = xrv.models.DenseNet(weights="densenet121-res224-all")

        # Fazer a predição
        outputs = model(img[None, ...])

        # Imprimir os resultados
        resultados = dict(zip(model.pathologies, outputs[0].detach().numpy()))
        resultados = {k: float(v) for k, v in resultados.items()}
        print(resultados)

        # Salvar os resultados em um arquivo JSON
        json_path = os.path.join(json_results_folder, f"result{idx}.json")
        
        with open(json_path, 'w') as json_file:
            json.dump(resultados, json_file, indent=4)
        print(f"Resultados salvos em {json_path}")

        # Gerar os Structured Reports
        dicom_sr_path = os.path.join(dicom_sr_folder, f"report{idx}.dcm")
        scs.create_dicom_sr(dicom_file, resultados, dicom_sr_path)

        # Enviar ao PACS
        scs.send_to_pacs(dicom_sr_path)

        idx += 1

if __name__ == "__main__":
    main()