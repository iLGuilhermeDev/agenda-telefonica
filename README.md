# 📒 Agenda de Contatos em Python

Aplicação desktop com interface gráfica (Tkinter) e banco de dados SQLite para gerenciar contatos de forma simples e eficiente.

## ✨ Funcionalidades

- ✅ Adicionar contato (nome, telefone, e-mail)
- 🔍 Buscar contato por parte do nome
- ✏️ Atualizar dados de um contato existente
- ❌ Remover contato com confirmação
- 📋 Listar todos os contatos ordenados por nome
- 🧹 Limpar campos do formulário automaticamente
- 🖱️ Seleção rápida na tabela para edição/remoção

## 🖥️ Tecnologias utilizadas

- **Python 3** – Linguagem de programação
- **Tkinter** – Interface gráfica nativa (já inclusa no Python)
- **SQLite3** – Banco de dados local (já inclusa no Python)
- **ttk.Treeview** – Tabela interativa para exibição dos contatos

## 📦 Como executar o projeto

### Pré-requisitos
- Ter o Python 3 instalado (versão 3.6 ou superior)
- Nenhuma biblioteca adicional precisa ser instalada (tudo é biblioteca padrão)

### Passos

1. **Clone ou baixe o arquivo** `agenda_gui.py`

2. **Abra o terminal** na pasta onde está o arquivo

3. **Execute o programa**:
   ```bash
   python agenda_gui.py
O banco de dados agenda.db será criado automaticamente na primeira execução.

🧭 Como usar
Adicionar contato
Preencha os campos Nome (obrigatório), Telefone e E-mail (opcionais) e clique em Adicionar.

Visualizar todos os contatos
Os contatos aparecem automaticamente na tabela assim que o programa inicia. Clique em Mostrar todos a qualquer momento para atualizar a lista.

Buscar contato
Digite um nome (ou parte dele) no campo de busca e clique em Buscar. A tabela mostrará apenas os contatos que correspondem. Para voltar à lista completa, clique em Mostrar todos.

Atualizar um contato
Clique em qualquer linha da tabela para selecionar o contato.

Os dados aparecerão nos campos de texto.

Altere o que desejar e clique em Atualizar.

Remover um contato
Selecione o contato na tabela.

Clique em Remover.

Confirme a exclusão na caixa de diálogo.

Limpar formulário
Clique em Limpar campos para apagar os dados dos campos de texto e desabilitar os botões de Atualizar e Remover.

🗂️ Estrutura do código
text
agenda_gui.py
├── Conexão e operações com SQLite

│   ├── conectar_banco()

│   ├── criar_tabela()

│   ├── adicionar_contato()

│   ├── listar_contatos()

│   ├── buscar_contato()
│   ├── atualizar_contato()

│   └── remover_contato()

└── Classe AgendaApp (interface Tkinter)

    ├── __init__() – constrói a janela e os widgets
    
    ├── carregar_contatos()
    
    ├── buscar()
    
    ├── adicionar()
    
    ├── on_selecionar()
    
    ├── limpar_campos()
    
    ├── atualizar()

    
    └── remover()
    
📁 Banco de dados
Arquivo: agenda.db (criado automaticamente)

Tabela: contatos

id (INTEGER, chave primária, auto-incremento)

nome (TEXT, obrigatório)

telefone (TEXT)

email (TEXT)
