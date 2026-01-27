import sqlite3
import os
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

def mes_normalize(m):
    ano, mes = m.split('-')
    mes_int = int(mes)
    nome_mes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    return f"{nome_mes[mes_int - 1]}/{ano}"

class ContaService():
    @staticmethod
    def criar_conta(nome_conta: str, valor: float, data_vencimento: str, session_id: int, categoria: str = None, pago: bool = False, lembrete: bool = False) -> bool:
        try:
            conn = sqlite3.connect(os.getenv("DATABASE_PATH"))
            c = conn.cursor()
            c.execute("""
                INSERT INTO conta (user_id, nome_conta, valor, data_vencimento, categoria, pago, lembrete)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (session_id, nome_conta, valor, data_vencimento, categoria, pago, lembrete))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao criar conta: {e}")
            return False
        
    
    @staticmethod
    def get_categorias_by_user(user_id: int) -> list:
        try:
            conn = sqlite3.connect(os.getenv("DATABASE_PATH"))
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT DISTINCT nome_categoria FROM categoria WHERE user_id = ?", (user_id,))
            categorias = c.fetchall()
            conn.close()
            return [dict(categoria) for categoria in categorias]
        except sqlite3.Error as e:
            conn.close()
            print(f"Erro ao buscar contas: {e}")
            return []
        
    @staticmethod
    def adicionar_categoria(session_id: int, nome_categoria: str) -> bool:
        try:
            conn = sqlite3.connect(os.getenv("DATABASE_PATH"))
            c = conn.cursor()
            c.execute("INSERT INTO categoria (user_id, nome_categoria) VALUES (?, ?)", (session_id, nome_categoria))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            conn.close()
            print(f"Erro ao adicionar categoria: {e}")
            return False
        
    @staticmethod
    def get_contas_by_user(session_id: int) -> list:
        try:
            conn = sqlite3.connect(os.getenv("DATABASE_PATH"))
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM conta WHERE user_id = ?", (session_id,))
            contas = c.fetchall()
            conn.close()
            mes = set()
            categorias = set()
            dicionario = {}

            for conta in contas:
                categorias.add(conta['categoria'])
                conta_data = datetime.strptime(conta['data_vencimento'], '%Y-%m-%d').date().strftime('%Y-%m')
                mes.add(conta_data)
                

            for m in mes:
                mes_normalize(m)
                dicionario[mes_normalize(m)] = {}



            for m in mes:
                for conta in contas:
                    conta_data = datetime.strptime(conta['data_vencimento'], '%Y-%m-%d').date().strftime('%Y-%m')
                    if conta_data == m:
                        dicionario[mes_normalize(m)][conta['categoria']] = []

            for m in mes:
                for conta in contas:
                    conta_data = datetime.strptime(conta['data_vencimento'], '%Y-%m-%d').date().strftime('%Y-%m')
                    if conta_data == m and conta['categoria'] in dicionario[mes_normalize(m)]:
                        dicionario[mes_normalize(m)][conta['categoria']].append(dict(conta))

            return dicionario
        
        except sqlite3.Error as e:
            conn.close()
            print(f"Erro ao buscar contas: {e}")
            return []
        
    @staticmethod
    def pagar_conta(conta_id: int) -> bool:
        try:
            conn = sqlite3.connect(os.getenv("DATABASE_PATH"))
            c = conn.cursor()
            c.execute("UPDATE conta SET pago = 1 WHERE id = ?", (conta_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            conn.close()
            print(f"Erro ao marcar conta como paga: {e}")
            return False
        
    @staticmethod
    def get_contas_pendentes(session_id: int, ano_mes: str) -> list:
        try:
            conn = sqlite3.connect(os.getenv("DATABASE_PATH"))
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM conta WHERE user_id = ? AND pago = 0 AND strftime('%Y-%m', data_vencimento) = ?", (session_id, ano_mes))
            contas = c.fetchall()
            conn.close()
            return [dict(conta) for conta in contas]
        except sqlite3.Error as e:
            conn.close()
            print(f"Erro ao buscar contas pendentes: {e}")
            return []