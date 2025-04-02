from sqlite3 import *
from datetime import date
from avisos import *

class Data_base(Avisos):
    DB_NAME = "contabilidade.sqlite3"
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

    def criar_conta(self, codigo, nome, tipo, saldo):
        self.execute_post("""
            INSERT OR IGNORE INTO contas_contabeis (codigo, nome, tipo, saldo) VALUES (?, ?, ?, ?);
            """, (codigo, nome, tipo, saldo))

    def transacao (self, data, conta_debito, conta_crédito, valor, descricao):
        self.execute_post("""
            INSERT OR IGNORE INTO contas_contabeis (codigo, nome, tipo, saldo) VALUES (?, ?, ?, ?);
            """, (data, conta_debito, conta_crédito, valor, descricao))
    def execute_post(self, prompt, param):
        # Conecta ao SQLite ou cria um arquivo 
        conn = connect(self.DB_NAME) 
        cursor = conn.cursor()
        
        cursor.execute(prompt, param)

        # Confirma e fecha conecção
        conn.commit()
        cursor.close()
        conn.close()
    
    def execute_get(self, prompt, param):
        # Conecta ao SQLite ou cria um arquivo 
        conn = connect(self.DB_NAME) 
        cursor = conn.cursor()
        
        res = cursor.execute(prompt, param)

        # Confirma e fecha conecção
        conn.commit()
        cursor.close()
        conn.close()

        return res

        
Data_base()