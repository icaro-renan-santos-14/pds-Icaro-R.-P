# API Petshop

Projeto da disciplina de Programacao no Desenvolvimento de Sistemas.

Este repositorio vai crescer durante todo o trimestre. Comecamos com uma API
simples usando Flask e sqlite3, e ao longo das aulas ela vai ganhar ORM,
separacao em camadas, login e, no final, um front-end em React.

Na **Aula 02**, o acesso ao SQLite passou a usar **Flask-SQLAlchemy**. As
classes `Dono` e `Pet` representam as tabelas, e as rotas usam objetos Python
para consultar, cadastrar, atualizar e remover registros.

**Nao apague nem recomece o projeto a cada aula.** O codigo evolui aqui dentro.

## Como rodar

### No GitHub Codespaces (recomendado)

1. Clique em **Code > Codespaces > Create codespace on main**.
2. Espere a preparacao terminar. As dependencias sao instaladas automaticamente.
3. No terminal, entre na pasta do back-end, atualize as dependencias (tambem
   necessario em um Codespace que ja existia) e crie o banco:

```
cd backend
pip install -r requirements.txt
python criar_banco.py
```

4. Suba o servidor:

```
python app.py
```

### Na sua maquina

```
cd backend
pip install -r requirements.txt
python criar_banco.py
python app.py
```

O servidor sobe em `http://localhost:5000`.

## Como testar as rotas

Abra o arquivo `backend/requisicoes.http` com a extensao **REST Client** e clique
em **Send Request** acima de cada requisicao. A resposta aparece ao lado.
Execute os exemplos na ordem: as requisicoes nomeadas `novoDono` e `novoPet`
fornecem os IDs usados para atualizar e remover os cadastros de teste.

O banco agora fica em `backend/instance/petshop.db`. Tanto `instance/` quanto
`*.db` estao no `.gitignore`. Rode `python criar_banco.py` ao abrir o projeto
em um lugar novo: ele cria as tabelas e insere os 3 donos e 5 pets de exemplo
somente se nao houver donos cadastrados. Rodar novamente preserva os dados.

O antigo `backend/petshop.db` da Aula 01 nao e mais usado. Os dados dele nao
sao transferidos automaticamente para o novo arquivo. Se precisar guarda-los,
faca uma copia antes de remover o banco antigo.

## Modelo de dados

**donos**

| campo    | tipo    | observacao     |
|----------|---------|----------------|
| id       | INTEGER | chave primaria |
| nome     | TEXT    | obrigatorio    |
| telefone | TEXT    | obrigatorio    |

**pets**

| campo   | tipo    | observacao                      |
|---------|---------|---------------------------------|
| id      | INTEGER | chave primaria                  |
| nome    | TEXT    | obrigatorio                     |
| especie | TEXT    | obrigatorio                     |
| idade   | INTEGER | obrigatorio                     |
| dono_id | INTEGER | chave estrangeira para donos.id |

## Contrato das rotas

As cinco rotas de **donos** e as cinco rotas de **pets** usam ORM no `app.py`.
Os metodos `to_dict()` convertem os objetos em dicionarios para a resposta JSON.

### Donos

| Metodo | URL | Resultado |
|--------|-----|-----------|
| GET | `/donos` | `200`: lista de donos |
| GET | `/donos/{id}` | `200`: dono; `404`: dono inexistente |
| POST | `/donos` | `201`: dono criado; `400`: dados invalidos |
| PUT | `/donos/{id}` | `200`: dono atualizado; `400`: dados invalidos; `404`: dono inexistente |
| DELETE | `/donos/{id}` | `200`: dono removido; `404`: dono inexistente |

POST e PUT recebem `nome` e `telefone` como textos nao vazios. Dados ausentes
ou invalidos retornam `{"erro": "Informe nome e telefone"}`. Um dono
inexistente retorna `{"erro": "Dono nao encontrado"}`.

Para preservar o relacionamento, DELETE de um dono que ainda possui pets
retorna `400` com `{"erro": "Dono possui pets cadastrados"}`. Transfira ou
remova os pets antes de excluir o dono.

### GET /pets

Lista todos os pets. A resposta traz o **nome do dono**, e nao apenas o
`dono_id`. O relacionamento `pet.dono` fornece o nome dentro de `to_dict()`,
sem escrever JOIN manualmente.

Resposta `200`:

```json
[
    {
        "id": 1,
        "nome": "Rex",
        "especie": "cachorro",
        "idade": 4,
        "dono_id": 1,
        "dono_nome": "Ana Paula Ribeiro"
    }
]
```

### GET /pets?dono_id=1

A mesma rota acima aceita um filtro opcional por query param. Se o `dono_id`
for enviado, retorna apenas os pets daquele dono. Se nao for enviado, retorna
todos.

O valor e convertido para inteiro antes de `Pet.query.filter_by(...).all()`.
Um filtro como `?dono_id=abc` retorna `400` com
`{"erro": "dono_id deve ser um numero inteiro"}`. Um dono sem pets (ou que
nao existe) retorna uma lista vazia com `200`.

### GET /pets/{id}

Busca um pet pelo id.

Resposta `200`: o objeto do pet.

Resposta `404`: `{"erro": "Pet nao encontrado"}`

### POST /pets

Cadastra um pet.

Corpo da requisicao:

```json
{
    "nome": "Bidu",
    "especie": "cachorro",
    "idade": 2,
    "dono_id": 1
}
```

Resposta `201`: o pet criado, com o `id` gerado pelo banco.

Resposta `400`: `{"erro": "Informe nome, especie, idade e dono_id"}`

Resposta `404`: `{"erro": "Dono nao encontrado"}` quando o `dono_id` nao existe,
incluindo o desafio com `dono_id: 999`.

`nome` e `especie` devem ser textos nao vazios, `idade` deve ser um inteiro
nao negativo e `dono_id` deve ser um inteiro. Campos ausentes, nulos, tipos
invalidos ou um corpo que nao seja um objeto JSON retornam `400`.

### PUT /pets/{id}

Atualiza um pet. Recebe os mesmos campos do POST.

Resposta `200`: o pet atualizado, incluindo `dono_nome`.

Resposta `400`: `{"erro": "Informe nome, especie, idade e dono_id"}`.

Resposta `404`: `{"erro": "Pet nao encontrado"}`

Se o novo dono nao existir, retorna `404` com
`{"erro": "Dono nao encontrado"}`, sem alterar o pet.

### DELETE /pets/{id}

Remove um pet.

Resposta `200`: `{"mensagem": "Pet removido com sucesso"}`

Resposta `404`: `{"erro": "Pet nao encontrado"}`

## Entrega

Quando terminar, salve o trabalho no GitHub:

```
git add .
git commit -m "aula02: api com orm"
git push
```

Confira no site do GitHub se os arquivos aparecem la antes de sair do
laboratorio.

## Estrutura do repositorio

```
pds-seunome/
├── .devcontainer/           configuracao do Codespaces
├── backend/                 a API
│   ├── app.py               modelos Dono/Pet e rotas com ORM
│   ├── criar_banco.py       cria as tabelas e os dados de exemplo
│   ├── instance/            banco local, ignorado pelo Git
│   ├── requisicoes.http     requisicoes de teste
│   └── requirements.txt
├── exercicios/              exercicios avulsos de cada aula
└── README.md
```
