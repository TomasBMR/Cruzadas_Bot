import random

from src.Tabuleiro import Tabuleiro
from src.Trie import Trie

class Palavras_Cruzadas():
    def __init__(self, trie: Trie, num_jogadores: int=2, seed: float=None):
        #file = open(path_palavras, "r")    
        #palavras = [palavra.lower() for palavra in file.read().split("\n") if len(palavra)]

        self.trie = trie
        distr_letras = [15, 3, 6, 5, 11, 2, 3, 2, 10, 1, 0, 5, 6, 4, 10, 4, 1, 6, 7, 5, 6, 3, 0, 1, 0, 1]

        saco_letras = "? ? ? "
        for i, num_letra in enumerate(distr_letras):
            saco_letras += (chr(97 + i) + " ") * num_letra

        self.saco_letras = saco_letras.split()

        if seed is None: seed = random.random()
        self.seed = seed
        self.rand = random.Random(seed)

        self.num_jogadores = num_jogadores
        self.letras_jogadores = [self.sorteia_letras(7) for _ in range(num_jogadores)]
        self.pontos_jogadores = [0 for _ in range(num_jogadores)]

        self.tabuleiro = Tabuleiro( self.trie )

        self.contador_jogadas = 0
        self.jogador_atual = 0
        self.contador_troca_letras = 0
        self.finalizado = False
        self.jogadas = []

        
    def fazer_jogada(self, pos_i: int, pos_j: int, horizontal: bool, palavra: str, pontos: int):
        if self.finalizado:
            raise Exception("jogo finalizado")
        if pos_i == -1:#Trocar letras
            self.contador_troca_letras += 1
            letras_usadas = self.letras_jogadores[self.jogador_atual]
            
            #Retorna as letras n usadas ao saco
            #self.saco_letras += [letra for letra in letras_usadas]

        else:
            self.contador_troca_letras = 0
            letras_usadas = self.tabuleiro.adiciona_palavra(pos_i, pos_j, horizontal, palavra)
            #num_letras_usadas = sum([num_letras for num_letras in letras_usadas.values()])
        
        self.jogadas.append((pos_i, pos_j, horizontal, palavra, pontos))
        
        #remove as letras usadas da mao do jogador
        for letra in letras_usadas:
            if letra.isupper():
                letra = "?"
            self.letras_jogadores[self.jogador_atual] = self.letras_jogadores[self.jogador_atual].replace(letra, "")

        #Adiciona novas letras a mao do jogador
        self.letras_jogadores[self.jogador_atual] += self.sorteia_letras(7 - len(self.letras_jogadores[self.jogador_atual]))

        self.pontos_jogadores[self.jogador_atual] += pontos

        if len(self.letras_jogadores[self.jogador_atual]) > 0:
            self.contador_jogadas += 1
            self.jogador_atual = self.contador_jogadas % self.num_jogadores
        else:
            self.finalizado = True

        if self.contador_troca_letras >= 5:
            self.finalizado = True

        if self.finalizado:
            restos = []
            for jogador, letras in enumerate(self.letras_jogadores):
                resto = sum([self.tabuleiro.valor_letras[letra] for letra in letras if letra != "?"])
                self.pontos_jogadores[jogador] -= resto
                restos.append(resto)
            if len(self.letras_jogadores[self.jogador_atual]) == 0:
                self.pontos_jogadores[self.jogador_atual] += sum(restos)


    def sorteia_letras(self, num_letras: int):
        #print(self.saco_letras)
        novas_letras = []
        for _ in range(num_letras):
            if len(self.saco_letras) == 0:
                break
            novas_letras.append(self.rand.choice(self.saco_letras))
            self.saco_letras.pop(self.saco_letras.index(novas_letras[-1]))
        #print(novas_letras)
        #print(self.saco_letras)
        return "".join(novas_letras)


    def get_letras_jogador_atual(self):
        return self.letras_jogadores[self.jogador_atual]


    def print_saco_letras(self):
        dicionario = {}
        for letra in self.saco_letras:
            if letra in dicionario:
                dicionario[letra] += 1
            else:
                dicionario[letra] = 1
        print(dicionario)

    
    def get_infos(self):
        """Retorna estatisticas do jogo ate o momento"""
        return {"Pontos jogadores": tuple(self.pontos_jogadores),
                "Finalizado": self.finalizado, 
                "Contador_troca_letras": self.contador_troca_letras,
                "Letras res no saco": len(self.saco_letras), 
                "Letras res na mao": sum(len(letras) for letras in self.letras_jogadores), 
                "Jogaodr com letras na mao": 0 if self.letras_jogadores[0] else 1,
                "Num jogadas": self.contador_jogadas,
                "seed": self.seed}

    def print_cenario(self, tabuleiro: bool=True, infos_jogadores: bool=True, saco_letras: bool=True):
        if self.finalizado:
            print(f"Jogo finalizado")
        print(f"Rodada: {self.contador_jogadas//2}")
        if infos_jogadores:
            print(f"Vez do jogador {self.jogador_atual}")
            for jogador in range(self.num_jogadores):
                print(f"Jogador {jogador} tem {self.pontos_jogadores[jogador]} pontos")
                print(f"e as letras ({self.letras_jogadores[jogador]})")
        if tabuleiro:
            self.tabuleiro.print_tabuleiro(True)
        if saco_letras:
            self.print_saco_letras()




if __name__ == "__main__":
    path = "br-sem-acentos.txt"
    trie = Trie(path)
    jogo = Palavras_Cruzadas( trie, 2 )

    jogo.print_cenario()

    print(jogo.get_infos())