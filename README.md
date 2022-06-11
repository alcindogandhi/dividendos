# Dividendos

Este projeto consiste em um conjunto de scripts Python para análise de dividendos das empresas listadas na [B3](https://www.b3.com.br/) para possível formação de uma carteira previdenciária, seguindo o método Barsi.

Os dados sobre as diversas empresas são obtidos por meio do [Yahoo Finance](https://finance.yahoo.com/), por meio da biblioteca [yfinance](https://pypi.org/project/yfinance/). Esses dados são obtidos por meio do script [yahooData.py](https://github.com/alcindogandhi/dividendos/blob/main/src/yahooData.py), que os salva em uma arquivo JSON de mesmo nome. Devido à quantidade de dados baixados e o tempo de acesso ao Yahoo Finance, este script apresenta um longo tempo de execução.

O processamento dos dados é feito pelo script [listaDividendos.py](https://github.com/alcindogandhi/dividendos/blob/main/src/listaDividendos.py), que importa os dados de dividendos em JSON obtidos na etapa anterior e gera um aquivo CSV com as seguintes estatísticas calculadas para cada ativo:

* DIV ULT: Dividendos do ativo pagos no último ano.
* DIV MEDIO: Média dos dividendos do ativo no período.
* DIV MEDIANA: Mediana dos dividendos do ativo no período.
* PRECO ATUAL: Preço de fechamento do ativo.
* TAXA ULT: Taxa de retorno dos dividendos considerando o dividendo pago no último ano.
* TAXA M: Taxa de retorno dos dividendos considerando a média dos dividendos.
* TAXA MD: Taxa de retorno dos dividendos considerando a mediana dos dividendos.

Cada um dos referidos scripts podem ser importados como um módulo e usados para análises posteriores.
