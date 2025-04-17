from flask import Flask, redirect, url_for, render_template, flash, request
import random
import string
from database import *

class APP(Database):
    app = None
    def __init__ (self, import_name):
        self.app = Flask(import_name)
        self.start_banco()

        self._setup_routes_contas()
        self._setup_routes_lancamentos()

    def get_secret_key(self, tamanho=24):
        caracteres = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(caracteres) for _ in range(tamanho))
    
    def _setup_routes_contas(self):
        @self.app.route('/', methods=['POST', 'GET'])
        def home():
            return render_template('home.html')
        
        @self.app.route('/contas', methods=['POST', 'GET'])
        def contas():
            contas = self.execute_get("SELECT * FROM contas_contabeis")
            self.teste(f"CONTAS: {contas}")
            return render_template('contas.html', contas=contas)

        @self.app.route('/create_conta', methods=['POST', 'GET'])
        def create_conta():
            return render_template('create_conta.html')

        @self.app.route('/execute_create_conta', methods=['POST'])
        def execute_create_conta():
            dados = (request.form.get('code'), request.form.get('name'), request.form.get('type'), float(request.form.get('balance')))

            try:
                self.criar_conta(dados)
                flash(f"Conta {dados[1]} Criada", 'sucess')
            except Exception as e:
                flash(f"Erro na criação da conta: {e}", 'error')
            
            return redirect(url_for('create_conta'))
    
    def _setup_routes_lancamentos(self):
        @self.app.route('/lancamentos', methods=['POST', 'GET'])
        def lancamentos():
            lancamentos = self.execute_get("SELECT * FROM transacoes")

            self.teste(lancamentos)

            return render_template('lancamentos.html', lancamentos=lancamentos)

        @self.app.route('/create_lancamento', methods=['POST', 'GET'])
        def create_lancamento():
            contas = self.execute_get("SELECT * FROM contas_contabeis")
            self.teste(f"CONTAS: {contas}")

            return render_template('create_lancamento.html', contas=contas)

        @self.app.route('/execute_create_lancamento', methods=['POST'])
        def execute_create_lancamento():
            dados = (request.form.get('date'), request.form.get('debito'), request.form.get('credito'), float(request.form.get('valor')),request.form.get('descricao'))

            try:
                self.teste(dados)
                self.registrar_transacao(dados)
                flash(f"Lançamento Feito", 'sucess')
            except Exception as e:
                flash(f"Erro na criação no lançamento: {e}", 'error')
            
            return redirect(url_for('create_lancamento'))

    def run(self, **kwargs):
        # Método para rodar a aplicação
        self.app.run(**kwargs)



if __name__ == '__main__':
    app = APP(__name__)
    app_flask = app.app
    app_flask.secret_key = app.get_secret_key()
    app.run(debug=True, port=5000)