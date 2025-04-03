from database import *

class Balanco_Patrimonial(Data_base):
    def atualizar_contas(self, codigo, operation_type, valor):
        saldo_atual = self.execute_get(f"SELECT saldo FROM contas_contabeis WHERE codigo = ?", (str(codigo),))

        valor = float(valor)
        
        if saldo_atual:
            saldo_atual = saldo_atual[0][0]
        else:
            saldo_atual = 0

        saldo_atualizado = 0

        self.teste(f"{saldo_atual, valor}")
        dig = codigo[0]

        if operation_type == 'debito':
            if dig == '1':
                saldo_atualizado = saldo_atual + valor
            else:
                saldo_atualizado = saldo_atual - valor
        else:
            if dig == '1':
                saldo_atualizado = saldo_atual - valor
            else:
                saldo_atualizado = saldo_atual + valor

        self.execute_post(f"UPDATE contas_contabeis SET saldo = ? WHERE codigo = ?", (saldo_atualizado, codigo))

    # def montar_balanco (self, data_ini, data_fim):

