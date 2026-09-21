# 🛒 Business Intelligence Dashboard - Redes de Supermercados

Este projeto consiste no desenvolvimento de uma solução de Business Intelligence (BI) ponta a ponta para a análise estratégica de faturamento, lucratividade e volume de movimentação de mercadorias. A arquitetura simula a infraestrutura de dados de uma rede de supermercados operando em três filiais estratégicas no município de MossoróRN Nova Betânia, Alto de São Manoel e Centro.

O grande diferencial do projeto está na união do perfil de desenvolvimento de software com a engenharia de dados, cobrindo desde a modelagem dimensional do banco até a ingestão automatizada por script e construção da camada de apresentação visual.

---

## 🛠️ Arquitetura do Sistema e Tecnologias

O ecossistema do projeto foi segregado em três camadas lógicas fundamentais

1.  Camada de Armazenamento e Modelagem (MySQL)
       Implementação do modelo dimensional Star Schema (Esquema Estrela) focado em performance analítica.
       Criação de tabelas estáticas de contexto (`dim_produto`, `dim_loja`) e uma tabela central de alta volumetria (`fato_vendas`).
       Desenvolvimento de uma `VIEW` analítica permanente (`vw_dashboard_vendas`) para encapsular os `JOINs` complexos e centralizar regras de cálculo de negócios direto na base, otimizando o consumo da ferramenta analítica.
       Arquivo de origem `bi_supermercado_mossoro.sql`

2.  Camada de Ingestão e Automação (Python)
       Script automatizado utilizando a biblioteca `mysql-connector-python`.
       Algoritmo programado para gerar dados sintéticos altamente realistas e realizar a inserção performática em lote (Bulk Insert) de 10.000 registros de vendas retroativos espalhados ao longo de 365 dias.
       Arquivo de origem `dados.py`

3.  Camada de Visualização de Dados (Power BI Desktop)
       Conexão integrada utilizando a ponte universal ODBC para leitura otimizada do servidor local MySQL.
       Uso de Linguagem DAX estruturada para criação de métricas de negócio dinâmicas e resilientes a erros de divisão por zero.
       Adoção de design corporativo minimalista (Clean UI) para maximizar o foco nos dados através de um plano de fundo customizado.
       Arquivo de origem `dashboard_supermercado.pbix`

---

## 📈 Inteligência de Negócio e Métricas Calculadas (DAX)

Para evitar poluição do modelo, as agregações foram resolvidas dinamicamente via medidas DAX no Power BI

   Faturamento Total Soma cumulativa do valor bruto das transações.
   Lucro Líquido Valor consolidado subtraindo o preço de custo (armazenado na dimensão) do preço final praticado na venda.
   Volume de Vendas Totalização física exata de unidades que saíram do estoque.
   Margem de Lucro (%) Métrica percentual dinâmica calculada via tratamento de exceção matemática
    ```dax
    Margem Lucro % = DIVIDE(SUM(vw_dashboard_vendas[lucro_liquido]), SUM(vw_dashboard_vendas[faturamento_total]), 0)
    ```

---

## 🖥️ Demonstração Prática do Dashboard

O layout foi concebido sob a técnica de leitura em Z, priorizando KPIs estratégicos no topo (Faturamento, Margem e Unidades), detalhamento geográfico por bairros à esquerda, distribuição por relevância de categorias à direita e auditoria operacional detalhada na base.

### 1. Visão Geral Consolidada
Exibição do ecossistema de dados completo computando o histórico total das 10.000 operações geradas pelo pipeline.
![Visão Geral](.imagesdashboard001.png)

### 2. Comportamento do Filtro Categoria Mercearia
Demonstração da reatividade da malha de gráficos ao isolar a cadeia de suprimentos da Mercearia.
![Filtro Mercearia](.imagesdashboard002.png)

### 3. Comportamento do Filtro Categoria Hortifruti
Análise focada na força regional do Hortifruti (como a produção e venda de Melão Tipo Exportação).
![Filtro Hortifruti](.imagesdashboard003.png)

### 4. Comportamento do Filtro Categoria Limpeza
Isolamento do fluxo de caixa e volumetria transacionada nos setores de produtos de limpeza das lojas.
![Filtro Limpeza](.imagesdashboard004.png)

---

## 🚀 Como Replicar este Ambiente Localmente

Como o projeto utiliza pacotes universais de programação, você pode subir toda a estrutura na sua máquina seguindo estes passos

1.  Preparação da Base Importe o script `bi_supermercado_mossoro.sql` dentro do seu gerenciador MySQL para criar o banco de dados e as views nativas.
2.  Preparação do Ambiente Python Garanta que possui o interpretador instalado e instale o driver de banco através do terminal
    ```bash
    pip install mysql-connector-python
    ```
3.  Carga dos Dados Abra o arquivo `dados.py`, insira a sua credencial local de acesso do MySQL e execute o arquivo no terminal
    ```bash
    python dados.py
    ```
4.  Consumo do Dashboard Abra o painel de ferramentas de administração do Windows chamado Fontes de Dados ODBC (64 bits), configure um DSN de Sistema apontando para o seu banco e abra o arquivo `dashboard_supermercado.pbix` no Power BI para atualizar a tela.
