from src.Gaddag import Gaddag
from src.Trie import Trie

from src.Cruzadas_Bot_Gaddag import Gaddag_Bot

from src.Tabuleiro import Tabuleiro
from src.Palavras_Cruzadas import Palavras_Cruzadas

path_dicionario = "dicionarios/br-sem-acentos.txt"

trie = Trie( path_dicionario )
gaddag = Gaddag( path_dicionario )

tabuleiro = Tabuleiro( trie )
jogo = Palavras_Cruzadas( trie, 2, seed=42 )

bot = Gaddag_Bot( jogo.tabuleiro, trie, gaddag )



while True:
    jogada = bot.escolhe_melhor_jogada(jogo.get_letras_jogador_atual(), jogo.tabuleiro.pos_vaga(7, 7))
    jogo.print_cenario(tabuleiro=False)
    print(jogada[0])
    jogo.fazer_jogada(*jogada[0])#, jogada[1], jogada[2], jogada[3], jogada[4])
    
    jogo.print_cenario(infos_jogadores=False, saco_letras=False)
    
    
    if jogo.finalizado:
        jogo.print_cenario(tabuleiro=False)
        break
    input("Aperte enter para ver o Próximo lance")