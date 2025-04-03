class Avisos:
    def erro(self, msg):
        try:
            with open("erro.txt", "a") as arquivo:  # Abre o arquivo em modo de adição ("a")
                arquivo.write(msg + "\n")  # Escreve a mensagem de erro e uma nova linha
            print("Mensagem de erro escrita em 'erro.txt' com sucesso.")
        except Exception as e:
            print(f"Ocorreu um erro ao escrever no arquivo 'erro': {e}")
    
    def teste(self, msg):
        try:
            with open("teste.txt", "a") as arquivo:  # Abre o arquivo em modo de adição ("a")
                arquivo.write(str(msg) + "\n")  # Escreve a mensagem de erro e uma nova linha
            print("Mensagem de teste escrita em 'teste.txt' com sucesso.")
        except Exception as e:
            print(f"Ocorreu um erro ao escrever no arquivo 'teste': {e}")