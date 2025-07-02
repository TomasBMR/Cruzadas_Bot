import numpy as np
import matplotlib.pyplot as plt
import itertools

from Trie import Trie


arvore = Trie()

file = open("br-sem-acentos.txt", "r")    
palavras = [palavra.lower() for palavra in file.read().split("\n") if len(palavra)]

for palavra in palavras:
    arvore.insere(palavra)

distr_letras = [15, 3, 6, 5, 11, 2, 3, 2, 10, 1, 0, 5, 6, 4, 10, 4, 1, 6, 7, 5, 6, 3, 0, 1, 0, 1]
lista_letras =  [[chr(97 + i)]*num_letra for i, num_letra in enumerate(distr_letras)]
#lista_letras.append(["?", "?", "?"])
saco_letras = list(itertools.chain.from_iterable(lista_letras))

print(saco_letras)


resultados = []
resultados_palavras = []

##
for i in range(1_000):
    #Distribuição uniforme de letras
    #letras = list(map(lambda t: chr(97+t), np.random.randint(0, 26, 7)))

    #distribuiçao real de letras
    letras = np.random.choice(saco_letras, 7, False)

    palavras = arvore.busca_possibilidades(''.join(letras))
    

    resultados_palavras.append((''.join(letras), palavras))
    resultados.append(len(palavras))

#print(resultados_palavras[np.argmax(resultados)], np.argmax(resultados))

print(resultados_palavras[np.argmax(resultados)], resultados[np.argmax(resultados)])

plt.hist(resultados, bins=max(resultados))
plt.axvline(np.mean(resultados), color='orange')
plt.show()
    
