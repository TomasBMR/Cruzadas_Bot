import numpy as np

from Trie import Trie
from Tabuleiro import Tabuleiro

class Bot:
    def __init__(self, tabuleiro: Tabuleiro, trie: Trie):
        self.tab: Tabuleiro = tabuleiro
        #self.tab.tabuleiro[7] = "00000astro00000"

        self.trie: Trie = trie


    def escolhe_melhor_jogada(self, letras: str, primeiro_lance: bool=False):
        jogadas = self.busca_jogadas_possiveis(letras, primeiro_lance=primeiro_lance)
        jogadas_pontos = [(jogada[0], self.tab.pontos_palavra(*jogada[0]), jogada[1], jogada[2]) for jogada in jogadas]
        jogadas_pontos.sort( key=lambda x: x[2] )
        #for jogada in jogadas_pontos:
            #if jogada[1] != jogada[2]:
                #print(f"jogada {jogada[0]} deu diferente! {jogada[1]} e {jogada[2]}]")
        #print(jogadas_pontos)
        #print(len(jogadas))
        if len(jogadas_pontos):
            return jogadas_pontos[-1]
        else:
            return((-1, -1, True, ""), 0, 0, [])#A string deveria ser as letras a serem trocadas

    def busca_jogadas_possiveis(self, letras: str, primeiro_lance: bool=False):
        letras_dict = {}
        for letra in letras:
            if letra not in letras_dict:
                letras_dict[letra] = 1
            else:
                letras_dict[letra] += 1
        num_letras = sum(letras_dict.values())

        jogadas = []
        for i, linha in enumerate(self.tab.tabuleiro):
            for j, char in enumerate(linha):
                if char.isalpha() or (self.tab.alguma_letra_adjacente(i, j)) or (i == 7 and j == 7):
                    #print(i, j, char)
                    #Busca na vertical
                    jogadas_v, jogadas_h = [], []
                    if (dist := min(6, self.tab.dist_cima_esq(i, j, False))) > 0:
                        for d in range(dist+1):
                            #print(f"Buscando em {(i - dist + d, j, False)}")
                            jogadas_h += [((i - dist + d, j, False, jogada[0]), jogada[1], jogada[2]) for jogada in self._busca_jogadas( i - dist + d, j, False, letras_dict, "", self.trie.raiz, num_letras, conectou=primeiro_lance)]
                    
                    #print(jogadas_h)
                    #Busca na horizontal
                    if (dist := min(6, self.tab.dist_cima_esq(i, j, True))) > 0:
                        for d in range(dist+1):
                            #print(f"Buscando em {( i, j - dist + d, True)}")
                            jogadas_v += [((i, j - dist + d, True, jogada[0]), jogada[1], jogada[2]) for jogada in self._busca_jogadas( i, j - dist + d, True, letras_dict, "", self.trie.raiz, num_letras, conectou=primeiro_lance)]
                    #print(jogadas_v)
                    jogadas += jogadas_h + jogadas_v
        #print(jogadas[:10])
        return jogadas


    """def _avalia_jogadas(self, i: int, j: int, letras: str) -> tuple[tuple[int, str], list[str]]:
        #Return (melhor pontuacao e palavra, lista de palavras)
        letras_dict = {}
        for letra in letras:
            if letra not in letras_dict:
                letras_dict[letra] = 1
            else:
                letras_dict[letra] += 1
        return self._busca_jogadas( i, j, letras_dict, "", self.trie.raiz)"""


    def _busca_jogadas(self, i: int, j: int, horizontal: bool,
                       letras_disponiveis: dict[str, int], 
                       prefixo: list[str, tuple[int, int]], 
                       no: dict[str, dict], num_letras: int, conectou: bool=False, 
                       pontos: int=0, multiplicadores: int=1,
                       palavras_ortogonais: list[str]=[]) -> list[tuple[tuple[int, int, bool, str], list[tuple[int, int, bool, str]]]]:
        palavras_possiveis = []
        #print(prefixo, "\n" in no)
        #if prefixo == "dizia":
        #print("\n" in no, sum(letras_disponiveis.values()) < num_letras, conectou, self.tab.pos_vaga_ou_fora_tab(i + (not horizontal), j + horizontal))
        #print(i + (not horizontal), j + horizontal)
        if "\n" in no and sum(letras_disponiveis.values()) < num_letras and  conectou and self.tab.pos_vaga_ou_fora_tab(i, j):
            bonus = 50 if sum(letras_disponiveis.values()) == 0 and num_letras == 7 else 0
            palavras_possiveis.append((prefixo, pontos * multiplicadores + sum([ponto[0] for ponto in palavras_ortogonais]) + bonus, palavras_ortogonais))
        
        #if self.tab.pos_vaga_ou_fora_tab(i + (not horizontal), j + horizontal):#sum(letras_disponiveis.values()) < 7 and 7 - sum(letras_disponiveis.values()) >= min_letras:
            #pass

        if i >= 15 or j >= 15:
            return palavras_possiveis

        #print("->", self.tab.tabuleiro[i][j])
        if self.tab.tabuleiro[i][j].isdigit():
            for letra in letras_disponiveis:
                letras_q_sobram = letras_disponiveis.copy() #fazer essa copia n parece razoavel, deve haver um caminho melhor # Isso so deveria acontecer depois de se verificar q a letra esta no no
                letras_q_sobram[letra] -= 1
                if letras_q_sobram[letra] <= 0:
                    letras_q_sobram.pop(letra, None)
                #if i == 0:
                    #print("-->", prefixo, letra, letra in no)
                if letra in no:
                    palavra_horizontal = self.tab.palavra_ortogonal(i, j, not horizontal, letra) #tbm deve influenciar a pontuacao
                    if len(palavra_horizontal[3]) <= 1 or (len(palavra_horizontal[3]) > 1 and self.trie.busca(palavra_horizontal[3])):
                        valor_letra = self.tab.valor_letras[letra] * (int(self.tab.quadrados_especiais[i][j]) if 0 < int(self.tab.quadrados_especiais[i][j]) < 4 else 1)
                        multiplicador = (int(self.tab.quadrados_especiais[i][j])//2 if 3 < int(self.tab.quadrados_especiais[i][j]) else 1)
                        if len(palavra_horizontal[3]) > 1:
                            palavras_ortogonal = [(self.tab.pontos_palavra(*palavra_horizontal), palavra_horizontal)]
                            conectou = True
                        else:
                            palavras_ortogonal = []
                        palavras_possiveis += self._busca_jogadas(i + (not horizontal), j + horizontal, horizontal, 
                                                                  letras_q_sobram, prefixo + letra, no[letra], num_letras, conectou,
                                                                  pontos + valor_letra, multiplicadores * multiplicador,
                                                                  palavras_ortogonais + palavras_ortogonal)

                elif letra == "?": #Joker
                    for possib in no:
                        if possib != "\n":
                            palavra_horizontal = self.tab.palavra_ortogonal(i, j, not horizontal, possib) #tbm deve influenciar a pontuacao
                            if len(palavra_horizontal[3]) <= 1 or (len(palavra_horizontal[3]) > 1 and self.trie.busca(palavra_horizontal[3])):
                                #valor_letra = tab.valor_letras[letra] * (int(tab.quadrados_especiais[i][j]) if 0 < int(tab.quadrados_especiais[i][j]) < 4 else 1)
                                multiplicador = (int(self.tab.quadrados_especiais[i][j])//2 if 3 < int(self.tab.quadrados_especiais[i][j]) else 1)
                                palavras_ortogonal = [(self.tab.pontos_palavra(*palavra_horizontal), palavra_horizontal)] if len(palavra_horizontal[3]) > 1 else []
                                if len(palavra_horizontal[3]) > 1:
                                    palavras_ortogonal = [(self.tab.pontos_palavra(*palavra_horizontal), palavra_horizontal)]
                                    conectou = True
                                else:
                                    palavras_ortogonal = []
                                palavras_possiveis += self._busca_jogadas(i + (not horizontal), j + horizontal, horizontal, 
                                                                          letras_q_sobram, prefixo + possib.upper(), no[possib], num_letras, conectou,
                                                                          pontos, multiplicadores * multiplicador,
                                                                          palavras_ortogonais + palavras_ortogonal)

        else:
            if (letra := self.tab.tabuleiro[i][j]).lower() in no:
                #print("!", prefixo, type(letra))
                valor_letra = self.tab.valor_letras[letra] if letra.islower() else 0
                palavras_possiveis += self._busca_jogadas(i + (not horizontal), j + horizontal, horizontal,
                                                          letras_disponiveis, prefixo + letra, no[letra.lower()], num_letras, True,
                                                          pontos + valor_letra, multiplicadores,
                                                          palavras_ortogonais)

        return palavras_possiveis

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
