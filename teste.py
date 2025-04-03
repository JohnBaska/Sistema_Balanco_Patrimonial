from balanco_patrimonial import *
from datetime import timedelta

class Teste(Balanco_Patrimonial):
    def __init__ (self):
        self.start_banco()
        self.start_contas()
        self.start_transacoes()
    
    def formatar_dados(self, dados):
        """
        Recebe dados de um banco de dados em formato de tuplas, formata e imprime.

        Args:
            dados (list): Uma lista de tuplas, onde cada tupla representa uma linha do banco de dados.
        """

        if not dados:
            print("Nenhum dado para exibir.")
            return

        # Nomes das colunas (você pode ajustar conforme necessário)
        colunas = ["ID", "Código", "Descrição", "Tipo", "Valor"]

        # Imprime o cabeçalho
        self.teste("-" * 70)
        print("|", end="")
        for coluna in colunas:
            print(f" {coluna:<20} |", end="")
        print()
        print("-" * 70)

        # Imprime os dados
        for linha in dados:
            print("|", end="")
            for valor in linha:
                print(f" {str(valor):<20} |", end="")
            print()
        print("-" * 70)
        
    def start_contas(self):
        dados = [
            ('1.1.1.01', 'Caixa', 'Ativo', 5000.00),
            ('1.1.1.02', 'Banco Conta Movimento', 'Ativo', 20000.00),
            ('1.2.1.01', 'Estoque', 'Ativo', 15000.00),
            ('2.1.1.01', 'Fornecedores a Pagar', 'Passivo', 8000.00),
            ('2.1.2.01', 'Empréstimos Bancários', 'Passivo', 10000.00),
            ('3.1.1.01', 'Capital Social', 'Patrimônio Líquido', 50000.00),
            ('3.2.1.01', 'Reservas de Lucros', 'Patrimônio Líquido', 5000.00)
        ]

        for i in dados:
            self.criar_conta(i)
        
        self.formatar_dados(self.execute_get("SELECT * FROM contas_contabeis"))

    def start_transacoes(self):
        hoje = date.today()

        transacoes = [
            (hoje - timedelta(days=5), '1.1.1.01', '2.1.1.01', 3000.00, 'Pagamento de fornecedores'),
            (hoje - timedelta(days=3), '1.1.1.02', '2.1.2.01', 5000.00, 'Pagamento de empréstimo bancário'),
            (hoje - timedelta(days=1), '1.2.1.01', '1.1.1.01', 2000.00, 'Compra de mercadorias à vista'),
            (hoje, '3.1.1.01', '1.1.1.02', 10000.00, 'Aporte de capital pelos sócios'),
            (hoje + timedelta(days=2), '1.1.1.01', '3.2.1.01', 1500.00, 'Reserva de lucros'),
        ]

        for i in transacoes:
            codigo_debito = str(i[1])
            codigo_credito = str(i[2])
            self.atualizar_contas(codigo_debito, 'debito', i[3])
            self.atualizar_contas(codigo_credito, 'credito', i[3])
        
        self.formatar_dados(self.execute_get("SELECT * FROM contas_contabeis"))

     
Teste()
