# Base - Controle De Leituras

Esta é a aplicação-base da avaliação de reposição da turma 2V.

Ela já possui CRUD de leituras com SQLite, Blueprint de autenticação, Blueprint de leituras e uma função de segurança iniciada em `seguranca.py`. A autenticação com `session` e o controle de acesso por usuário ainda precisam ser implementados.

## Executar

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Acesse `http://127.0.0.1:5000`.

## Arquivos Principais

- `app.py`: cria a aplicação e registra os Blueprints.
- `auth.py`: rotas de cadastro, login e logout a serem completadas.
- `leituras.py`: rotas do CRUD de leituras.
- `seguranca.py`: função de proteção das rotas privadas.
- `database.py`: funções de banco de dados.
- `templates/`: páginas HTML.

## Observação

Não substitua a aplicação por outro projeto. A tarefa é adaptar esta base para autenticação com `session`, vinculando cada leitura ao usuário logado.

1. por que as rotas de leituras ficaram em leituras.py e não em app.py?
as rotas de leitura devem ficar em leituras.py porque é o blueprint que essas rotas pertencem, pra que o app fique só com o necessário pra iniciar a aplicação

2. Como a aplicação identifica o usuário logado usando session?
quando o usuario faz login, a aplicação salva o id dele na sessão usando session["usuario_id"] = usuario[id], e aí o flask consulta esse id na sess[ão pra saber quem tá logado sem precisar pedir pra logar de novo

3. Como seguranca.py, leituras.py e database.py impedem acesso a leituras de outro usuário?
eles impedem filtrando as consultas ao banco pelo id do usuário logado, que é feito pela session, garantindo que aquele usuário só veja seus próprios dados
