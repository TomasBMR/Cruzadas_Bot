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
        self.quadrados_especiais = ['600200060002006',
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

        self.valor_letras = {'a':1, 'b':3, 'c':2, 'd':2, 'e':1, 'f':4, 'g':4, 'h':4, 'i':1, 'j':7, 'l':2, 
                             'm':1, 'n':3, 'o':1, 'p':2, 'q':10, 'r':1, 's':1, 't':1, 'u':1, 'v':4, 'z':10}
    

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
            if not letra.isupper():
                if reta[pos_d + i].isdigit():# Letras maiusculas sao jokers "?"
                    pontos += self.valor_letras[letra] * (int(reta_especiais[pos_d + i]) if 1 < int(reta_especiais[pos_d + i]) <= 3 else 1)
                    if int(reta_especiais[pos_d + i]) > 3:
                        multiplicadores *= int(reta_especiais[pos_d + i])/2# Talvez a regra seja somar os multiplicadores
                else:
                    pontos += self.valor_letras[letra]
        return pontos * multiplicadores


    def palavra_horizontal(self, pos_i: int, pos_j: int, letra: str) -> str:
        """Recebe uma posição vazia e uma letra,  
          se a adição dessa letra formar uma palavra na horizontal retorna ela """
        if pos_i < 0 or pos_i > 14 or pos_j < 0 or pos_j > 14:
            raise Exception("Posição fora do tabuleiro")
        if not self.tabuleiro[pos_i][pos_j].isdigit():
            raise Exception("Posição ocupada")
            
        """je, jd = 0, 0
        for j in range(1, 15):
            if pos_j-j < 0 or self.tabuleiro[pos_i][pos_j-j].isdigit():
                je = j-1
                break

        for j in range(1, 15):
            if pos_j+j > 14 or self.tabuleiro[pos_i][pos_j+j].isdigit():
                jd = j-1
                break"""

        return self.tabuleiro[pos_i][:pos_j].split('0')[-1] + letra + self.tabuleiro[pos_i][pos_j+1:].split('0')[0]
        
        #return self.tabuleiro[pos_i][pos_j-je:pos_j] + letra + self.tabuleiro[pos_i][pos_j+1:pos_j+jd+1]
            

    def palavra_vertical(self, pos_i: int, pos_j: int, letra: str) -> str:
        """Recebe uma posição vazia e uma letra,  
          se a adição dessa letra formar uma palavra na vertical retorna ela """
        if pos_i < 0 or pos_i > 14 or pos_j < 0 or pos_j > 14:
            raise Exception("Posição fora do tabuleiro")
        if not self.tabuleiro[pos_i][pos_j].isdigit():
            raise Exception("Posição ocupada")
        
        coluna = "".join([linha[pos_j] for linha in self.tabuleiro])

        return coluna[:pos_i].split('0')[-1] + letra + coluna[pos_i+1:].split('0')[0]

    def dist_para_cima(self, pos_i: int, pos_j: int) -> int:
        """Recebe um quadrado ocupado e retorna o numero 
        de quadrados livres diretamente a cima dele -2"""
        for i in range(1, 16):
            if pos_i-i < 0:#Da pra diminuir uma iteracao mudando ordem dos if no caso em que a busca eh pra cima... mas n faz diferenca
                return i-1
            if not self.tabuleiro[pos_i-i][pos_j].isdigit():
                return i-2
        #Credo, esse geito eh uma porcaria. eh so usar split como nas função de cima

    def dist_para_esq(self, pos_i: int, pos_j: int) -> int:
        """Recebe um quadrado ocupado e retorna o numero 
        de quadrados livres diretamente a esquerda dele -2"""
        for j in range(1, 16):
            if pos_j-j < 0:
                return j-1
            if not self.tabuleiro[pos_i][pos_j-j].isdigit():
                return j-2
            
    
    def print_tabuleiro(self, espacos_especiais=False):
        print("    " + "\/ "*15)
        #print(f"   \," + '/\ '.join([str(i) for i in range(15)]))
        for i, linha in enumerate(self.tabuleiro):
            print(f"{" "}{" "*(-len(str(i))+2)+str(i)}> ", end="")
            for j, char in enumerate(linha):
                if char == "0":
                    if espacos_especiais and self.quadrados_especiais[i][j] != "0":
                        char = self.quadrados_especiais[i][j]
                    else:
                        char = "_"
                print(char + "  ", end="")
            print()



if __name__ == "__main__":
    tab = Tabuleiro()

    tab.tabuleiro[5] = "r0000ab0de00000"
    tab.tabuleiro[7] = "r0000astro00000"
    tab.tabuleiro[10]= "a000000os000000"
    tab.tabuleiro[14]= "000000000000000"

    tab.print_tabuleiro(True)

    print(tab.pontos_palavra(5, 5, False, "azarado"))
    print(tab.pontos_palavra(5, 5, False, "azar"))
    print(tab.pontos_palavra(13, 0, True, "marcado"))


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
