def palavra_to_lista(palavra:str) -> list:
    return [(char, ()) for char in palavra]

class Tabuleiro:
    def __init__(self, tabuleiro: list[str] = None):
        if tabuleiro is None:
           tabuleiro = ["0" * 15 for _ in range(15)]

        self.tabuleiro: list[str] = tabuleiro

        #0 quadrado vazio
        #2 dobro da letra
        #3 triplo da letra
        #4 dobro da palavra
        #6 triplo da palavra
        self.quadrados_especiais = [
                        '600200060002006',
                        '040003000300040',
                        '004000202000400',
                        '200400020004002',
                        '000040000040000',
                        '030003000300030',
                        '002000202000200',
                        '600200040002006',#meio
                        '002000202000200',
                        '030003000300030',
                        '000040000040000',
                        '200400020004002',
                        '004000202000400',
                        '040003000300040',
                        '600200060002006']

        self.valor_letras = {'a':1, 'b':3, 'c':2, 'd':2, 'e':1, 'f':4, 'g':4, 'h':4, 'i':1, 'j':7, 'l':2, 'm':1, 'n':3, 
                             'o':1, 'p':2, 'q':10, 'r':1, 's':1, 't':1, 'u':1, 'v':4, 'x':8, 'z':10}
    

    def adiciona_palavra(self, pos_i: int, pos_j: int, horizontal: bool, palavra: str) -> str:
        """Recebe uma posicao, uma direcao e uma palavra
        Insere essa palavra no tabuleiro e retorna as letras utilizadas"""
        if pos_i < 0 or pos_i > 14 or pos_j < 0 or pos_j > 14:
            raise Exception("Posição fora do tabuleiro")
        pos_d = pos_j if horizontal else pos_i
        if pos_d + len(palavra) > 15:
            raise Exception("Palavra sai do tabuleiro")
        
        if horizontal:
            antes = self.tabuleiro[pos_i][pos_j:pos_j + len(palavra)]
            self.tabuleiro[pos_i] = self.tabuleiro[pos_i][:pos_j] + palavra + self.tabuleiro[pos_i][pos_j + len(palavra):]

        else:
            coluna = "".join([linha[pos_j] for linha in self.tabuleiro])
            antes = coluna[pos_i:pos_i + len(palavra)]

            coluna = coluna[:pos_i] + palavra + coluna[pos_i+len(palavra):]
            self.tabuleiro = [lin[:pos_j] + coluna[i] + lin[pos_j + 1:] for i, lin in enumerate(self.tabuleiro)]
        #print(antes)
        #print(f"Palavra fez {self.pontos_palavra(pos_i, pos_j, horizontal, palavra)} pontos")
        letras_usadas = [letra_p for letra_a, letra_p in zip(antes, palavra) if letra_a.isdigit()]
        return "".join(letras_usadas)
        """dict_letras_usadas = {}
        for letra in letras_usadas:
            if letra not in dict_letras_usadas:
                dict_letras_usadas[letra] = 1
            else:
                dict_letras_usadas[letra] += 1
        return dict_letras_usadas"""


    def pontos_palavra(self, pos_i: int, pos_j: int, horizontal: bool, palavra: str):
        """Recebe uma posicao, uma direcao e uma palavra
        Retorna o numero de pontos q essa palavra faria 
        se escrita a partir da posicao dada"""
        if pos_i < 0 or pos_i > 14 or pos_j < 0 or pos_j > 14:
            raise Exception("Posição fora do tabuleiro")
        
        pos_d = pos_j if horizontal else pos_i
        if pos_d + len(palavra) > 15:
            raise Exception("Palavra sai do tabuleiro")

        reta = self.tabuleiro[pos_i] if horizontal else "".join([linha[pos_j] for linha in self.tabuleiro])
        reta_especiais = self.quadrados_especiais[pos_i] if horizontal else "".join([linha[pos_j] for linha in self.quadrados_especiais])

        pontos = 0
        multiplicadores = 1

        for i, letra in enumerate(palavra):
            if reta[pos_d + i].isdigit():
                if letra.islower():# Letras maiusculas sao jokers "?" e não pontuam
                    pontos += self.valor_letras[letra] * (int(reta_especiais[pos_d + i]) if 1 < int(reta_especiais[pos_d + i]) <= 3 else 1)
                if int(reta_especiais[pos_d + i]) > 3:
                        multiplicadores *= int(reta_especiais[pos_d + i])//2# Talvez a regra seja somar os multiplicadores
            elif letra.islower():
                pontos += self.valor_letras[letra]
        return pontos * multiplicadores


    def palavra_ortogonal(self, pos_i: int, pos_j: int, horizontal:bool, letra:str) -> tuple[int, int, str]:#talvez retornar a pontuação da palavra seja uma boa
        if pos_i < 0 or pos_i > 14 or pos_j < 0 or pos_j > 14:
            raise Exception("Posição fora do tabuleiro")
        if self.tabuleiro[pos_i][pos_j].isalpha():
            raise Exception("Posição ocupada")
        
        if horizontal:
                     
            if self.pos_vaga_ou_fora_tab(pos_i, pos_j+1):
                trecho_dir = ""
            else:
                trecho_dir = self.tabuleiro[pos_i][pos_j+1:].split('0')[0]
            if self.pos_vaga_ou_fora_tab(pos_i, pos_j-1):
                trecho_esq = ""
            else:
                trecho_esq = self.tabuleiro[pos_i][:pos_j].split('0')[-1]

            return (pos_i, pos_j - len(trecho_esq), horizontal, trecho_esq + letra + trecho_dir)
            if self.pos_vaga_ou_fora_tab(pos_i, pos_j+1) and self.pos_vaga_ou_fora_tab(pos_i, pos_j-1):
                return (pos_i, pos_j, horizontal, letra)
            """inicio_palavra, fim_palavra = -1, -1
            for j, char in enumerate(self.tabuleiro[pos_i]):#Deu errado...
                if char.isalpha() or j == pos_j:
                    if inicio_palavra == -1:
                        inicio_palavra = j
                else:
                    if j > pos_j:
                        fim_palavra = j# - 1
                        break
                    inicio_palavra = -1
            if fim_palavra == -1: fim_palavra = len(self.tabuleiro)
            resultado_teste = (pos_i, inicio_palavra, horizontal, self.tabuleiro[pos_i][inicio_palavra:pos_j] + letra + self.tabuleiro[pos_i][pos_j+1:fim_palavra])
            return resultado_teste"""
            trecho_esq = self.tabuleiro[pos_i][:pos_j].split('0')[-1]
            return (pos_i, pos_j - len(trecho_esq), horizontal, trecho_esq + letra + self.tabuleiro[pos_i][pos_j+1:].split('0')[0])

        else:
            if self.pos_vaga_ou_fora_tab(pos_i+1, pos_j) and self.pos_vaga_ou_fora_tab(pos_i-1, pos_j):
                return (pos_i, pos_j, horizontal, letra)
            """inicio_palavra, fim_palavra = -1, -1
            for i, linha in enumerate(self.tabuleiro):# Deu errado...
                #print(i, linha[pos_j].isalpha(),  i == pos_i)
                if linha[pos_j].isalpha() or i == pos_i:
                    if inicio_palavra == -1:
                        inicio_palavra = i
                else:
                    if i > pos_i:
                        fim_palavra = i# - 1
                        break
                    inicio_palavra = -1
            if fim_palavra == -1: fim_palavra = len(self.tabuleiro[pos_j])
            #palavra = "".join([linha[pos_j] for linha in self.tabuleiro[inicio_palavra:pos_i]]) + letra + "".join([linha[pos_j] for linha in self.tabuleiro[pos_i+1:fim_palavra]])
            palavra = [linha[pos_j] for linha in self.tabuleiro[inicio_palavra:fim_palavra]]
            palavra[pos_i - inicio_palavra] = letra
            resultado_teste = (inicio_palavra, pos_j, horizontal, "".join(palavra))
            return resultado_teste"""
            coluna = "".join([linha[pos_j] for linha in self.tabuleiro])
            trecho_cima = coluna[:pos_i].split('0')[-1]
            return (pos_i - len(trecho_cima), pos_j, horizontal, trecho_cima + letra + coluna[pos_i+1:].split('0')[0])
            if resultado_certo != resultado_teste:
                print(resultado_certo)
                print(resultado_teste)
                print(inicio_palavra, fim_palavra)
                print(pos_i)
                print("".join([linha[pos_j] for linha in self.tabuleiro[inicio_palavra:pos_i]]), "|", "".join([linha[pos_i] for linha in self.tabuleiro[pos_i+1:fim_palavra]]))
                self.print_tabuleiro()
                raise Exception("Aqui oh")
            return resultado_certo


    def dist_cima_esq(self, pos_i: int, pos_j: int, horizontal: bool) -> int:
        """Recebe um quadrado ocupado e retorna o numero 
        de quadrados livres diretamente a cima dele -2"""
        if pos_i < 0 or pos_i > 14 or pos_j < 0 or pos_j > 14:
            raise Exception("Posição fora do tabuleiro")
        """if self.tabuleiro[pos_i+1][pos_j].isalpha() or self.tabuleiro[pos_i-1][pos_j].isalpha() or self.tabuleiro[pos_i][pos_j+1].isalpha() or self.tabuleiro[pos_i][pos_j-1].isalpha():
            raise Exception("Posição não ocupada")"""
        
        if horizontal:
            lin = "".join(["a" if char.isalpha() or j == pos_j else "0" for j, char in enumerate(self.tabuleiro[pos_i][:pos_j])])
            split = lin.split("a")
        else:
            coluna = "".join(["a" if linha[pos_j].isalpha() or i == pos_i else "0" for i, linha in enumerate(self.tabuleiro[:pos_i])])
            split = coluna.split("a")
        return len(split[-1]) - (len(split)>1)
    

    def alguma_letra_adjacente(self, pos_i: int, pos_j: int):
        if pos_i < 0 or pos_i > 14 or pos_j < 0 or pos_j > 14:
            raise Exception("Posição fora do tabuleiro")
        v, h = False, False
        if pos_i + 1 <= 14:
            h = self.tabuleiro[pos_i+1][pos_j].isalpha()
        if pos_i - 1 >= 0:
            h = h or self.tabuleiro[pos_i-1][pos_j].isalpha()
        if pos_j + 1 <= 14:
            v = self.tabuleiro[pos_i][pos_j+1].isalpha()
        if pos_j - 1 >= 0:
            v = v or self.tabuleiro[pos_i][pos_j-1].isalpha()
        return h or v


    def pos_vaga(self, pos_i: int, pos_j: int):
        """True se a posicao esta vaga e False caso contrario.
        retorna False se posição estiver fora do tabuleiro"""
        if pos_i < 0 or pos_i > 14 or pos_j < 0 or pos_j > 14:
            raise Exception("Posição fora do tabuleiro")
        return self.tabuleiro[pos_i][pos_j].isdigit()
    
    def pos_vaga_ou_fora_tab(self, pos_i: int, pos_j: int):
        if pos_i < 0 or pos_i > 14 or pos_j < 0 or pos_j > 14:
            return True
        return self.tabuleiro[pos_i][pos_j].isdigit()

    
    def print_tabuleiro(self, espacos_especiais=False, func_teste=None):
        print("    " + "".join([f"|{x%10}|" for x in range(15)]))
        #print("    " + "|0/" + "|/ "*6 + "|7/ " + "|/ "*7)
        #print(f"   \," + '/\ '.join([str(i) for i in range(15)]))
        for i, linha in enumerate(self.tabuleiro):
            print(f"{" "}{" "*(-len(str(i))+2)+str(i)}> ", end="")
            for j, char in enumerate(linha):
                if char == "0":
                    if espacos_especiais and self.quadrados_especiais[i][j] != "0":
                        char = self.quadrados_especiais[i][j]
                    else:
                        char = "_"
                if not char.isalpha() and func_teste is not None:
                    char = "1" if func_teste(i, j) else "0"
                print(char + "  ", end="")
            print()
        print()



if __name__ == "__main__":
    tab = Tabuleiro()

    #tab.tabuleiro[5] = "r0000ab0de00000"
    #tab.tabuleiro[7] = "00000astro00000"
    #tab.tabuleiro[10]= "a000000os000000"
    #tab.tabuleiro[14]= "000000000000000"

    tab.print_tabuleiro(True)

    print(tab.adiciona_palavra(7, 5, True, "astro"))
    tab.print_tabuleiro(True)

    print(tab.adiciona_palavra(7, 5, False, "azar"))
    tab.print_tabuleiro(True)

    print(tab.adiciona_palavra(10, 5, True, "roupas"))
    tab.print_tabuleiro(True)

    print(tab.adiciona_palavra(9, 1, True, "alara"))
    tab.print_tabuleiro(True)

    print(tab.palavra_ortogonal(8, 6, True, "a"))

    """print(tab.dist_cima_esq(9, 0, False))
    print(tab.dist_cima_esq(9, 0, True))
    print(tab.dist_cima_esq(10, 5, True))
    print(tab.dist_cima_esq(10, 6, False))"""
    """print(tab.pontos_palavra(5, 5, False, "azarado"))
    print(tab.pontos_palavra(5, 5, False, "azar"))
    print(tab.pontos_palavra(13, 0, True, "marcado"))"""

    """print(tab.dist_para_cima(6, 5))
    print(tab.dist_para_cima(4, 5))"""
    """print(tab.palavra_horizontal(5, 7, "x"))
    print(tab.palavra_horizontal(10, 6, "x"))
    print(tab.palavra_horizontal(14, 0, "x"))
    print(tab.palavra_horizontal(14, 14, "x"))
    print(tab.palavra_horizontal(14, 9, "x"))
    print(tab.palavra_horizontal(15, 9, "x"))
    print(tab.palavra_horizontal(14, 10, "x"))"""

    """print(tab.palavra_vertical(4, 5, "x"))
    print(tab.palavra_vertical(6, 5, "x"))
    print(tab.palavra_vertical(6, 6, "x"))
    print(tab.palavra_vertical(6, 7, "x"))
    print(tab.palavra_vertical(6, 0, "x"))"""
