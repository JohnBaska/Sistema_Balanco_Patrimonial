from sqlite3 import *
from datetime import date
from avisos import *

class Data_base(Avisos):
    DB_NAME = "contabilidade.sqlite"
    def __init__(self):
        self.start()

    def start(self):
        # Conecta ao SQLite ou cria um arquivo 
        conn = connect(self.DB_NAME) 
        cursor = conn.cursor()

        # Cria a tabela contas contábeis
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contas_contabeis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT UNIQUE NOT NULL,
                    nome TEXT NOT NULL,
                    tipo TEXT CHECK (tipo IN ('Ativo', 'Passivo', 'Patrimoio Liquido')) NOT NULL,
                    saldo REAL DEFAULT 0
                )""")
        except Exception as e:
            self.erro(f"Erro ao criar a tabela de contas contabeis: {e}")
        
        # Criar a tabela de transações
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data DATE NOT NULL,
                    conta_debito TEXT NOT NULL,
                    conta_credito TEXT NOT NULL,
                    valor REAL NOT NULL CHECK (valor > 0),
                    descricao TEXT,
                    FOREIGN KEY (conta_debito) REFERENCES contas_contabeis(codigo),
                    FOREIGN KEY (conta_credito) REFERENCES contas_contabeis(codigo)
                );
            """)
        except Exception as e:
            self.erro(f"Erro ao criar a tabela de contas contabeis: {e}")

        # Confirma e fecha conecção
        conn.commit()
        cursor.close()
        conn.close()

        
Data_base()