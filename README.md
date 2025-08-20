## Bot Palavras Cruzadas
Um bot que joga o jogo de tabuleiro de forma quase ótima, gerando todos os lances possíveis em um determinado momento de uma partida e escolhnedo o melhor.

### Geração de Lances
Para gerar os lances disponivies uma estrutura de dados em árvore chamada Gaddag foi usada para armazenar o dicionário de palavras possíveis.
Isso permite gerar de forma eficiente cada lance ao mesmo tempo em que se calcula sua pontuação.
## Funcionamento

### Geração de Lances
No cerne do bot está uma estrutura de dados em árvore especializada chamada **Gaddag** que armazena o dicionário de palavras válidas. Essa escolha permite gerar lances de forma extremamente eficiente, especialmente para jogadas que envolvem a conexão com palavras já existentes no tabuleiro, calculando simultaneamente a pontuação de cada opção.


## TODO:
- Usar Aprendizado por Reforço para escolher entre os lances disponíveis de forma mais estratégica
- Adicionar paralelismo para executar mais partidas durante o treinamento por reforço


## Referências
- [Artigo Trie](https://www.cs.cmu.edu/afs/cs/academic/class/15451-s06/www/lectures/scrabble.pdf)
- [Artigo Gaddag](https://ericsink.com/downloads/faster-scrabble-gordon.pdf)
- [Regras Palavras Cruzadas](https://tablegames.com.br/wp-content/uploads/2017/10/palavras_cruzadas_manual_table_games.pdf)

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
