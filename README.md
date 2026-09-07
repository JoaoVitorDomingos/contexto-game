# PONTEXTO

Jogo eletrônico de adivinhação de palavras inspirado na mecânica do **Contexto**, desenvolvido como Trabalho Integrador das disciplinas de **Inteligência Artificial** e **Redes de Computadores e Sistemas Distribuídos** do curso de Bacharelado em Ciência da Computação da UNESPAR.

## 1. Sobre o projeto

O PONTEXTO é um jogo de adivinhação de palavras baseado na similaridade semântica. O jogador realiza tentativas de palavras e recebe sua posição em um ranking de proximidade em relação à palavra secreta.

O projeto utiliza uma arquitetura **cliente-servidor**. O cliente é responsável pela interface gráfica e pela interação com o jogador, enquanto o servidor concentra a lógica da partida e, na versão completa, o processamento de PLN e o cálculo da similaridade semântica.

Nesta etapa do projeto, correspondente à entrega parcial do 3º bimestre, estão sendo desenvolvidas e testadas as telas iniciais, a estrutura cliente-servidor e os componentes básicos necessários para a evolução do jogo.

## 2. Livro escolhido

O livro utilizado como base para o jogo é:

**O Olho de Vidro — Camilo Castelo Branco**

Fonte: Projeto Gutenberg

https://www.gutenberg.org/ebooks/26110

O conteúdo do livro será utilizado posteriormente como base para o processamento textual e para a construção do vocabulário empregado pelo jogo.

## 3. Tecnologias utilizadas

### Linguagem

- **Python** — linguagem principal do projeto.

### Interface gráfica

- **Tkinter** — biblioteca utilizada para a construção da interface gráfica do cliente.
- O visual adotado nesta etapa é básico, utilizando os componentes padrão disponibilizados pelo Tkinter.

### Comunicação

- **XML-RPC** — mecanismo de Remote Procedure Call utilizado para a comunicação entre cliente e servidor.
- A implementação utiliza o módulo `xmlrpc` disponível na biblioteca padrão do Python.

### Processamento de linguagem natural

Na versão completa do projeto estão previstas as seguintes tecnologias:

- **NLTK** — pré-processamento textual.
- **spaCy** — obtenção de representações vetoriais por meio de embeddings.
- **Unidecode** — normalização de caracteres e remoção de acentos.
- **Requests** — obtenção de conteúdo textual, quando necessário.

## 4. Arquitetura

O projeto segue uma arquitetura cliente-servidor:

```text
                    PONTEXTO
                       │
             ┌─────────┴─────────┐
             │                   │
          CLIENTE             SERVIDOR
             │                   │
        Interface             Lógica do
         Tkinter              jogo + IA
             │                   │
             └────── XML-RPC ────┘
```

### Cliente

O cliente é responsável por:

- apresentar a interface gráfica;
- receber as entradas do jogador;
- enviar solicitações ao servidor;
- apresentar as respostas recebidas;
- controlar a navegação entre as telas.

O cliente não realiza o processamento de PLN.

### Servidor

O servidor é responsável por:

- controlar a partida;
- receber as tentativas;
- manter o histórico;
- controlar o estado do jogo;
- futuramente realizar o processamento textual;
- futuramente gerar o ranking de similaridade;
- futuramente processar dicas e desistência.

## 5. Estrutura do projeto

```text
projeto-final/
│
├── client/
│   ├── main.py
│   ├── ui/
│   └── network/
│
├── server/
│   ├── main.py
│   ├── game/
│   ├── ia/
│   └── network/
│
├── shared/
│   └── constants.py
│
└── README.md
```

A estrutura será ampliada durante o desenvolvimento da versão completa para incluir os módulos responsáveis pelo processamento do livro, vocabulário, embeddings, similaridade e ranking.

## 6. Requisitos

Para executar o projeto, é necessário ter:

- Python 3 instalado;
- sistema operacional compatível com Python e Tkinter;
- acesso ao terminal/PowerShell.

A versão atual utiliza principalmente bibliotecas da própria distribuição padrão do Python. As bibliotecas de IA serão necessárias conforme os módulos de PLN forem implementados.

## 7. Instalação

### 7.1 Verificar o Python

No terminal, execute:

```powershell
python --version
```

Caso o comando esteja disponível, será apresentada a versão instalada do Python.

### 7.2 Instalar dependências

Na etapa atual, não há necessidade de instalar bibliotecas externas para executar as telas e a comunicação básica, pois Tkinter e XML-RPC fazem parte da distribuição padrão do Python.

Quando os módulos de IA forem implementados, as dependências externas necessárias deverão ser instaladas.

Caso seja criado um arquivo `requirements.txt`, a instalação poderá ser feita com:

```powershell
pip install -r requirements.txt
```

## 8. Como executar

O projeto utiliza dois processos independentes: **servidor** e **cliente**.

É necessário abrir dois terminais.

### Terminal 1 — Servidor

Primeiro, entre na pasta raiz do projeto:

```powershell
cd caminho/para/o/projeto
```

Depois execute:

```powershell
python -m server.main
```

O servidor permanecerá em execução aguardando as solicitações do cliente.

### Terminal 2 — Cliente

Em outro terminal, também a partir da pasta raiz do projeto:

```powershell
python -m client.main
```

A interface gráfica do PONTEXTO será aberta.

### Importante

Os comandos devem ser executados a partir da **raiz do projeto** utilizando `python -m`. Isso garante que os módulos `client`, `server` e `shared` sejam encontrados corretamente pelos imports.

## 9. Testes

Os componentes do projeto são testados individualmente durante o desenvolvimento.

Para executar um teste a partir da raiz do projeto, utilize o módulo correspondente. Por exemplo:

```powershell
python -m server.game.test_game_manager
```

Para testar a comunicação RPC:

1. iniciar o servidor;
2. abrir outro terminal;
3. executar o teste do cliente RPC.

Exemplo:

```powershell
python -m server.network.test_rpc_server
```

Os testes são utilizados durante o desenvolvimento para verificar o funcionamento da comunicação e da lógica antes da integração com a interface gráfica.

## 10. Autores

**Guilherme Henrique de Sousa**

**João Vitor C. Domingos**

### Disciplinas

- Inteligência Artificial
- Redes de Computadores e Sistemas Distribuídos

### Curso

Bacharelado em Ciência da Computação

### Instituição

Universidade Estadual do Paraná — UNESPAR
