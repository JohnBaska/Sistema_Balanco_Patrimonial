from sqlite3 import *
from datetime import date
from avisos import *

class Database(Avisos):
    DB_NAME = "contabilidade.sql"
    def start_banco(self):
        # Conecta ao SQLite ou cria um arquivo 
        conn = connect(self.DB_NAME) 
        cursor = conn.cursor()

        # Cria a tabela contas contábeis
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contas_contabeis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT NOT NULL UNIQUE,
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

    def criar_conta(self, dados):
        self.execute_post("""
            INSERT OR IGNORE INTO contas_contabeis (codigo, nome, tipo, saldo) VALUES (?, ?, ?, ?);
            """, dados)

    def registrar_transacao (self, dados):
        self.execute_post("""
            INSERT OR IGNORE INTO transacoes (data, conta_debito, conta_credito, valor, descricao) VALUES (?, ?, ?, ?, ?);
            """, dados)
    
    def execute_post(self, prompt, param):
        # Conecta ao SQLite ou cria um arquivo 
        conn = connect(self.DB_NAME) 
        cursor = conn.cursor()
        
        cursor.execute(prompt, param)

        # Confirma e fecha conecção
        conn.commit()
        cursor.close()
        conn.close()
    
    def execute_get(self, prompt, param=None):
        # Conecta ao SQLite ou cria um arquivo 
        conn = connect(self.DB_NAME) 
        cursor = conn.cursor()
        
        if param == None:
            cursor.execute(prompt)
        else:
            cursor.execute(prompt, param)

        res = cursor.fetchall()

        # Confirma e fecha conecção
        conn.commit()
        cursor.close()
        conn.close()

        return res

        
Database()