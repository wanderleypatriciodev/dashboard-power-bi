import mysql.connector
import random
from datetime import datetime, timedelta

def gerar_massa_de_dados():
    # 1. Configurar a conexão com o seu MySQL local
    # Ajuste o 'user' e 'password' conforme as credenciais da sua máquina
    config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '',
        'database': 'bi_supermercado_mossoro'
    }

    try:
        conexao = mysql.connector.connect(**config)
        cursor = conexao.cursor()
        print("Conectado ao MySQL com sucesso!")

        # 2. Definições para a simulação de dados aleatórios
        # IDs que inserimos manualmente nas tabelas de dimensão
        ids_lojas = [1, 2, 3]  # Nova Betânia, Alto de São Manoel, Centro
        
        # Dicionário mapeando o id_produto ao seu preço de venda aproximado
        # { id_produto: preco_venda }
        produtos_precos = {
            1: 5.99,   # Melão Tipo Exportação
            2: 7.50,   # Arroz Integral
            3: 8.90,   # Feijão Carioca
            4: 2.30    # Detergente
        }

        # Configuração do intervalo de datas (últimos 365 dias até hoje)
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=365)

        vendas_para_inserir = []
        total_registros = 10000

        print(f"Gerando {total_registros} registros de vendas simuladas...")

        # 3. Loop para criar os dados na memória do Python
        for _ in range(total_registros):
            # Gera uma data aleatória dentro do intervalo
            dias_aleatorios = random.randint(0, 365)
            data_venda = (data_inicio + timedelta(days=dias_aleatorios)).strftime('%Y-%m-%d')
            
            id_loja = random.choice(ids_lojas)
            id_produto = random.choice(list(produtos_precos.keys()))
            
            # Define uma quantidade de itens comprados aleatória (de 1 a 10 unidades)
            quantidade = random.randint(1, 10)
            valor_unitario = produtos_precos[id_produto]

            # Adiciona a linha na nossa lista de lote
            vendas_para_inserir.append((data_venda, id_produto, id_loja, quantidade, valor_unitario))

        # 4. Inserção em lote (Bulk Insert) para alta performance
        query_insert = """
            INSERT INTO fato_vendas (data_venda, id_produto, id_loja, quantidade, valor_unitario) 
            VALUES (%s, %s, %s, %s, %s)
        """
        
        # Executa de mil em mil para não sobrecarregar a memória
        tamanho_lote = 1000
        for i in range(0, len(vendas_para_inserir), tamanho_lote):
            lote = vendas_para_inserir[i:i + tamanho_lote]
            cursor.executemany(query_insert, lote)
            conexao.commit()
            print(f"Progresso: {i + len(lote)} / {total_registros} registros inseridos.")

        print("\nSucesso total! 10.000 vendas inseridas na tabela fato_vendas.")

    except mysql.connector.Error as erro:
        print(f"Erro ao interagir com o banco de dados: {erro}")
        
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
            print("Conexão com o banco de dados encerrada.")

if __name__ == "__main__":
    gerar_massa_de_dados()
