path = "br-sem-acentos.txt"

file = open(path, "r")    
palavras = [palavra for palavra in file.read().split("\n") if len(palavra)]
#print(len(palavras))

j=0
k=0
for i, palavra in enumerate(palavras):
    if palavra[0].isupper():
        print(palavra, j, i)
        if palavra.capitalize() == palavras[i-1].capitalize():
            print("Aqui!!")
            print(palavras[i-1], k, i-1)
            k+=1
        #print(palavras[i+1])
        j+=1

print(j, k)