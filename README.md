## Bot Palavras Cruzadas
Um bot que gera todos os lances possíveis em um determinado momento de uma partida de palavras cruzadas e joga o melhor.

### Funcionamento
Para gerar os lances disponivies uma estrutura de dados em árvore chamada Gaddag foi usada para armazenar o dicionário de palavras possíveis.
Isso permite gerar de forma eficiente cada lance ao mesmo tempo em que se calcula sua pontuação.

O critério atual para escolha entre os lances disponíveis é a pontuação de cada um.


## TODO:
- Usar Aprendizado por Reforço para escolher entre os lances disponíveis de forma mais estratégica
- Adicionar paralelismo para executar mais partdas durante o treinamento por reforço


## Referências
- [Artigo Trie](https://www.cs.cmu.edu/afs/cs/academic/class/15451-s06/www/lectures/scrabble.pdf)
- [Artigo Gaddag](https://ericsink.com/downloads/faster-scrabble-gordon.pdf)
- [Regras Palavras Cruzadas](https://tablegames.com.br/wp-content/uploads/2017/10/palavras_cruzadas_manual_table_games.pdf)
