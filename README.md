# Mini-curso: Python WEB + Angular

## Objetivo

Desenvolver uma pequena aplicação web Python, com o fim de se compreender os principais conceitos dos padrões mais recentes de desenvolvimento WEB (notadamente APIs REST e Single Page Application).

## Aplicação de Exemplo

Construiremos o MVP de uma aplicação de gestão de tarefas pessoais, com as seguintes features:

* Cadastro de novas tarefas
* Visualização da lista de tarefas pendentes
* Marcar tarefas como concluídas


O nome da aplicação será ```mytodo```.

## Fora do escopo

* Controle de autenticação de usuários (padrão OAuth)
* Controle de versão do banco de dados
* Empacotamento da solução via Docker (o docker será usado apenas enquanto facilitador em alguns passos)
* Auto deploy
* Controle de versão
* Integração contínua
* Ferramentas ORM
* Framework para desenvolvimento REST (implementaremos APIs REST de maneira manual)
* Configurações diversas (inclusive segurança) para o ambiente de produção
* etc

O foco do mini-curso é exclusivamente funcional, não contemplando requisitos não funcionais, gestão de configuração ou frameworks web focados em low-code (a intenção é simplesmente dar uma ideia mais concreta das facetas de uma aplicação WEB).

## Pré-requisitos

* Python
* TypeScript
* SQL
* Protocolo HTTP
* HTML/CSS
* Padrões de projeto (MVC)

## Passos para o Backend com DJango

1. Instalar o Django (mais recente)

```sh
pip install Django
```

2. Criar o projeto Django

```sh
django-admin startproject minicurso
```

3. Criar e habilitar o virtual environment Python

```sh
python3 -m venv .venv
source ./.venv/bin/activate
```

4. Instalar novamento o Django (agora no ambiente virtual)

```sh
pip install Django
```

5. Escrever SQL de criação das tabelas do banco de dados (arquivo ```database/create.sql```)

```sql
create table task (
    id varchar(36) not null primary key,
    description varchar not null,
    priority smallint not null,
    complexity smallint not null,
    created_at timestamp without time zone not null default now(),
    finished_at timestamp without time zone,
    time interval,
    status boolean not null default false
);

insert into task (id, description, priority, complexity)
values ('15d941f4-d33e-4218-bdc2-7b3365daa752', 'Elaborar mini-curso de Python WEB', 10, 6);

insert into task (id, description, priority, complexity)
values ('625ef774-7751-4a5e-a66b-afc1c8d7867e', 'Gravar mini-curso de Python WEB', 10, 4);
```

6. Criar uma instância banco de dados postgres (usando docker)

```yml
version: '2'

services:
    postgres:
        image: postgres:11.5
        ports: 
           - "5440:5432"
        volumes:
           - $PWD/database:/docker-entrypoint-initdb.d/
        environment:
           - "POSTGRES_DB=teste_db"
           - "POSTGRES_USER=postgres"
           - "POSTGRES_PASSWORD=postgres"
```

Obs.: Note o mapeamento do entrypoint para criação das tabelas do BD.

7. Iniciar o banco de dados

```sh
docker-compose up -d postgres
```

8. Instalar o "driver" de conexão com o banco

```sh
pip install psycopg2-binary
```

9. Testar a aplicação

```sh
python manage.py runserver
```

10. Criar a aplicação Django

```sh
python manage.py startapp mytodo
```

Obs.: O Django divide os conceitos de projeto e aplicação:

* Projeto: Representa um servidor web em si (ou um site que responde por um endereço, popularmente falando). Na prática, se torna um conjunto de aplicações.
* É um subconjunto de um projeto, porém corresponde a um módulo completo, com seus próprios endpoints (URLs).

A ideia aqui é que aplicações podem ser reutilizáveis em diversos projetos, mas podem conter toda uma aplicação web (propriamente dita).

11. Configurar a conexão com o banco de dados (```settings.py```)

```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('database_name', 'teste_db'),
        'USER': os.getenv('database_user', 'postgres'),
        'PASSWORD': os.getenv('database_password', 'postgres'),
        'HOST': os.getenv('database_host', 'localhost'),
        'PORT': os.getenv('database_port', '5440'),
    }
}
```

12. Instalar o sqlparams e um pacote de utilitários da própria Nasajon (nsj-gcf-utils):

```sh
pip install sqlparams==3.0.0
pip install nsj-gcf-utils==0.1.2
```

13. Escrever um objeto para acesso ao banco de dados (```mytodo/repository/task_repository.py```):

```python
import uuid

from nsj_gcf_utils.abstract_repository import AbstractRepository
from typing import Any, Dict


class TaskRepository(AbstractRepository):

    def find_by_id(self, id: str):
        sql = """
        select
            id,
            description,
            priority,
            complexity,
            created_at,
            finished_at,
            (extract(epoch from time)/3600)::int as time,
            status
        from
            task
        where
            id = :id
        """

        return self.fetchOne(sql, {'id': id})

    def list(self, status: bool = False):
        sql = """
        select
            id,
            description,
            priority,
            complexity,
            created_at,
            finished_at,
            (extract(epoch from time)/3600)::int as time,
            status
        from
            task
        where
            status = :status
        order by
            created_at desc
        """

        return self.fetchAll(sql, {'status': status})

    def insert_new(self, task: Dict[str, Any]):
        sql = """
        insert into task (
            id, description,
            priority, complexity )
        values (
            :id, :description,
            :priority, :complexity )
        """

        id = str(uuid.uuid4())

        count = self.execute(
            sql, {
                'id': id,
                'description': task['description'],
                'priority': task['priority'],
                'complexity': task['complexity']
            }
        )

        if count <= 0:
            raise Exception(f'Error inserting new task ({id}): {task}')

        return id

    def update(self, id: str, task: Dict[str, Any]):
        sql = """
        update task set
            description=:description, priority=:priority, complexity=:complexity, created_at=:created_at
        where
            id = :id
        """

        return self.execute(sql, {
            'id': id,
            'description': task['description'],
            'priority': task['priority'],
            'complexity': task['complexity'],
            'created_at': task['created_at']
        })

    def get_status(self, id: str):
        sql = """
        select
            status
        from
            task
        where
            id = :id
        """

        return self.fetchOne(sql, {'id': id})

    def update_status(self, id: str, status: bool):
        current_status = self.get_status(id)['status']

        if status == current_status:
            return 0
        elif status and not current_status:
            sql = """
            update task set
                status=true, finished_at=now(), time=now()-created_at
            where
                id = :id
                and not status
            """
        elif not status and current_status:
            sql = """
            update task set
                status=false, finished_at=null, time=null
            where
                id = :id
                and status
            """
        else:
            raise Exception(f'Inconsistent status {status} - {current_status}')

        self.execute(sql, {'id': id})

        return 0

    def delete_by_id(self, id: str):
        sql = """
        delete from task where id = :id
        """
        return self.execute(sql, {'id': id})
```

14. Criar um super classe paras as views do projeto (```mytodo/view/generic_view.py```):

```python
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from typing import Any, Dict, List


@method_decorator(csrf_exempt, name='dispatch')
class GenericView(View):

    def _check_required_attributes(self, attributes: List[str], data_dict: Dict[str, Any]):

        missing = []
        for attribute in attributes:
            if not attribute in data_dict:
                missing.append(attribute)

        if len(missing) > 0:
            return missing
        else:
            return None
```

___
Entendendo um pouco sobre o MTV:

O MTV (Model Template View) é o padrão de projeto adotado pelo Django, e pode ser explicado através de um paralelo com o padrão MVC.

No MVC tradicional, a camada View representa os artefatos de código destinados à exibição dos dados ao usuário. Na evolução MV<sup>2</sup>C entende-se que a camada View deve ser divida entre artefatos destinados à renderização em si dos dados (geração de HTMLs, por exemplo), e artefatos destinado ao controle desta visualização (lógica de filtragem de dados, por exemplo, para posterior renderização).

Assim, pode traçar o seguinte paralelo entre o MVT e o MV<sup>2</sup>C:

* M = As classes de modelo do Django equivalem às do tradicional MVC.
* T = A camada Template do Django equivale a camada de pura exibição descrita no MV<sup>2</sup>C (consistindo em templates de renderização de conteúdo, principalmente HTMLs).
* V = A camada View do Django equivale a camada de controle da View, descrita no MV<sup>2</sup>C (contendo boa parte da lógica de negócio e manipulação das classes de modelo).

Por fim, onde se encontra a camada Controller do tradicional MVC?

A resposta é que o próprio Django se encarrega de implementar esta camada, pois o framework controla, por exemplo, o mapeamento entre as URLs e as Views (o que normalmente é definido nas classes de Controller, de outros frameworks WEB).

_Obs.: Nós não usaremos os Templates do Django, pois estaremos trabalhando como conceito de Single Page Application (que é mais recente do que a renderização de HTMLs no lado servidor). Também não usaremos os Modelos do Django, pois queremos exemplificar o acesso direto ao banco de dados (sem um framework ORM como peça intermediária)._
___

15. Escrever uma View para gravação de novas tarefas, e listagem das tarefas por status (```mytodo/view/tasks_view.py```):

```python
from django.http import HttpResponse
from nsj_gcf_utils.json_util import json_dumps, json_loads
from typing import Any

from mytodo.repository.task_repository import TaskRepository
from mytodo.view.generic_view import GenericView


class TasksView(GenericView):

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._repository = TaskRepository()

    def get(self, request, *args, **kwargs):

        try:
            status = False
            if request.GET.get('status'):
                status = (request.GET.get('status').lower() == 'true')

            tasks = self._repository.list(status)
            return HttpResponse(json_dumps(tasks), status=200, content_type='application/json')
        except Exception as e:
            msg = '{"message": "Unknown error listing tasks: ' + str(e) + '"}'
            return HttpResponse(content=msg, status=500)

    def post(self, request, *args, **kwargs):

        try:
            # Loading json
            task = json_loads(request.body.decode())

            # Checking required attributes
            required_attributes = ['description', 'priority', 'complexity']
            missing_attributes = self._check_required_attributes(
                required_attributes, task)
            if missing_attributes:
                msg = '{"message": "Missing parameters: ' + \
                    str(missing_attributes) + '."'
                return HttpResponse(msg, status=400)

            # Inserting into database
            id = self._repository.insert_new(task)

            # Retrieving inserted task
            task = self._repository.find_by_id(id)

            return HttpResponse(content=json_dumps(task), status=200)
        except Exception as e:
            msg = '{"message": "Unknown error listing tasks: ' + str(e) + '"}'
            return HttpResponse(content=msg, status=500)
```

16. Escrever uma View para recuperação, atualização e deleção de tarefas em particular (```mytodo/view/task_view.py```):

```python
from django.http import HttpResponse
from nsj_gcf_utils.json_util import json_dumps, json_loads
from typing import Any

from mytodo.repository.task_repository import TaskRepository
from mytodo.view.generic_view import GenericView


class TaskView(GenericView):

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._repository = TaskRepository()

    def get(self, request, *args, **kwargs):

        try:
            # Getting ID
            id = kwargs["id"]

            # Getting task
            task = self._repository.find_by_id(id)

            if task is None:
                return HttpResponse('', status=404)

            return HttpResponse(json_dumps(task), status=200, content_type='application/json')
        except Exception as e:
            msg = '{"message": "Unknown error getting task: ' + \
                str(e) + '"}'
            return HttpResponse(content=msg, status=500)

    def put(self, request, *args, **kwargs):

        try:
            # Loading json
            task = json_loads(request.body.decode())

            # Getting ID
            id = kwargs["id"]

            # Checking required attributes
            required_attributes = [
                'description', 'priority', 'complexity', 'created_at', 'status']
            missing_attributes = self._check_required_attributes(
                required_attributes, task)
            if missing_attributes:
                msg = '{"message": "Missing parameters: ' + \
                    str(missing_attributes) + '."'
                return HttpResponse(msg, status=400)

            # Updating task
            self._repository.update(id, task)
            self._repository.update_status(id, task['status'])

            return HttpResponse(content='', status=204)
        except Exception as e:
            msg = '{"message": "Unknown error updating task status: ' + \
                str(e) + '"}'
            return HttpResponse(content=msg, status=500)

    def patch(self, request, *args, **kwargs):

        try:
            # Loading json
            task = json_loads(request.body.decode())

            # Getting ID
            id = kwargs["id"]

            # Checking required attributes
            required_attributes = ['status']
            missing_attributes = self._check_required_attributes(
                required_attributes, task)
            if missing_attributes:
                msg = '{"message": "Missing parameters: ' + \
                    str(missing_attributes) + '."'
                return HttpResponse(msg, status=400)

            # Updating task status
            self._repository.update_status(id, task['status'])

            return HttpResponse(content='', status=204)
        except Exception as e:
            msg = '{"message": "Unknown error updating task status: ' + \
                str(e) + '"}'
            return HttpResponse(content=msg, status=500)

    def delete(self, request, *args, **kwargs):

        try:
            # Getting ID
            id = kwargs["id"]

            # Deleting
            count = self._repository.delete_by_id(id)

            if count <= 0:
                return HttpResponse('', status=404)

            return HttpResponse('', status=204, content_type='application/json')
        except Exception as e:
            msg = '{"message": "Unknown error deleting task: ' + \
                str(e) + '"}'
            return HttpResponse(content=msg, status=500)
```

17. Criar um arquivo de mapeamento das rotas na aplicação (```mytodo/urls.py```).

```python
from django.urls import path

from mytodo.view.task_view import TaskView
from mytodo.view.tasks_view import TasksView
# from . import views

urlpatterns = [
    path('tasks', TasksView.as_view(), name='tasks'),
    path('tasks/<str:id>', TaskView.as_view(), name='task'),
]
```

18. Configurar o mapeamento das rotas da aplicação, no projeto (```minicurso/urls.py```).

```python
urlpatterns = [
    path('', include('mytodo.urls')),
    path('admin/', admin.site.urls),
]
```

19. Criar um arquivo ".rest" para testar todas as rotas (```rest/tasks.rest```):

```rest
#################
# Listing tasks #
#################
GET http://127.0.0.1:8000/tasks HTTP/1.1
Accpet: application/json

###################
# Filtering tasks #
###################
GET http://127.0.0.1:8000/tasks?status=true HTTP/1.1
Accpet: application/json

##################
# Getting a task #
##################
GET http://127.0.0.1:8000/tasks/625ef774-7751-4a5e-a66b-afc1c8d7867e HTTP/1.1
Accpet: application/json

##################
# Inserting task #
##################
POST http://127.0.0.1:8000/tasks HTTP/1.1
Content-Type: application/json

{
    "description": "Teste de insert",
    "priority": 3.0,
    "complexity": 1.0
}

################
# Closing task #
################
PATCH http://127.0.0.1:8000/tasks/625ef774-7751-4a5e-a66b-afc1c8d7867e HTTP/1.1
Content-Type: application/json

{
    "status": true
}

####################
# Updatting a task #
####################
PUT http://127.0.0.1:8000/tasks/625ef774-7751-4a5e-a66b-afc1c8d7867e HTTP/1.1
Accpet: application/json

{
    "description": "Gravar mini-curso de Python WEB atualizado",
    "priority": 10,
    "complexity": 4,
    "created_at": "2021-08-20T17:55:07",
    "status": false
}
```

## Passos para o Frontend com Angular

1. Instalar o gerenciador de dependências javascript ```npm```

```sh
sudo apt install npm
```

2. Instalar o ambiente de execução javascript ```nodejs```

```sh
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs
```

3. Instalar o aplicativo de linha de comando do ```Angular```:

```sh
npm install -g @angular/cli
```

4. Criar a aplicação Angular:

```sh
ng new mytodo
```

5. Iniciar a aplicaçao Angular

```sh
cd mytodo
ng serve --open
```

5. Alterar o título da alicação no arquivo ```src/app/app.component.ts```

```ts
export class AppComponent {
  title = 'My TODO';
}
```

6. Alterar o template principal da aplicação ```src/app/app.component.html```

```html
<h1>{{title}}</h1>
<app-tasks></app-tasks>
```

7. Criar o componente de exeibição dos detalhes de uma tarefa

```sh
ng generate component tasks
```

8. Criar a interface de representação de uma tarefa ```src/app/task.ts```

```ts
export interface Task {
    id: string;
    description: string;
    priority: number;
    complexity: number;
    created_at: string;
    finished_at: string;
    time: number;
    status: boolean;
}
```

9. Importe o FormsModule na aplicação (para fazer "binding" entre a interface e os objetos):

```ts
import { FormsModule } from '@angular/forms';

@NgModule({
...
  imports: [
    BrowserModule,
    FormsModule
  ],
...
```

X. Adicionr o módulo de controle de rotas do Angular

```sh
ng generate module app-routing --flat --module=app
```

X. Configure o proxy para o servidor de backend

## Próximos Passos

Em futuros mini-cursos idealizamos cobrir:

* Backend com Flask
* Backend serverless (Google Cloud Functions ou AWS Lambda Functions)
* Integração com técnicas de IA (estimativa de custo em dias das tarefas pendentes, baseado na complexidade, prioridade e custo, em dias, do histórico de tarefas concluídas)
