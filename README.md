# PONTEXTO

Jogo eletrônico de adivinhação de palavras inspirado na mecânica do **Contexto**, desenvolvido como Trabalho Integrador das disciplinas de **Inteligência Artificial** e **Redes de Computadores e Sistemas Distribuídos** do curso de Bacharelado em Ciência da Computação da UNESPAR.

## 1. Sobre o projeto

O PONTEXTO é um jogo de adivinhação de palavras baseado na similaridade semântica. O jogador realiza tentativas de palavras e recebe sua posição em um ranking de proximidade em relação à palavra secreta.

O projeto utiliza uma arquitetura **cliente-servidor**. O cliente é responsável pela interface gráfica e pela interação com o jogador, enquanto o servidor concentra a lógica da partida e o processamento necessário para a similaridade semântica.

Nesta etapa do projeto, estão implementadas e sendo testadas as telas iniciais, a comunicação cliente-servidor por XML-RPC, o gerenciamento básico da partida e os componentes de processamento textual e similaridade semântica.

## 2. Livro escolhido

O livro utilizado como base para o jogo é:

**O Olho de Vidro — Camilo Castelo Branco**

Fonte: Projeto Gutenberg

https://www.gutenberg.org/ebooks/26110

O conteúdo do livro é utilizado como base para o processamento textual e para a construção do vocabulário empregado pelo jogo.

## 3. Tecnologias utilizadas

### Linguagem

- **Python** — linguagem principal do projeto.

### Interface gráfica

- **Tkinter** — biblioteca utilizada para a construção da interface gráfica do cliente.
- O visual utiliza os componentes padrão disponibilizados pelo Tkinter.

### Comunicação

- **XML-RPC** — mecanismo de Remote Procedure Call utilizado para a comunicação entre cliente e servidor.
- A implementação utiliza o módulo `xmlrpc` disponível na biblioteca padrão do Python.

### Processamento de linguagem natural

- **spaCy** — utilizado para obtenção de representações vetoriais por meio de embeddings.
- **Requests** — utilizado para obtenção do conteúdo textual do livro quando o arquivo local ainda não está disponível.
- O projeto possui processamento textual próprio para normalização, tokenização e remoção de palavras de parada.

As dependências externas utilizadas diretamente pelo código estão registradas no arquivo `requirements.txt`.

## 4. Arquitetura

O projeto segue uma arquitetura cliente-servidor:

```text
                     PONTEXTO
                         │
              ┌──────────┴──────────┐
              │                     │
           CLIENTE               SERVIDOR
              │                     │
         Interface              Lógica do jogo
          Tkinter                    + IA
              │                     │
              └────── XML-RPC ──────┘
```

### Cliente

O cliente é responsável por:

- apresentar a interface gráfica;
- receber as entradas do jogador;
- enviar solicitações ao servidor;
- apresentar as respostas recebidas;
- controlar a navegação entre as telas;
- exibir o estado da partida;
- indicar visualmente quando uma tentativa está sendo enviada ao servidor.

O cliente não realiza o processamento de PLN ou o cálculo de similaridade.

### Servidor

O servidor é responsável por:

- iniciar e disponibilizar o serviço XML-RPC;
- controlar a partida;
- receber as tentativas;
- manter o histórico;
- controlar o estado do jogo;
- processar o texto do livro;
- construir o modelo semântico;
- calcular a similaridade entre palavras;
- determinar a posição das tentativas no ranking.

## 5. Estrutura do projeto

```text
projeto-final/
│
├── client/
│   ├── main.py
│   ├── network/
│   │   └── rpc_client.py
│   └── ui/
│       ├── about_screen.py
│       ├── game_screen.py
│       ├── help_screen.py
│       ├── loading_spinner.py
│       ├── menu.py
│       └── screen_manager.py
│
├── server/
│   ├── main.py
│   ├── game/
│   │   └── game_manager.py
│   ├── ia/
│   │   ├── book_loader.py
│   │   ├── semantic_model.py
│   │   └── text_processor.py
│   ├── network/
│   │   └── rpc_server.py
│   └── data/
│       └── o_olho_de_vidro.txt
│
├── shared/
│   └── constants.py
│
├── requirements.txt
└── README.md
```

A estrutura poderá ser ampliada durante o desenvolvimento para separar novos componentes de jogo, IA, testes e demais responsabilidades.

## 6. Requisitos

Para executar o projeto, é necessário ter:

- **Python 3** instalado;
- sistema operacional compatível com Python;
- **Tkinter** disponível na instalação do Python;
- acesso ao terminal/PowerShell;
- acesso à internet na primeira execução caso o livro ainda não esteja disponível localmente.

As dependências externas do projeto são:

- `requests`;
- `spacy`.

O modelo de linguagem utilizado pelo spaCy também precisa ser instalado separadamente:

```powershell
python -m spacy download pt_core_news_md
```

## 7. Instalação

### 7.1 Verificar o Python

Na raiz do projeto, execute:

```powershell
python --version
```

Caso o comando esteja disponível, será apresentada a versão instalada do Python.

### 7.2 Instalar as dependências

Na raiz do projeto, execute:

```powershell
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém as dependências externas utilizadas pelo projeto.

### 7.3 Instalar o modelo do spaCy

Depois de instalar as dependências, execute:

```powershell
python -m spacy download pt_core_news_md
```

O modelo `pt_core_news_md` é utilizado pelo servidor para gerar as representações vetoriais utilizadas no cálculo de similaridade semântica.

### 7.4 Sobre Tkinter

O Tkinter faz parte da distribuição padrão do Python em instalações que incluem esse componente e, por isso, **não deve ser adicionado ao `requirements.txt`**.

Da mesma forma, `xmlrpc`, `threading`, `random`, `re`, `unicodedata`, `collections` e `pathlib` são módulos da biblioteca padrão utilizados pelo projeto e não precisam ser instalados pelo `pip`.

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

Em outro terminal, também a partir da pasta raiz do projeto, execute:

```powershell
python -m client.main
```

A interface gráfica do PONTEXTO será aberta.

### Importante

Os comandos devem ser executados a partir da **raiz do projeto** utilizando `python -m`.

Não execute:

```powershell
cd client
python main.py
```

A execução a partir da raiz garante que os módulos `client`, `server` e `shared` sejam encontrados corretamente pelos imports.

## 9. Dados do livro

O servidor utiliza o arquivo:

```text
server/data/o_olho_de_vidro.txt
```

Caso o arquivo ainda não esteja disponível, o componente responsável pelo carregamento do livro pode obtê-lo pela internet a partir da fonte definida no projeto.

Depois que o conteúdo estiver disponível localmente, ele pode ser reutilizado sem a necessidade de uma nova obtenção.

## 10. Testes

Os componentes do projeto são testados individualmente durante o desenvolvimento.

Quando existirem módulos de teste no projeto, eles devem ser executados a partir da raiz utilizando o formato:

```powershell
python -m caminho.do.modulo_de_teste
```

A comunicação RPC também deve ser testada com o servidor em execução antes da integração completa com a interface gráfica.

## 11. Autores

**Guilherme Henrique de Sousa**

**João Vitor C. Domingos**

### Disciplinas

- Inteligência Artificial
- Redes de Computadores e Sistemas Distribuídos

### Curso

Bacharelado em Ciência da Computação

### Instituição

Universidade Estadual do Paraná — UNESPAR
