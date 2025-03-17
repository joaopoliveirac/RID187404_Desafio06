# Pipeline de dados com Python

## Introdução
Na era da transformação digital, dados precisos são essenciais para empresas como a "DncInsight Solutions", especializada em análise e processamento de dados. A empresa enfrenta desafios com a qualidade e organização dos dados recebidos, muitas vezes inconsistentes e incompletos. Para resolver isso, "DncInsight Solutions" iniciou um desafio interno para desenvolver um sistema robusto e automatizado para o processamento de dados.

Como engenheiro de dados na "DncInsight Solutions", eu fui responsável por desenvolver um pipeline de dados usando Apache Airflow. Este pipeline transformará dados brutos em insights valiosos através de um processo que inclui a limpeza e agregação de dados. Diferentemente da abordagem tradicional com AWS S3, você simulará um ambiente de produção usando pastas locais para armazenamento de dados.

## Por que esse projeto foi desenvolvido?
O projeto foi desenvolvido para resolver o problema de inconsistência e falta de organização nos dados recebidos pela "DncInsight Solutions". Com a crescente quantidade de dados provenientes de diferentes fontes, a empresa precisava de uma solução escalável e eficiente para processar e transformar esses dados em informações úteis. Através da automação do pipeline de dados com Apache Airflow, o objetivo é garantir que os dados sejam limpos, transformados e organizados de maneira consistente, permitindo que as equipes de análise possam gerar insights precisos e rápidos para suportar a tomada de decisões estratégicas.

A utilização do Airflow, Docker e Python, junto com o Pandas para processamento e transformação, permite criar um ambiente controlado e isolado para o processamento de dados, com alta flexibilidade e escalabilidade. A automação do processo, juntamente com o armazenamento local, simula um ambiente de produção de forma eficiente e custo-efetiva, atendendo às necessidades da empresa sem a dependência de grandes plataformas em nuvem, como a AWS.

O resultado esperado é uma solução robusta e otimizada, que não só facilita a análise de dados, mas também melhora a qualidade das informações que alimentam as decisões estratégicas da empresa.

## Etapas do projeto

### 1 - Configuração do ambiente

Instalação do astromer airflow [Astronomer install](https://www.astronomer.io/docs/astro/cli/install-cli)

### 2 - Criação da pipeline
1. Upload de Dados Brutos (Bronze)
- Objetivo: Carregar os dados brutos de um arquivo CSV para a camada de dados Bronze.
- Processo: O arquivo CSV é lido a partir de uma pasta específica (definida pelo caminho no código) e salvo na pasta de dados "bronze", gerando um arquivo dados_bronze.csv.

2. Processamento de Dados da Camada Bronze para a Camada Silver
- Objetivo: Limpar e transformar os dados brutos na camada Silver, removendo dados inválidos e realizando ajustes nos valores.
- Processo:
Remoção de registros com valores nulos (dropna).
Conversão de campos de data para o formato datetime (date_of_birth e signup_date).
Normalização do formato de e-mails para garantir que todos tenham um domínio no formato adequado.
Cálculo da idade com base na data de nascimento (date_of_birth).
Resultado: Um arquivo CSV transformado e limpo é gerado na pasta "silver" com o nome dados_silver.csv.

3. Processamento de Dados da Camada Silver para a Camada Gold
- Objetivo: Agregar e classificar os dados, criando uma visão mais detalhada e analisável dos dados para a camada Gold.
- Processo:
Criação de faixas etárias com base na idade calculada, dividindo os dados em intervalos de 10 anos (0-10, 11-20, etc.).
Agrupamento dos dados com base na faixa etária e no status de inscrição (subscription_status), com a contagem de registros em cada grupo.
Resultado: Dois arquivos são gerados na camada Gold:
dados_gold.csv, contendo os dados transformados.
dados_agrupados.csv, contendo os dados agrupados com a quantidade de registros em cada faixa etária e status de inscrição.

4. Armazenamento e Organização
- Objetivo: Organizar os dados processados em camadas distintas (Bronze, Silver e Gold) para facilitar o gerenciamento e a análise.
- Processo: Os dados são armazenados em pastas específicas para cada camada, seguindo uma estrutura hierárquica de dados.
Essas etapas formam um pipeline de dados simples que segue o conceito de data lake com camadas (Bronze, Silver e Gold), permitindo processar, transformar e organizar os dados de forma eficiente.

### 3- Criação da DAG
- Objetivo: Definir a estrutura da DAG (Directed Acyclic Graph) para orquestrar o pipeline de dados.
- Processo:
A DAG é nomeada como pipeline com a descrição pipeline_csv e um horário de início em 2025-03-17. A DAG está configurada para rodar a cada minuto com o agendamento "* * * * *", sem realizar "catchup" (não executa tarefas para datas passadas).
A DAG contém três tasks principais que representam os processos de transformação dos dados (Bronze, Silver e Gold).

### 4- Definição das tasks
- Task de Upload de Dados Brutos para a Camada Bronze:
- Objetivo: Carregar os dados brutos para a camada Bronze.
- Processo: A função upload_raw_data_to_bronze é chamada com o arquivo raw_data.csv.
A task é registrada com o task_id='bronze'.
Dependência: Esta task precisa ser concluída antes que a task da camada Silver seja iniciada.

- Task de Processamento da Camada Bronze para a Camada Silver:
- Objetivo: Limpar e transformar os dados na camada Silver.
- Processo: A função process_bronze_to_silver é chamada com o arquivo dados_bronze.csv.
A task é registrada com o task_id='silver'.
Dependência: Esta task depende da execução bem-sucedida da task de upload de dados brutos (task Bronze).

- Task de Processamento da Camada Silver para a Camada Gold:
- Objetivo: Agregar e classificar os dados na camada Gold.
- Processo: A função process_silver_to_gold é chamada com o arquivo dados_silver.csv.
A task é registrada com o task_id='gold'.
Dependência: Esta task depende da execução bem-sucedida da task da camada Silver.

- Definição das Dependências entre as Tasks
- A execução das tasks segue uma ordem específica:
A task t1 (Bronze) deve ser concluída antes da execução da task t2 (Silver).
A task t2 (Silver) deve ser concluída antes da execução da task t3 (Gold).
Isso é configurado através do operador >>, que define a sequência de execução das tasks: t1 >> t2 >> t3.

- Execução da DAG
A DAG é executada com a chamada final pipeline(), que inicia a orquestração do fluxo de dados.
Essas etapas configuram a DAG e suas tasks dentro do Apache Airflow, garantindo que o pipeline de dados seja executado de forma organizada, com cada etapa dependendo da conclusão da anterior.

## Conclusão
Este projeto de pipeline de dados, utilizando Apache Airflow, Docker, Python e Pandas, permitiu a construção de uma solução robusta para a transformação e processamento de dados em diferentes camadas (Bronze, Silver e Gold). A automação do fluxo de dados, desde o carregamento de dados brutos até a criação de insights mais profundos e estruturados, garantiu não apenas a eficiência do processo, mas também a consistência e qualidade das informações.

Através da utilização de uma DAG no Airflow, conseguimos orquestrar e controlar o fluxo de execução das tasks, garantindo que cada etapa fosse realizada de maneira sequencial e no momento certo. A escolha de ferramentas como Pandas para o processamento e Docker para isolar o ambiente de execução contribuiu para a escalabilidade e flexibilidade da solução.

O pipeline desenvolvido neste projeto demonstra a importância de processos automatizados e bem estruturados para transformar dados brutos em informações valiosas que podem ser utilizadas para tomada de decisões estratégicas. Com o Airflow, a solução se torna ainda mais eficiente e fácil de manter, permitindo a realização de ajustes e melhorias contínuas no processamento de dados à medida que a necessidade de novos insights cresce.

## Como Executar o Projeto

Antes de executar o projeto, você precisa ter o Docker Compose instalado [Como instalar Docker Compose](https://docs.docker.com/compose/install/) e o Astronomer CLI(airflow) [Como instalar o Astronomer CLI](https://www.astronomer.io/docs/astro/cli/install-cli).

### 1- Clonar o repositório
Clone o repositório para sua máquina local:

```bash
git clone https://github.com/joaopoliveirac/RID187404_Desafio06
```


### 2- Acessar o repositório do projeto
Após clonar o repositório, entre no diretório do projeto:

```bash
cd RID187404_Desafio06
```

### 3- Iniciar o Astronomer CLI
Estando na pasta do projeto, rodar o seguinte comando para iniciar:

```bash
astro dev start
```

Isso irá subir o container do projeto no seu Docker e permitir o acesso ao [Airflow](localhost:8080) para acompanhar a execução da pipeline.