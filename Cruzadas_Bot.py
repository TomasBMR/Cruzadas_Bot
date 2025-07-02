import numpy as np

from Trie import Trie
from Tabuleiro import Tabuleiro

class Bot:
    def __init__(self, tabuleiro: Tabuleiro, trie: Trie):
        self.tab: Tabuleiro = tabuleiro
        #self.tab.tabuleiro[7] = "00000astro00000"

        self.trie: Trie = trie

        self.letras: str = ""


    def calc_melhor_jogada(self):
        for i, linha in enumerate(self.tab):
            for j, char in enumerate(linha):
                #Expande na vertical
                if dist := self.tab.dist_para_cima(i, j) > 0:
                    for d in range(dist+1):
                        self.avalia_jogadas( i - dist + d, j )
                    
                #Expande na horizontal
    

    def avalia_jogadas(self, i: int, j: int) -> tuple[tuple[int, str], list[str]]:
        #Return (melhor pontuacao e palavra, lista de palavras)
        letras_dict = {}
        for letra in self.letras:
            if letra not in letras_dict:
                letras_dict[letra] = 1
            else:
                letras_dict[letra] += 1
        self._busca_jogadas( i, j, letras_dict, "", self.trie.raiz)


    def _busca_jogadas(self, 
                       i: int, j: int, 
                       letras_disponiveis: dict[str, int], 
                       prefixo: list[str, tuple[int, int]], 
                       no: dict[str, dict], 
                       pontuacao_ortogonais: list[tuple[str, int]]=[]) -> list[str]:
        palavras_possiveis = []
        if "\n" in no:
            palavras_possiveis.append(prefixo)

        if i >= 15 or j >= 15:
            return palavras_possiveis

        if self.tab.tabuleiro[i][j].isdigit():
            for letra in letras_disponiveis:
                letras_q_sobram = letras_disponiveis.copy() #fazer essa copia n parece razoavel, deve haver um caminho melhor # Isso so deveria acontecer depois de se verificar q a letra esta no no
                letras_q_sobram[letra] -= 1
                if letras_q_sobram[letra] <= 0:
                    letras_q_sobram.pop(letra, None)

                if letra in no:
                    palavra_horizontal = self.tab.palavra_horizontal(i, j, letra) #tbm deve influenciar a pontuacao
                    if self.trie.busca(palavra_horizontal):
                        palavras_possiveis += self._busca_jogadas(i + 1, j, letras_q_sobram, prefixo + [letra, (i, j)], no[letra], pontuacao_ortogonais+[(palavra_horizontal, )])

                elif letra == "?": #Joker
                    for possib in no:
                        if possib != "\n":
                            palavra_horizontal = self.tab.palavra_horizontal(i, j, possib) #tbm deve influenciar a pontuacao
                            if self.trie.busca(palavra_horizontal):
                                palavras_possiveis += self._busca_jogadas(i+1, j, letras_q_sobram, prefixo + [possib.lower(), (i, j)], no[possib])

        else:
            if letra := self.tab.tabuleiro[i][j] in no:
                palavras_possiveis += self._busca_jogadas(i+1, j, letras_q_sobram, prefixo + [letra, (i, j)], no[letra])

        return palavras_possiveis

    def calc_pontos(self, prefixo: list[str, tuple[int, int]]):
        pontos = 0
        for letra in prefixo:
            pontos += letra


if __name__ == "__main__":
    trie = Trie()
    trie.load_words( "br-sem-acentos.txt" )

    tab = Tabuleiro()
    tab.tabuleiro[7] = "00000ASTRO00000"

    bot = Bot( tab, trie )

    tab.print_tabuleiro()
