# Processo Seletivo MICLab
**Candidato: Matheus Hencklein Ponte**<br>
**E-mail: m247277@dac.unicamp.br**<br><br>
Prezada Prof. Letícia Rittner,<br>

Consegui resolver os desafios da fase do processo seletivo. Minha maior dificuldade foi por conta de utilizar o Docker, uma plataforma que nunca utilizei antes e, por isso, não consegui colocar o arquivo Dockerfile nesse repositório, pois procurei no repositório orthancteam/orthanc no DockerHub, mas não encontrei.<br>

Apesar disso, com auxílio da ferramenta de IA Microsoft Copilot, consegui baixar o Docker Desktop e, utilizando WSL no VSCode, comecei a resolução das tarefas. <br>

### Tarefa 1
Para baixar e configurar o PACs OrthanC, executei o comando no bash:<br>

`docker pull orthancteam/orthanc`<br>

Aprendi que "orthanc" se trata de uma imagem pronta do OrthanC-server no Docker. Depois, rodei no terminal:<br>

`docker run -p 4242:4242 -p 8042:8042 --rm orthancteam/orthanc`<br>

Assim, acessando a porta 8042 no navegador, http://localhost:8042, executei a interface do PACs OrthanC.

### Tarefa 2
Ao acessar a interface do OrthanC via navegador e clicar em "All Studies", não há estudos na lista. Precisamos adicionar os arquivos .dcm usando um script Python que usa a API REST.<br>

Aprendi, nessa parte, que os parâmetros `ORTHANC_URL`, `ORTHANC_USERNAME`, `ORTHANC_PASSWORD`, `DICOM_DIRECTORY` fazem parte da API REST e devem ser utilizadas para definir, respectivamente, para onde fazer o upload das imagens, o nome e a senha para acesso à plataforma, e o diretório local onde cada estudo localiza-se. O restante do código percorre os arquivos DICOM e os envia ao OrthanC-server, por meio de uma requisição.<br>

Após esse passo, cinco estudos aparecem na aba "All Studies".

### Tarefa 3





