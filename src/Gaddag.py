import time
from Trie import Trie

class Gaddag:
    """ Estrutura em arvore que armazena e facilita a busca de uma lista de plavras.
        Semelhante a Trie mas cada palavra eh representada n vezes em que n eh o numero de letras na palavra"""
    def __init__(self, path: str=None):
        self.raiz: dict[str, dict] = {}
        self.num_palavras: int = 0
        self.num_nos: int = 0

        if path:
            self.carrega_palavras(path)

    def insere(self, palavra: str):
        """Insere uma palavra na Arvore"""
        for i, _ in enumerate(palavra):
            pal = palavra[i:] + "+" + palavra[i::-1][1:] + "\n"
            #print(f"inserindo {pal}")
            no = self.raiz
            for letra in pal:
                if letra not in no:
                    no[letra] = {}
                    self.num_nos += 1
                no = no[letra]
            self.num_palavras += 1
        

    def busca(self, palavra: str) -> bool:
        """Verifica se uma palavra está na Arvore"""
        no = self.raiz
        for letra in palavra + "\n":
            if letra not in no:
                return False
            no = no[letra]
        return True
    
    
    def busca_possibilidades(self, letras_disponiveis: str) -> list[str]:
        """Gera um dicionario com a contagem das letras disponiveis para em seguida
        encontrae todas as plavras q se pode escrever com as letras disponiveis
        """
        letras_dict = {}
        for letra in letras_disponiveis:
            if letra not in letras_dict:
                letras_dict[letra] = 1
            else:
                letras_dict[letra] += 1
        return self._busca_possibilidades(letras_dict)
    

    def _busca_possibilidades(self, letras_disponiveis: dict[str, int], prefixo: str=None, no: dict=None) -> list[str]:
        """Busca recursivamente todas as plavras q se pode escrever com as letras disponiveis"""
        #Talvez mudar letra de str para set...
        palavras_possiveis = []
        if prefixo is None: prefixo = "" # Dá pra tirar esses ifs?
        if no is None: 
            no = self.raiz
        elif "\n" in no:
            palavras_possiveis.append(prefixo)

        for letra in letras_disponiveis:
            letras_q_sobram = letras_disponiveis.copy() #fazer essa copia n parece razoavel, deve haver um caminho melhor
            letras_q_sobram[letra] -= 1
            if letras_q_sobram[letra] <= 0:
                letras_q_sobram.pop(letra, None)

            if letra in no:
                palavras_possiveis += self._busca_possibilidades(letras_q_sobram, prefixo + letra, no[letra])

            elif letra == "?": #Joker
                for possib in no:
                    if possib != "\n":
                        palavras_possiveis += self._busca_possibilidades(letras_q_sobram, f"{prefixo}({possib})", no[possib])

        return palavras_possiveis


    def carrega_palavras(self, path:str):
        """Recebe o caminha para um txt com uma lista de palavras e carrega elas na Arvore"""
        file = open(path, "r")    
        palavras = [palavra.lower() for palavra in file.read().split("\n") if len(palavra)]
        #print(len(palavras))
        #print(sum([len(palavra) for palavra in palavras])/len(palavras))

        for palavra in palavras:
            self.insere(palavra)


if __name__ == "__main__":
    path = "br-sem-acentos.txt"
    #print("começou")
    #t0 = time.time()
    #trie = Trie(path)
    #print(time.time()-t0)
    print("começou")
    t0 = time.time()
    gaddag = Gaddag()
    gaddag.insere("gato")
    print(time.time()-t0)
    print(gaddag.num_palavras)
    print(gaddag.num_nos)