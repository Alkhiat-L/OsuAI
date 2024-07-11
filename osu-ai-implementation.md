# Osu! Estratégia de implementação de IA usando Gravações de outros jogadores

## 1. Coleta de dados e pré-processamento

- Coletar gravações de outros jogadores de Osu!.
- Extrair informações importantes:
  - Movimentos do cursor
  - Teclas pressionadas
  - Posição das notas e o timing
  - Score e acurácia.

## 2. Environment Setup

- Criar um ambiente de Osu! usando Pygame:
  - Implementar as mecânicas básicas do jogo (surgimento de notas, pontuação, etc.)
  - Projetar um ambiente de observação que inclua:
    - Posição atual do mouse
    - Posição da próxima nota e o timing
    - Score e acurácia atual
  - Definir o espaço de ação:
    - Movimento do mouse (dx, dy)
    - Clicks do mouse

## 3. Reinforcement Learning Framework

- É possivel fazer um ambiente próximo ao do Gym, afinal não há muito para onde ir além do básico:
  - `reset()`: Iniciar um novo jogo
  - `step(action)`: Processar um "frame" da gameplay
  - `render()`: Visualizar o estado do jogo

## 4. Reward Function

- Projetar uma função de recompensa que leve em conta a:
  - Acurácia
  - Manter o combo
  - A perda de HP
  - A pontuação

## 5. AI Model

- A gente ainda precisa decidir se vai continuar com o modelo de PPO ou se vai tentar algum outro
- Desenvolver um modelo que seja capaz de receber os dados do Osu!.

## 6. Training Pipeline

- Loop de treino:
  - Receber ações da política (Policy)
  - Executar ações no ambiente
  - Computar as recompensas e atualizar a política

## 7. Imitation Learning Integration

- Usar os dados recolhidos através das gravações para melhorar o modelo:
  - Prétreinar o modelo com os dados da gravação
  - Aperfeiçoar (Fine-tune) usando Aprendizado por Reforço

## 8. Evaluation and Iteration

- Testar a IA em vários mapas de Osu!.
- Analizar a performance and iterar a estrutura do modelo, sobre a função de recompensa, ou o processo de treinamento se necessário
