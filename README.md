# ⛓️ Simulador de Proof of Work (PoW) com Tkinter

Este projeto consiste em um **simulador de Proof of Work (Prova de Trabalho)** desenvolvido em Python, com interface gráfica utilizando a biblioteca **Tkinter**.

O objetivo do projeto é demonstrar, de forma prática e didática, o funcionamento de mecanismos de consenso utilizados em **redes descentralizadas**, como as blockchains, permitindo a visualização do processo de mineração e validação de blocos.

---

## 📌 Sobre Redes Descentralizadas

Redes descentralizadas são sistemas distribuídos onde não existe uma autoridade central responsável pelo controle dos dados ou das operações.

Em vez disso, todos os participantes (nós) colaboram entre si para manter a rede funcionando de forma segura e confiável.

Principais características:

- Ausência de um servidor central
- Maior resistência a falhas
- Maior segurança contra ataques
- Transparência das operações
- Participação coletiva na validação dos dados

Exemplo de uso: Blockchain, redes peer-to-peer (P2P), sistemas distribuídos.

---

## 🔐 Proof of Work (Prova de Trabalho)

O **Proof of Work (PoW)** é um mecanismo de consenso utilizado para validar transações e criar novos blocos em uma blockchain.

Ele funciona por meio da resolução de um problema matemático complexo, que exige alto poder computacional.

Processo simplificado:

1. Os nós competem para resolver um desafio criptográfico
2. O primeiro que encontra a solução válida cria o bloco
3. O bloco é verificado pelos demais nós
4. O bloco é adicionado à cadeia
5. O minerador recebe uma recompensa

Esse método é utilizado em redes como o **Bitcoin**.

Vantagens:
- Alta segurança
- Dificulta ataques maliciosos

Desvantagens:
- Alto consumo de energia
- Necessidade de grande poder computacional
- Baixa eficiência energética

---

## 🔄 Outras Alternativas ao Proof of Work

Além do PoW, existem outros mecanismos de consenso utilizados em redes descentralizadas:

### ✅ Proof of Stake (PoS)
A validação ocorre com base na quantidade de moedas que o usuário possui.

- Menor consumo de energia
- Mais sustentável
- Utilizado no Ethereum (atual)

### ✅ Delegated Proof of Stake (DPoS)
Os usuários elegem validadores.

- Maior velocidade
- Menor descentralização

### ✅ Proof of Authority (PoA)
Validadores são previamente autorizados.

- Alta performance
- Usado em redes privadas

### ✅ Proof of History (PoH)
Utiliza registro temporal para ordenar eventos.

- Alta escalabilidade
- Usado na Solana

### ✅ Byzantine Fault Tolerance (BFT)
Foco em tolerância a falhas.

- Alta confiabilidade
- Comum em blockchains corporativas

---

## 🖥️ Tecnologias Utilizadas

- Python
- Tkinter (Interface Gráfica)
- Bibliotecas auxiliares definidas em `requirements.txt`

---

## 📦 Instalação

Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```
Observação
A biblioteca Tkinter já vem instalada por padrão no Python.
Em algumas distribuições Linux, pode ser necessário instalar manualmente:
```bash
sudo apt-get install python3-tk
```
## ▶️ Execução
Para executar o simulador, utilize:
```bash
python main.py
```
Após a execução, a interface gráfica será exibida, permitindo acompanhar o processo de simulação do Proof of Work.

## 🎯 Objetivo do Projeto
Este projeto tem finalidade acadêmica e didática, sendo utilizado para:
- Compreender o funcionamento de blockchains
- Estudar mecanismos de consenso
- Visualizar o processo de mineração
- Aplicar conceitos de sistemas distribuídos
- Praticar programação em Python

## 📚 Aprendizados
Com o desenvolvimento deste projeto, foi possível:
- Entender o funcionamento do Proof of Work
- Compreender redes descentralizadas
- Trabalhar com interfaces gráficas em Python
- Simular processos computacionais complexos
- Consolidar conceitos de blockchain
