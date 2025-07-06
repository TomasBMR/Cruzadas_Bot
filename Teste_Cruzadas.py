from Trie import Trie
from Palavras_Cruzadas import Palavras_Cruzadas
from Cruzadas_Bot import Bot
from time import time

path = "br-sem-acentos.txt"

trie = Trie(path)


def rodar_partida(prints:bool=False, seed:int=None):
    jogo = Palavras_Cruzadas(trie, seed=seed)
    bot = Bot(jogo.tabuleiro, trie)

    if prints: jogo.print_cenario()
    while True:
        jogada = bot.escolhe_melhor_jogada(jogo.get_letras_jogador_atual(), not jogo.contador_jogadas)
        if prints: jogo.print_cenario(tabuleiro=False, saco_letras=False)
        jogo.fazer_jogada(jogada[0][0], jogada[0][1], jogada[0][2], jogada[0][3], jogada[2])
        if prints: jogo.print_cenario(infos_jogadores=False)
        if prints: print(jogada)
        if jogo.finalizado:
            if prints: jogo.print_cenario(tabuleiro=False)
            break
        if prints: input()
    return jogo.get_infos()

num_jogos = 10
infos = []
tempos = []
for _ in range(num_jogos):
    t0 = time()
    info = rodar_partida(prints=False)
    tempo = (time() - t0)
    infos.append(info)
    tempos.append(tempo)
    print(info[0])
    print(tempo)

print(sum(tempos)/num_jogos)

#Na versao atual o jogo de seed 42 dura em media de 0.624 segundos
