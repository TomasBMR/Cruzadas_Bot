import numpy as np

from .Trie import Trie
from .Gaddag import Gaddag
from .Tabuleiro import Tabuleiro

#from Cruzadas_Bot import Bot

class Gaddag_Bot:
    def __init__(self, tabuleiro: Tabuleiro, trie: Trie, gaddag: Gaddag):
        self.tab: Tabuleiro = tabuleiro

        self.trie: Trie = trie

        self.gaddag: Gaddag = gaddag

        self.jogadas: list
        self.num_letras: int
        self.primeiro_lance: bool

    def escolhe_melhor_jogada( self, letras: str, primeiro_lance: bool=False ):
        self.busca_jogadas_possiveis( letras, primeiro_lance=primeiro_lance )
        self.jogadas.sort( key=lambda x: x[4] )

        if len(self.jogadas):
            #print(self.jogadas[-15:])
            #print("Gaddag^^^")
            return self.jogadas[-1], self.jogadas
        else:
            #Falta implementar essa logica
            return(-1, -1, True, "", 0), [(-1, -1, True, "", 0)]#A string deveria ser as letras a serem trocadas

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

                if char.isalpha() or (i == 7 and j == 7):
                    #Busca na vertical
                    self.pos_j = j
                    self.pos_i = i
                    self.horizontal = False
                    self._busca_jogadas(i, j, False, letras_dict, "", self.gaddag.raiz)
                    self.horizontal = True
                    self._busca_jogadas(i, j, True, letras_dict, "", self.gaddag.raiz)

                elif self.tab.alguma_letra_adjacente(i, j):
                    v_c, v_b, h_e, h_d = self.tab.qual_letra_adjacente(i, j)
                    self.pos_j = j
                    self.pos_i = i
                    if v_c or v_b:#Aqui vai ter que remover redundancia
                        self.horizontal = True
                        self._busca_jogadas(i, j, True, letras_dict, "", self.gaddag.raiz)
                        #self._busca_jogadas_Trie(i, j, True, letras_dict, "", self.trie.raiz)
                    if h_e or h_d:
                        self.horizontal = False
                        self._busca_jogadas(i, j, False, letras_dict, "", self.gaddag.raiz)
                        #self._busca_jogadas_Trie(i, j, False, letras_dict, "", self.trie.raiz)

                        

                    


    def _busca_jogadas(self, i: int, j: int, horizontal: bool,
                                    letras_disponiveis: dict[str, int], 
                                    prefixo: list[str, tuple[int, int]], 
                                    no: dict[str, dict], sentido: bool=True, #sentido True direita/baixo
                                    pontos: int=0, multiplicadores: int=1,
                                    palavras_ortogonais: list[str]=[], caminho:list[dict]="", infos:list[int]=None):
        """Usa uma gaddag para encontrar os lances possíveis 
        que passam por uma posicao especifica"""
        if infos is None:
            infos = [(i, j)]
        else:
            infos = infos + [(i, j)]

        """if infos[0] == (1, 11):
            print("Aqui!!!!")
            print(prefixo)
            print(caminho)
            print(horizontal, infos)"""
        
        if "\n" in no and sum(letras_disponiveis.values()) < self.num_letras and self.tab.pos_vaga_ou_fora_tab(i, j):
            bonus = 50 if sum(letras_disponiveis.values()) == 0 and self.num_letras == 7 else 0
            #sinal_sentido = 1 if sentido else -1
            self.jogadas.append((i + (not horizontal), j + horizontal, self.horizontal, prefixo, pontos * multiplicadores + sum([ponto[0] for ponto in palavras_ortogonais]) + bonus))#, palavras_ortogonais, caminho, infos))
            #if prefixo=='duplos':
            #    print(self.jogadas[-1])
        if "+" in no and self.tab.pos_vaga_ou_fora_tab(i, j): #Constroi inicio da palavra para traz
            #if self.pos_i == 7 and self.pos_j == 7:
                #print(prefixo, caminho)
                #print(not self.tab.pos_vaga(self.pos_i, self.pos_j))
            #Verifica se a proxima pos esta vaga antes de voltar
            if self.tab.pos_vaga_ou_fora_tab(i, j):
                self._busca_jogadas(self.pos_i - (not horizontal), self.pos_j - horizontal, horizontal, 
                                    letras_disponiveis, prefixo, no["+"], False,
                                    pontos, multiplicadores,
                                    palavras_ortogonais, caminho + "+", infos)
            
        if i < 0 or j < 0 or i >= 15 or j >= 15:
            return
        
            



        #if self.pos_i==7 and self.pos_j == 7:
            #print(i, j, self.tab.tabuleiro[i][j])
        #    self.tab.print_tabuleiro()
        if self.tab.tabuleiro[i][j].isdigit():
            for letra in letras_disponiveis:
                ortogonais = self.tab.get_letras_ortogonais(i, j, not horizontal) #Letras que podem fazer palavras ortogonalmente
                if letra in no and (letra in ortogonais or "*" in ortogonais):
                    palavra_horizontal = self.tab.palavra_ortogonal(i, j, not horizontal, letra) #Preciso buscar pq influencia a pontuacao
                    if len(palavra_horizontal[3]) <= 1 or (len(palavra_horizontal[3]) > 1 and self.trie.busca(palavra_horizontal[3])):
                        especial = int(self.tab.quadrados_especiais[i][j])
                        valor_letra = self.tab.valor_letras[letra] * (especial if 0 < especial < 4 else 1)
                        multiplicador = (especial//2 if 3 < especial else 1)
                        
                        palavras_ortogonal = []
                        if len(palavra_horizontal[3]) > 1:
                            palavras_ortogonal = [(self.tab.pontos_palavra(*palavra_horizontal), palavra_horizontal)]

                        letras_q_sobram = letras_disponiveis.copy() #fazer essa copia n parece razoavel, deve haver um caminho melhor# so faco a copia no caso de a letra ser usada
                        letras_q_sobram[letra] -= 1
                        if letras_q_sobram[letra] <= 0:
                            letras_q_sobram.pop(letra, None)
                        sinal_sentido = 1 if sentido else -1
                        n_prefixo = prefixo + letra if sentido else letra + prefixo

                        self._busca_jogadas(i + (not horizontal) * sinal_sentido, j + horizontal * sinal_sentido, horizontal, 
                                            letras_q_sobram, n_prefixo, no[letra], sentido,
                                            pontos + valor_letra, multiplicadores * multiplicador,
                                            palavras_ortogonais + palavras_ortogonal, caminho + letra, infos)

                elif letra == "?": #Joker
                    for possib in no:
                        ortogonais = self.tab.get_letras_ortogonais(i, j, not horizontal)
                        if possib != "\n" and possib != "+" and (possib in ortogonais or "*" in ortogonais):
                            palavra_horizontal = self.tab.palavra_ortogonal(i, j, not horizontal, possib.upper())
                            if len(palavra_horizontal[3]) <= 1 or (len(palavra_horizontal[3]) > 1 and self.trie.busca(palavra_horizontal[3])):
                                especial = int(self.tab.quadrados_especiais[i][j])
                                multiplicador = (especial//2 if 3 < especial else 1)
                                palavras_ortogonal = [(self.tab.pontos_palavra(*palavra_horizontal), palavra_horizontal)] if len(palavra_horizontal[3]) > 1 else []
                                
                                
                                letras_q_sobram = letras_disponiveis.copy() #fazer essa copia n parece razoavel, deve haver um caminho melhor # so faco a copia no caso de a letra ser usada
                                letras_q_sobram[letra] -= 1
                                if letras_q_sobram[letra] <= 0:
                                    letras_q_sobram.pop(letra, None)
                                sinal_sentido = 1 if sentido else -1
                                n_prefixo = prefixo + possib.upper() if sentido else possib.upper() + prefixo
                                self._busca_jogadas(i + (not horizontal) * sinal_sentido, j + horizontal * sinal_sentido, horizontal, 
                                                    letras_q_sobram, n_prefixo, no[possib], sentido,
                                                    pontos, multiplicadores * multiplicador,
                                                    palavras_ortogonais + palavras_ortogonal, caminho + possib, infos)

        else:
            letra = self.tab.tabuleiro[i][j]
            #if self.pos_i==7 and self.pos_j == 7: print("letra ja no tab")
            #infos.append(("inter!"))
            if letra.lower() in no:
                #if self.pos_i==7 and self.pos_j == 7:
                #    print(prefixo, caminho)
                valor_letra = self.tab.valor_letras[letra] if letra.islower() else 0
                sinal_sentido = 1 if sentido else -1
                n_prefixo = prefixo + letra if sentido else letra + prefixo
                self._busca_jogadas(i + sinal_sentido * (not horizontal), j + sinal_sentido * horizontal, horizontal,
                                    letras_disponiveis, n_prefixo, no[letra.lower()], sentido,
                                    pontos + valor_letra, multiplicadores,
                                    palavras_ortogonais, caminho + letra, infos + [("inter", i, j)])


    def _busca_jogadas_Trie(self, i: int, j: int, horizontal: bool,
                       letras_disponiveis: dict[str, int], 
                       prefixo: list[str, tuple[int, int]], 
                       no: dict[str, dict], conectou: bool=False, 
                       pontos: int=0, multiplicadores: int=1,
                       palavras_ortogonais: list[str]=[], infos=[]):
        #infos = infos + [(i, j)]

        if "\n" in no and sum(letras_disponiveis.values()) < self.num_letras and  conectou and self.tab.pos_vaga_ou_fora_tab(i, j):
            bonus = 50 if sum(letras_disponiveis.values()) == 0 and self.num_letras == 7 else 0
            self.jogadas.append((self.pos_i, self.pos_j, self.horizontal, prefixo, pontos * multiplicadores + sum([ponto[0] for ponto in palavras_ortogonais]) + bonus))#, palavras_ortogonais))
        
        if self.primeiro_lance and i==7 and j==7:
            conectou = True

        if i >= 15 or j >= 15:
            return

        if self.tab.tabuleiro[i][j].isdigit():
            for letra in letras_disponiveis:
                ortogonais = self.tab.get_letras_ortogonais(i, j, not horizontal)
                if letra in no and (letra in ortogonais or "*" in ortogonais):
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
                        self._busca_jogadas_Trie(i + (not horizontal), j + horizontal, horizontal, 
                                            letras_q_sobram, prefixo + letra, no[letra], conectou,
                                            pontos + valor_letra, multiplicadores * multiplicador,
                                            palavras_ortogonais + palavras_ortogonal, infos)

                elif letra == "?": #Joker
                    for possib in no:
                        ortogonais = self.tab.get_letras_ortogonais(i, j, not horizontal)
                        if possib != "\n" and (possib in ortogonais or "*" in ortogonais):
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
                                self._busca_jogadas_Trie(i + (not horizontal), j + horizontal, horizontal, 
                                                    letras_q_sobram, prefixo + possib.upper(), no[possib], conectou,
                                                    pontos, multiplicadores * multiplicador,
                                                    palavras_ortogonais + palavras_ortogonal, infos)

        else:
            return
            if (letra := self.tab.tabuleiro[i][j]).lower() in no:
                valor_letra = self.tab.valor_letras[letra] if letra.islower() else 0
                self._busca_jogadas(i + (not horizontal), j + horizontal, horizontal,
                                    letras_disponiveis, prefixo + letra, no[letra.lower()], True,
                                    pontos + valor_letra, multiplicadores,
                                    palavras_ortogonais, infos)
    """def calc_pontos(self, prefixo: list[str, tuple[int, int]]):
        pontos = 0
        for letra in prefixo:
            pontos += letra"""

def identifica_repetições(lista:list):
    repeticoes = {}
    for elem in lista:
        if elem in repeticoes:
            repeticoes[elem] += 1
        else:
            repeticoes[elem] = 0
    return { key: value for key, value in repeticoes.items() if value > 0}
    
if __name__ == "__main__":
    trie = Trie()
    trie.carrega_palavras( "br-sem-acentos.txt" )
    gaddag = Gaddag()
    gaddag.carrega_palavras( "br-sem-acentos.txt" )

    print("Carregou palavras")

    tab = Tabuleiro()
    bot_g = Gaddag_Bot( tab, trie, gaddag )
    #bot = Bot( tab, trie )


    """tab.adiciona_palavra(7, 3, True, "salona")
    tab.adiciona_palavra(0, 3, False, "tostamos")
    tab.adiciona_palavra(0, 0, True, "fretar")
    tab.adiciona_palavra(6, 8, True, 'vedem')
    tab.adiciona_palavra(0, 12, False, 'cogitEm')
    tab.adiciona_palavra(0, 8, True, "civicas")
    tab.adiciona_palavra(4, 2, True, "malho")
    tab.adiciona_palavra(6, 10, False, "daquilo")
    tab.adiciona_palavra(12, 3, True, "pilotado")"""


    tab.print_tabuleiro(True)
    #print(bot.escolhe_melhor_jogada("fretaro", True))
    #melhor_jogada = bot.escolhe_melhor_jogada("dumplso", True)
    #print(melhor_jogada)

    melhor_jogada, jogadas = bot_g.escolhe_melhor_jogada("dumplso", True)
    print(melhor_jogada)

    repeticoes = identifica_repetições(jogadas)
    print(jogadas)
    print(repeticoes)
    print(len(jogadas), sum([val for val in repeticoes.values()]))

    #tab.adiciona_palavra(*melhor_jogada[:4])
    
    #tab.print_tabuleiro(True)

    """tab.adiciona_palavra( 7, 5, True, "astro" )
    tab.adiciona_palavra(1, 9, False, "valiamos")#72
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


    #tab.print_tabuleiro(True)
