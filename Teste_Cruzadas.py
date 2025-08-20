import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import time
import cProfile

from Trie import Trie
from Gaddag import Gaddag
from Palavras_Cruzadas import Palavras_Cruzadas
from Cruzadas_Bot import Bot
from Cruzadas_Bot_Gaddag import Gaddag_Bot



path = "br-sem-acentos.txt"

trie = Trie( path )
gaddag = Gaddag( path )
print("Palavras_Carregadas")

def rodar_partida_bot_Trie(prints: bool=False, seed: int=None):
    jogo = Palavras_Cruzadas(trie, seed=seed)
    bot = Bot(jogo.tabuleiro, trie)
    
    try:
        if prints: jogo.print_cenario()
        while True:
            jogada = bot.escolhe_melhor_jogada(jogo.get_letras_jogador_atual(), jogo.tabuleiro.pos_vaga(7, 7))
            if prints: jogo.print_cenario(tabuleiro=False)
            #print(jogada)
            jogo.fazer_jogada(jogada[0], jogada[1], jogada[2], jogada[3], jogada[4])
            #jogo.fazer_jogada(jogada[0][0], jogada[0][1], jogada[0][2], jogada[0][3], jogada[2])
            if prints: jogo.print_cenario(infos_jogadores=False, saco_letras=False)
            #if prints: jogo.tabuleiro.print_tabuleiro(True, func_teste=lambda i, j: jogo.tabuleiro.letras_ortogonais[i][j][True])
            #if prints: jogo.tabuleiro.print_tabuleiro(True, func_teste=lambda i, j: jogo.tabuleiro.letras_ortogonais[i][j][False])
            if prints: print(jogada)
            if jogo.finalizado:
                if prints: jogo.print_cenario(tabuleiro=False)
                if jogo.get_infos()[0][0]<1 or jogo.get_infos()[0][1]<1:
                    raise Exception("negativo parca!")
                break
            if prints: input()
    except:
        raise Exception(f"Nao sei qual o erro mas a seed eh {jogo.seed}")
    return jogo.get_infos()

def rodar_partida_bot_Gaddag(prints: bool=False, seed: int=None):
    jogo = Palavras_Cruzadas(trie, seed=seed)
    bot = Gaddag_Bot(jogo.tabuleiro, trie, gaddag)
    
    try:
        if prints: jogo.print_cenario()
        while True:
            jogada = bot.escolhe_melhor_jogada(jogo.get_letras_jogador_atual(), jogo.tabuleiro.pos_vaga(7, 7))
            if prints: jogo.print_cenario(tabuleiro=False)
            #print(jogada)
            jogo.fazer_jogada(jogada[0], jogada[1], jogada[2], jogada[3], jogada[4])
            #jogo.fazer_jogada(jogada[0][0], jogada[0][1], jogada[0][2], jogada[0][3], jogada[2])
            if prints: jogo.print_cenario(infos_jogadores=False, saco_letras=False)
            #if prints: jogo.tabuleiro.print_tabuleiro(True, func_teste=lambda i, j: jogo.tabuleiro.letras_ortogonais[i][j][True])
            #if prints: jogo.tabuleiro.print_tabuleiro(True, func_teste=lambda i, j: jogo.tabuleiro.letras_ortogonais[i][j][False])
            if prints: print(jogada)
            if jogo.finalizado:
                if prints: jogo.print_cenario(tabuleiro=False)
                if jogo.get_infos()[0][0]<1 or jogo.get_infos()[0][1]<1:
                    raise Exception("negativo parca!")
                break
            if prints: input()
    except:
        raise Exception(f"Nao sei qual o erro mas a seed eh {jogo.seed}")
    return jogo.get_infos()


def compara_funcionamento_bots(prints: bool=False, seed: int=None):
    jogo = Palavras_Cruzadas(trie, seed=seed)
    #bot = Bot(jogo.tabuleiro, trie)
    bot1 = Bot( jogo.tabuleiro, trie )
    bot2 = Gaddag_Bot( jogo.tabuleiro, trie, gaddag )
    try:
        if prints: jogo.print_cenario()
        while True:
            jogada_certa = bot1.escolhe_melhor_jogada(jogo.get_letras_jogador_atual(), jogo.tabuleiro.pos_vaga(7, 7))
            jogada_teste = bot2.escolhe_melhor_jogada(jogo.get_letras_jogador_atual(), jogo.tabuleiro.pos_vaga(7, 7))
            if jogada_certa[:4] != jogada_teste[:4]:

                print("Diferentes!!")
                print(jogada_certa)
                print(jogada_teste)
                if jogada_certa[4] != jogada_teste[4]:
                    raise Exception("Diferente!")
            else:
                pass
                #print("Igual")

            if prints: jogo.print_cenario(tabuleiro=False)
            #print(jogada_certa)
            jogo.fazer_jogada(jogada_certa[0], jogada_certa[1], jogada_certa[2], jogada_certa[3], jogada_certa[4])
            #jogo.fazer_jogada(jogada[0][0], jogada[0][1], jogada[0][2], jogada[0][3], jogada[2])
            if prints: jogo.print_cenario(infos_jogadores=False, saco_letras=False)
            #if prints: jogo.tabuleiro.print_tabuleiro(True, func_teste=lambda i, j: jogo.tabuleiro.letras_ortogonais[i][j][True])
            #if prints: jogo.tabuleiro.print_tabuleiro(True, func_teste=lambda i, j: jogo.tabuleiro.letras_ortogonais[i][j][False])
            if prints: print(jogada_certa)
            if jogo.finalizado:
                if prints: jogo.print_cenario(tabuleiro=False)
                if jogo.get_infos()[0][0]<1 or jogo.get_infos()[0][1]<1:
                    raise Exception("negativo parca!")
                break
            if prints: input()
    except:
        raise Exception(f"Nao sei qual o erro mas a seed eh {jogo.seed}")
    return jogo.get_infos()



"""def aux():
    return [1]

def teste():
    lista = []
    for _ in range(1_000_000):
        #lista += [1]
        lista.append(1)
    return lista

t0 = time()
teste()
print(time()-t0)"""
#cProfile.run('teste()')


#cProfile.run('rodar_partida(prints=False, seed=42)')

#jogadas = compara_funcionamento_bots(prints=True, seed=0)[-1]


#jogadas = rodar_partida(prints=True, seed=42)[-1]

#print([jogada[:5] for jogada in jogadas])

num_jogos = 1
infos = []
tempos = []
for i in range(num_jogos):
    print(i)
    t0 = time()
    info = rodar_partida_bot_Trie(prints=False, seed=i)
    tempo = (time() - t0)
    infos.append(info)
    tempos.append(tempo)
    #print(info[0])
    print(tempo)

print(f"media tempo Trie: {np.mean(tempos)}")
print(f"variancia tempo Trie: {np.var(tempos)}")


num_jogos = 50
infos = []
tempos = []
for i in range(num_jogos):
    print(i)
    t0 = time()
    info = rodar_partida_bot_Gaddag( prints=False )
    tempo = (time() - t0)
    infos.append(info)
    tempos.append(tempo)
    #print(info[0])
    print(tempo)


pontos_1 = []
pontos_2 = []
v_d_e = []
letras_no_saco = []
letras_na_mao = []
num_jogos_sem_sobra = 0

v = 0
d = 0
e = 0
for info in infos:
    pontos_1.append(info[0][0])
    pontos_2.append(info[0][1])
    v_d_e.append(info[0][0] - info[0][1])
    if info[0][0] - info[0][1]>0:
        v += 1
        v_d_e.append(1)
    elif info[0][0] - info[0][1]<0:
        d += 1
        v_d_e.append(0)
    else:
        e += 1
        v_d_e.append(-1)
    if info[2] == 0:
        num_jogos_sem_sobra += 1
    else:
        letras_no_saco.append(info[3])
        letras_na_mao.append(info[3])


if num_jogos > 0:
    print(f"media tempo: {np.mean(tempos)}")
    print(f"variancia tempo: {np.var(tempos)}")
    print(v, d, e)
    print(num_jogos_sem_sobra)


    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)


    (_, bins, _) = ax1.hist(pontos_1, color='orange', alpha=0.5, ec='k', label='pnts j_1')
    ax1.axvline(np.mean(pontos_1), color='orange', label=f'media j_1: {np.mean(pontos_1)}')
    ax1.hist(pontos_2, bins=bins, color='blue', alpha=0.5, ec='k', label='pnts j_2')
    ax1.axvline(np.mean(pontos_2), color='blue', label=f'media j_2: {np.mean(pontos_2)}')
    ax1.set_title("hist pontos primeiro e segundo jogador")
    ax1.legend()

    ax2.hist(v_d_e, alpha=0.6)
    ax2.axvline(np.mean(v_d_e), label=f'media dif: {np.mean(v_d_e)}')
    ax2.axvline(np.mean(v_d_e), label=f'mediana dif: {np.median(v_d_e)}')

    ax2.set_title("hist diferenca jogadores")
    ax2.legend()

    ax3.hist(letras_na_mao)
    ax3.hist(letras_no_saco)
    ax3.set_title("hist num letras restantes na mao e no saco")

    ax4.hist(tempos)
    ax4.axvline(np.mean(tempos), label=f'media tempo: {np.mean(tempos)}')
    ax4.legend()
    ax4.set_title("hist duracao das partidas")


    plt.tight_layout()
    plt.show()


#Na primeira versao o jogo de seed 42 durava em media 0.624 segundos
#Na versao atual o jogo de seed 42 dura em media 0.443 segundos

#0.624
#0.544 nao copia o dict de letras desnecessariamente
#0.465 Checa antes de fazer splits na palavra_ortogonal
#0.459 armazena trecho splitado para n fazer splt repetido
#0.474 (nao uso) faz loop ao invez de split para calcular palavra_ortogonal
#0.409 na busca por jogadas nao reotorna e soma a lista de resposta, apenas faz append em uma variavel da classe
#0.406 (nao tenho certeza se fez diferenca) Não passa a variável num_letra no método busca_jogadas
#0.443 (nao sei pq ficou mais devagar...) Remove alguns retornos desnecessarios 
#Agora vou adicionar as letras joker e essa métrica vai quebrar...