
# Boas-vindas

Se você chegou até aqui, é porque se interessou em saber mais sobre o projeto. Este arquivo tem duas partes: Os meus passos e dicas para você conseguir usá-lo, e as instruções padrões da Astronomer.

### Projeto

Aqui, nós temos uma aplicação que faz todo o processo de ETL acerca do clima das cidades do Vale do Paraíba, São Paulo e Recife. Além disso, trás informações sobre distâncias e melhores rotas para viajar entre municípios. Os *jobs* rodam a cada uma hora, e eram mais de 1500 rotas calculadas, então, por fins de construção, apenas informações de três caminhos estão disponívels: `Recife` -> `São Paulo`, `Recife` -> `São José dos Campos` e `São Paulo` -> `São José dos Campos`.

Esses processo alimenta um banco de dados que é consumido na aplicação da **Zebrinha Azul**, que você pode conferir [aqui](https://zebrinha-azul-dash-app.onrender.com/).

O **Airflow** é bem conhecido para orquestração de pipelines de dados. Ele tem como base as chamas DAGs, que são tarefas que rodam automaticamente. Aqui, além do Airflow, utilizamos o `Astro SDK` para construir e gerenciar nosso ambiente. O Astro facilita principalmente nas tarefas de trocar fontes e destinos de dados, além de acelerar a interação entre *tasks*.

Temos duas DAGs principais:

- `database_pipeline.py`: Gerencia o funcionamento e garante que o banco de dados esteja sempre disponível.
- `etl_pipeline.py`: Que condensa todas as operações de extração, transformação, validação e carregamento dos dados para o banco. É o core do projeto.

Foram feitos pequenos testes para garantir a qualidade dos dados utilizando `great-expectations`. Eles rodam em todos os arquivos gerados automaticamente, assim que são coletados das **APIs** e depois do processo de transformação, antes das informações serem carregadas no banco.

**Estrutura**

```
├───.astro
├───dags
│   └───src
│       ├───data
│       ├───etl
│       │   ├───operators
│       │   │   ├───extractors
│       │   │   ├───loaders
│       │   │   │   ├───database
│       │   │   │   ├───mapper
│       │   │   ├───transformers
│       │   ├───sql
│       └───validators
│           └───validation_assets
│               └───cols
├───include
|   └...
├───plugins
└───tests
    └───dags
```

A disponibilização de pastas do repositório foi feita para ser bem modular e tornar independentes as funções de etl e validação. É complicado fazer dags rodarem scripts externos de python, então tive que alocar tudo dentro da pasta.

As pastas `include` e `tests` são dependências do próprio **Astro SDK**. Também há um ambiente `great-expectations` no projeto, mas optei por construir os validadores do `ge` na pasta `validators`.

### Futuras melhorias

Pela falta de tempo em concluir o projeto, dá para perceber que algumas coisas não estão totalmente otimizadas. Apesar dos pipelines estarem consistentes, muitos parâmetros nas funções (Principalmente de diretórios), podem ser otimizados.

No final do desenvolvimento, percebi que havia uma inconsistência nas saídas de dados numéricos em uma das APIs. Isso foi tratado e passado para a etapa de **transformação**, mas seria bom incluir esse caso nas validações do *great-expectations.*

Criar uma DAG que avisa por e-mail quando alguma das validações der errado.

Código sempre pode ser refatorado. A ideia é deixá-lo cada vez mais limpo.

HOSPEDAR NA ASTRONOMER NÉ :D

***EDIT***: *Já está hospedado. Positivo e operante 24/7 :p*

## Recomendações para a Instalação

- Eu utilizei um banco de dados Redshift, WeatherApi e a Api de Mapas da Google. Você precisará configurar variáveis de ambiente para usá-los. Os campos necessários são:

    - ``PYTHONPATH``='usr/local/airflow' (Recomendo deixar desse exato jeito porque é bem complicado mexer com dependências no ambiente Airflow)
 
    **Credenciais do Redshift que você pega na AWS**
    - ``REDSHIFT_HOST`` 
    - ``REDSHIFT_PORT``
    - ``REDSHIFT_DBNAME``
    - ``REDSHIFT_USER``
    - ``REDSHIFT_PASSWORD``

    **Outros**
    - ``REDSHIFT_CONN_ID`` - Essa aqui é o nome da conexão que você vai criar no Airflow UI. A aplicação se conecta com o redshift por ela para rodar a DAG de criação de tabelas

    - ``WEATHER_API_KEY`` - Chave da [WeatherAPI](https://www.weatherapi.com/), utilizada nesse projeto.
    - ``DIRECTIONS_API_KEY`` - Chave da [API Directions do Google](https://developers.google.com/maps/documentation/directions/overview)
- Você também tem que ter o Python na sua máquina para iniciar o ambiente com `astro dev init`, além do **Docker Desktop**
- Todos os arquivos `.csv` são gerados pelas dags, com exceção do `municipios.csv`, que eu adaptei manualmente porque os disponíveis na internet continuam erros.

Tutorial da Astro aí embaixo. Flw 🚀

========

Overview
========

Welcome to Astronomer! This project was generated after you ran 'astro dev init' using the Astronomer CLI. This readme describes the contents of the project, as well as how to run Apache Airflow on your local machine.

Project Contents
================

Your Astro project contains the following files and folders:

- dags: This folder contains the Python files for your Airflow DAGs. By default, this directory includes two example DAGs:
    - `example_dag_basic`: This DAG shows a simple ETL data pipeline example with three TaskFlow API tasks that run daily.
    - `example_dag_advanced`: This advanced DAG showcases a variety of Airflow features like branching, Jinja templates, task groups and several Airflow operators.
- Dockerfile: This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. If you want to execute other commands or overrides at runtime, specify them here.
- include: This folder contains any additional files that you want to include as part of your project. It is empty by default.
- packages.txt: Install OS-level packages needed for your project by adding them to this file. It is empty by default.
- requirements.txt: Install Python packages needed for your project by adding them to this file. It is empty by default.
- plugins: Add custom or community plugins for your project to this file. It is empty by default.
- airflow_settings.yaml: Use this local-only file to specify Airflow Connections, Variables, and Pools instead of entering them in the Airflow UI as you develop DAGs in this project.

Deploy Your Project Locally
===========================

1. Start Airflow on your local machine by running 'astro dev start'.

This command will spin up 4 Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Webserver: The Airflow component responsible for rendering the Airflow UI
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- Triggerer: The Airflow component responsible for triggering deferred tasks

2. Verify that all 4 Docker containers were created by running 'docker ps'.

Note: Running 'astro dev start' will start your project with the Airflow Webserver exposed at port 8080 and Postgres exposed at port 5432. If you already have either of those ports allocated, you can either [stop your existing Docker containers or change the port](https://docs.astronomer.io/astro/test-and-troubleshoot-locally#ports-are-not-available).

3. Access the Airflow UI for your local Airflow project. To do so, go to http://localhost:8080/ and log in with 'admin' for both your Username and Password.

You should also be able to access your Postgres Database at 'localhost:5432/postgres'.

Deploy Your Project to Astronomer
=================================

If you have an Astronomer account, pushing code to a Deployment on Astronomer is simple. For deploying instructions, refer to Astronomer documentation: https://docs.astronomer.io/cloud/deploy-code/

Contact
=======

The Astronomer CLI is maintained with love by the Astronomer team. To report a bug or suggest a change, reach out to our support.
