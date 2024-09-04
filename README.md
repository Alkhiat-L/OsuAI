# OsuAI

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1eUIJQWWizp9amvMdh9FnrZnCdss-7VQt?usp=sharing)

O Osu! é um jogo de ritmo popular que desafia o jogador a clicar em círculos, arrastar sliders e girar spinners no tempo certo com a música.
Este projeto visa aplicar técnicas de aprendizado por reforço (RL), o qual tem se tornado uma ferramenta poderosa para treinar agentes de inteligência artificial (IA) a realizar tarefas complexas, e Aprendizado por Imitação para criar uma IA capaz de jogar Osu! em alto nível. Dentro de suas capacidades, um agente deve ser capaz de realizar tarefas que exigem alta coordenação e velocidade, habilidades que também são necessárias em jogos de ritmo.
A combinação de precisão temporal, movimento do cursor e alta velocidade faz do Osu! um desafio para o modelo de IA.

## Estrutura do Projeto

O projeto é dividido em vários arquivos e pastas, cada um com um propósito específico. Abaixo estão os principais arquivos e pastas:

- `osupy`: O diretório principal do projeto, onde estão os arquivos de configuração, o modelo de IA e o agente RL.
- `tests`: O diretório onde estão os testes unitários.
- `Makefile`: O arquivo de configuração do Make que define as tarefas do projeto.
- `osupy/OsuPy.py`: O arquivo principal do projeto, onde está a lógica do jogo.
- `osupy/env.py`: O arquivo responsável por criar o ambiente Gym do projeto.
- `osupy/model.py`: O arquivo responsável por criar o modelo de IA.
- `osupy/test.py`: O arquivo responsável por permitir a visualização do modelo de IA em tempo real.
- `logs`: O diretório onde os arquivos de modelos de IA são salvos.
- `logs/best_model.zip`: O arquivo de modelo de IA que é o melhor modelo de IA treinado de acordo com o ambiente de Evaluation.

> [!NOTE]
> Os arquivos `*.py` na pasta raiz do projeto são da versão antiga do projeto, a qual foi feita para funcionar gravando a tela do jogo original, essa versão não está mais sendo atualizada. Os arquivos `*.py` na pasta `osupy` são as versões atualizadas do projeto.

## Executando o Projeto

Para executar o projeto, siga os passos abaixo:

1. Clone o repositório:

```bash
git clone https://github.com/Alkhiat-L/OsuAI.git
```

2. Crie um ambiente virtual:

```bash
cd OsuAI
python -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:

```bash
make init
```

4. Execute o projeto sem o modelo de IA:

```bash
make start
```

5. Treine o modelo de IA:

```bash
make model
```

6. Execute o projeto com o modelo de IA:

```bash
make model_test
```
