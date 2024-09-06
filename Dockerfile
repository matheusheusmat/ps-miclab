# Use a imagem base do Orthanc
FROM orthancteam/orthanc:latest

# Instale as dependências do sistema
USER root
RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    python3-venv \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crie um diretório para os scripts e dados
WORKDIR /app

# Copie os scripts e os arquivos DICOM para o container
COPY /ps-miclab /app

# Crie um ambiente virtual Python e ative-o
RUN python3 -m venv /env
RUN /env/bin/pip install --upgrade pip

# Instale as bibliotecas Python necessárias
RUN /env/bin/pip install torchxrayvision torch torchvision pydicom requests numpy

# Defina o comando padrão para o container
ENTRYPOINT ["/bin/bash", "-c", "/env/bin/python /app/send_dicom.py && /env/bin/python /app/generate_results_and_sreports.py || tail -f /dev/null"]
