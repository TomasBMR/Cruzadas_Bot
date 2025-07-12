import numpy as np

from Trie import Trie
from Tabuleiro import Tabuleiro

class Bot:
    def __init__(self, tabuleiro: Tabuleiro, trie: Trie):
        self.tab: Tabuleiro = tabuleiro

        self.trie: Trie = trie

        self.jogadas: list
        self.num_letras: int
        self.primeiro_lance: bool

    def escolhe_melhor_jogada(self, letras: str, primeiro_lance: bool=False):
        self.busca_jogadas_possiveis(letras, primeiro_lance=primeiro_lance)
        self.jogadas.sort( key=lambda x: x[4] )

        if len(self.jogadas):
            return self.jogadas[-1]
        else:
            #Falta implementar essa logica
            return(-1, -1, True, "", 0, 0, [])#A string deveria ser as letras a serem trocadas

    def busca_jogadas_possiveis(self, letras: str, primeiro_lance: bool=False):
        letras_dict = {}
        for letra in letras:
            if letra not in letras_dict:
                letras_dict[letra] = 1
            else:
                letras_dict[letra] += 1

        self.num_letras = sum(letras_dict.values())
        self.jogadas = []
        self.primeiro_lance = primeiro_lance
        for i, linha in enumerate(self.tab.tabuleiro):
            for j, char in enumerate(linha):
                if char.isalpha() or (self.tab.alguma_letra_adjacente(i, j)) or (i == 7 and j == 7):

                    #Busca na vertical
                    if (dist := min(6 + (not primeiro_lance), self.tab.dist_cima_esq(i, j, False))) > 0:
                        self.pos_j = j
                        self.horizontal = False
                        for d in range(dist + 1):
                            self.pos_i = i - dist + d
                            self._busca_jogadas( i - dist + d, j, False, letras_dict, "", self.trie.raiz)
                    
                    #Busca na horizontal
                    if (dist := min(6 + (not primeiro_lance), self.tab.dist_cima_esq(i, j, True))) > 0:
                        self.pos_i = i
                        self.horizontal = True
                        for d in range(dist + 1):
                            self.pos_j = j - dist + d
                            self._busca_jogadas( i, j - dist + d, True, letras_dict, "", self.trie.raiz)


    def _busca_jogadas(self, i: int, j: int, horizontal: bool,
                       letras_disponiveis: dict[str, int], 
                       prefixo: list[str, tuple[int, int]], 
                       no: dict[str, dict], conectou: bool=False, 
                       pontos: int=0, multiplicadores: int=1,
                       palavras_ortogonais: list[str]=[]):

        if "\n" in no and sum(letras_disponiveis.values()) < self.num_letras and  conectou and self.tab.pos_vaga_ou_fora_tab(i, j):
            bonus = 50 if sum(letras_disponiveis.values()) == 0 and self.num_letras == 7 else 0
            self.jogadas.append((self.pos_i, self.pos_j, self.horizontal, prefixo, pontos * multiplicadores + sum([ponto[0] for ponto in palavras_ortogonais]) + bonus, palavras_ortogonais))
        
        if self.primeiro_lance and i==7 and j==7:
            conectou = True

        if i >= 15 or j >= 15:
            return

        if self.tab.tabuleiro[i][j].isdigit():
            for letra in letras_disponiveis:
                if letra in no:
                    palavra_horizontal = self.tab.palavra_ortogonal(i, j, not horizontal, letra) #tbm deve influenciar a pontuacao
                    if len(palavra_horizontal[3]) <= 1 or (len(palavra_horizontal[3]) > 1 and self.trie.busca(palavra_horizontal[3])):
                        especial = int(self.tab.quadrados_especiais[i][j])
                        valor_letra = self.tab.valor_letras[letra] * (especial if 0 < especial < 4 else 1)
                        multiplicador = (especial//2 if 3 < especial else 1)
                        
                        if len(palavra_horizontal[3]) > 1:
                            palavras_ortogonal = [(self.tab.pontos_palavra(*palavra_horizontal), palavra_horizontal)]
                            conectou = True
                        else:
                            palavras_ortogonal = []

                        letras_q_sobram = letras_disponiveis.copy() #fazer essa copia n parece razoavel, deve haver um caminho melhor# so faco a copia no caso de a letra ser usada
                        letras_q_sobram[letra] -= 1
                        if letras_q_sobram[letra] <= 0:
                            letras_q_sobram.pop(letra, None)
                        self._busca_jogadas(i + (not horizontal), j + horizontal, horizontal, 
                                            letras_q_sobram, prefixo + letra, no[letra], conectou,
                                            pontos + valor_letra, multiplicadores * multiplicador,
                                            palavras_ortogonais + palavras_ortogonal)

                elif letra == "?": #Joker
                    for possib in no:
                        if possib != "\n":
                            palavra_horizontal = self.tab.palavra_ortogonal(i, j, not horizontal, possib.upper())
                            if len(palavra_horizontal[3]) <= 1 or (len(palavra_horizontal[3]) > 1 and self.trie.busca(palavra_horizontal[3])):
                                especial = int(self.tab.quadrados_especiais[i][j])
                                multiplicador = (especial//2 if 3 < especial else 1)
                                palavras_ortogonal = [(self.tab.pontos_palavra(*palavra_horizontal), palavra_horizontal)] if len(palavra_horizontal[3]) > 1 else []
                                if len(palavra_horizontal[3]) > 1:
                                    palavras_ortogonal = [(self.tab.pontos_palavra(*palavra_horizontal), palavra_horizontal)]
                                    conectou = True
                                else:
                                    palavras_ortogonal = []
                                
                                letras_q_sobram = letras_disponiveis.copy() #fazer essa copia n parece razoavel, deve haver um caminho melhor # so faco a copia no caso de a letra ser usada
                                letras_q_sobram[letra] -= 1
                                if letras_q_sobram[letra] <= 0:
                                    letras_q_sobram.pop(letra, None)
                                self._busca_jogadas(i + (not horizontal), j + horizontal, horizontal, 
                                                    letras_q_sobram, prefixo + possib.upper(), no[possib], conectou,
                                                    pontos, multiplicadores * multiplicador,
                                                    palavras_ortogonais + palavras_ortogonal)

        else:
            if (letra := self.tab.tabuleiro[i][j]).lower() in no:
                valor_letra = self.tab.valor_letras[letra] if letra.islower() else 0
                self._busca_jogadas(i + (not horizontal), j + horizontal, horizontal,
                                    letras_disponiveis, prefixo + letra, no[letra.lower()], True,
                                    pontos + valor_letra, multiplicadores,
                                    palavras_ortogonais)


    def calc_pontos(self, prefixo: list[str, tuple[int, int]]):
        pontos = 0
        for letra in prefixo:
            pontos += letra


if __name__ == "__main__":
    trie = Trie()
    trie.carrega_palavras( "br-sem-acentos.txt" )

    tabu = Tabuleiro()
    #tab.adiciona_palavra( 7, 5, True, "astro" )
    """tab.adiciona_palavra(1, 9, False, "valiamos")#72
    tab.adiciona_palavra(5, 5, False, "lha")#11
    tab.adiciona_palavra(4, 8, True, "fim")#12
    tab.adiciona_palavra(2, 8, True, "gaste")#28
    tab.adiciona_palavra(2, 6, True, "pegaste")#13
    tab.adiciona_palavra(0, 7, False, 'breca')#30
    tab.adiciona_palavra(0, 11, False, 'vote')#22
    tab.adiciona_palavra(7, 4, True, 'castro')#7
    tab.adiciona_palavra(7, 4, True, 'castrou')#8
    tab.adiciona_palavra(3, 5, False, 'bilhar')#12
    tab.adiciona_palavra(0, 9, False, 'avaliamos')#13
    tab.adiciona_palavra(4, 2, True, 'flui')#16
    tab.adiciona_palavra(2, 6, True, 'pegastes')#12
    tab.adiciona_palavra(0, 3, False, 'cruel')#18
    tab.adiciona_palavra(1, 13, False, 'estudam')#24
    tab.adiciona_palavra(0, 0, True, 'pOncas')#27
    tab.adiciona_palavra(4, 2, False, 'fAtigou')#17
    tab.adiciona_palavra(10, 0, True, 'chupei')#22
    tab.adiciona_palavra(8, 0, False, 'secarei')#27
    tab.adiciona_palavra(10, 3, False, 'plano')#20
    tab.adiciona_palavra(14, 2, True, 'soquemo')#48

    #tab.adiciona_palavra(9, 7, False, 'diziam')#26"""


    bot = Bot( tabu, trie )

    tabu.print_tabuleiro(True)

    print(bot.escolhe_melhor_jogada("dxaozii", True))

    #tab.print_tabuleiro(True)
