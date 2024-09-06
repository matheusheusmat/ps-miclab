# Processo Seletivo MICLab
**Candidato: Matheus Hencklein Ponte**<br>
**E-mail: m247277@dac.unicamp.br**<br><br>
Prezada Prof. Letícia Rittner,<br>

Consegui resolver os desafios da fase do processo seletivo. Minha maior dificuldade foi por conta de utilizar o Docker, uma plataforma que nunca utilizei antes e, por isso, pode ser que o arquivo Dockerfile apresente problemas. Peço desculpas por isso<br>

Apesar disso, com auxílio do Microsoft Copilot e do ChatGPT, consegui baixar o Docker Desktop e, utilizando WSL no VSCode, comecei a resolução das tarefas. <br>

### Tarefa 1
Para baixar e configurar o PACs OrthanC, executei o comando no bash:<br>

`docker pull orthancteam/orthanc`<br>

Aprendi que "orthanc" se trata de uma imagem pronta do OrthanC-server no Docker. Depois, rodei no terminal:<br>

`docker run -p 4242:4242 -p 8042:8042 --rm orthancteam/orthanc`<br>

Assim, acessando a porta 8042 no navegador, http://localhost:8042, com o usuário e senha `orthanc`, executei a interface do PACs OrthanC.

### Tarefa 2
Ao acessar a interface do OrthanC via navegador e clicar em "All Studies", não há estudos na lista. Precisamos adicionar os arquivos .dcm usando um script Python que usa a API REST.<br>

Aprendi, nessa parte, que os parâmetros `ORTHANC_URL`, `ORTHANC_USERNAME`, `ORTHANC_PASSWORD`, `DICOM_DIRECTORY` fazem parte da API REST e devem ser utilizadas para definir, respectivamente, para onde fazer o upload das imagens, o nome e a senha para acesso à plataforma, e o diretório local onde cada estudo localiza-se. O restante do código percorre os arquivos DICOM e os envia ao OrthanC-server, por meio de uma requisição.<br>

Ao executarmos `python3 send_dicom.py` no terminal WSL, os cinco estudos da pasta "dicom_samples" aparecem na aba "All Studies".

### Tarefa 3
A tarefa 3 exige que sejam gerados arquivos `.json` que contenham os resultados do TorchXRayVision. Dividi a tarefa em dois arquivos:<br>

- O primeiro arquivo, `generate_results_and_sreports.py`, itera sobre cada um dos arquivos DICOM em dicom_samples e, ao chamar read_xray_dcm, os transforma em um array de píxeis. Sobre esse array é aplicado o modelo de deep learning do TorchXRayVision, que constrói um dicionário do Python com os parâmetros encontrados, que entendi ser a probabilidade do paciente ter alguma das complicações apresentadas. Ao final, imprime o dicionário e o salva em formato `.json` na pasta "json_results". <br>

- O segundo arquivo, `read_xray_dicom`, contém a função `read_xray_dcm` que, dado o caminho de um arquivo .dcm, retorna um array de píxeis.<br>

Basta, então, executar `python3 generate_results_and_sreports.py` no terminal do WSL para que os `.json` sejam gerados. **Atenção:**ambas as tarefas 3 e 4 são feitas quando o comando é executado.

### Tarefa 4
Por fim, a tarefa 4 abordou a construção de um DICOM Structured Report a partir de uma imagem DICOM e o seu envio ao PACS OrthanC. Novamente, dividi em dois arquivos:<br>
- O primeiro arquivo, `generate_results_and_sreports.py`, na mesma iteração que gera o `.json` de cada arquivo, também gera o seu SR. Para isso, chama a função `create_dicom_sr` e, em seguida, envia o arquivo criado ao servidor OrthanC, chamando `send_to_pacs`.
- O segundo arquivo, `sr_create_send.py`, possui duas funções: `create_dicom_sr` lê, para cada caminho de arquivo DICOM, seus metadados, incluindo nome de paciente, estudo e série atual, e o adiciona no SR, salvando na pasta `dicom_structured_reports`; e `send_to_pacs` envia o SR para o PACS, usando a API REST. 
Nessa parte, tive alguns problemas, com o servidor retornando o erro 400, que estudei e, lançando mão da ferramenta `dciodvfy` do toolkit `dicom3tools`, como li na documentação, descobri ser o campo do SR "SOPClassUID" mal-formatado. Após refatorações em `create_dicom_sr`, funcionou, e os reports apareceram no OrthanC.

### Construção do Dockerfile
Após testar os scripts e garantir sua funcionalidade com a imagem já pronta, tentei construir minha própria imagem Docker, como está descrito no arquivo, utilizando o orthancteam/orthanc como base e adicionando os arquivos e dependências.<br>

Ao se fazer um request, o erro "Connection Refused" aparece, que pesquisei ser falta de comunicação entre o script e o OrthanC. Mesmo refatorando o arquivo Dockerfile diversas vezes, infelizmente não funcionou.

### Considerações finais
Aplicar o modelo pré-treinado sobre imagens DICOM para gerar predições em imagens radiográficas foi, no meu ponto de vista, uma ótima experiência e espero aprender mais sobre no MICLab. Agradeço a oportunidade e espero progredir para a próxima fase do processo!







