# Mini-curso: Python WEB + Angular

## Objetivo

Desenvolver uma pequena aplicação web Python, com o fim de se compreender os principais conceitos dos padrões mais recentes de desenvolvimento WEB (notadamente APIs REST e Single Page Application).

## Aplicação de Exemplo

Construiremos o MVP de uma aplicação de gestão de tarefas pessoais, com as seguintes features:

* Cadastro de novas tarefas
* Visualização da lista de tarefas pendentes
* Marcar tarefas como concluídas
* Estimativa de prazo para as tarefas pendentes (usando técnicas de Machine Learning)

O nome da aplicação será ```mytodo```.

## Fora do escopo

* Controle de autenticação de usuários (padrão OAuth)
* Gestão de alterações no banco de dados
* Empactoamento da solução via Docker (o docker será usado apenas enquanto facilitador em alguns passos)
* Auto deploy
* Controle de versão
* Integração contínua
* Ferramentas ORM
* Framework para desenvolvimento REST
* Configurações diversas (inclusive segurança) para o ambiente de produção
* etc

O foco do mini-curso é exclusivamente funcional, não contemplando requisitos não funcionais, gestão de configuração ou frameworks web focados em low-code (a intenção é dar uma ideia mais concreta ddas facetas de uma aplicação WEB).

## Pré-requisitos

* Sintaxe Python
* Sintaxe TypeScript
* Sintaxe SQL
* Noções sobre o protocolo HTTP
* Noções de HTML/CSS
* Padrão de projetos MVC

## Passos para o Backend com DJango

1. Criar e habilitar o virtual environment Python

```sh
python3 -m venv .venv
source ./.venv/bin/activate
```

2. Criar um banco de dados (docker)

3. Instalar o Django (mais recente)

```sh
pip install Django
```

4. Instalar o "driver" de conexão com o banco

```sh
pip install psycopg2-binary
```

5. Criar o projeto Django

```sh
django-admin startproject minicurso
```

6. Testar a aplicação

```sh
cd minicurso
python manage.py runserver
```

7. Criar a aplicação Django

```sh
python manage.py startapp mytodo
```

8. Configurando a conexão com o banco de dados

9. Entendendo um pouco sobre o MTV:

O MTV (Model Template View) é o padrão de projeto adotado pelo Django, e pode ser explicado através de um paralelo com o padrão MVC.

No MVC tradicional, a camada View representa os artefatos de código destinados à exibição dos dados ao usuário. Na evolução MV<sup>2</sup>C entende-se que a camada View deve ser divida entre artefatos destinados à renderização em si dos dados (geração de HTMLs, por exemplo), e artefatos destinado ao controle desta visualização (lógica de filtragem de dados, por exemplo, para posterior renderização).

Assim, pode traçar o seguinte paralelo entre o MVT e o MV<sup>2</sup>C:

* M = As classes de modelo do Django equivalem às do tradicional MVC.
* T = A camada Template do Django equivale a camada de pura exibição descrita no MV<sup>2</sup>C (consistindo em templates de renderização de conteúdo, principalmente HTMLs).
* V = A camada View do Django equivale a camada de controle da View, descrita no MV<sup>2</sup>C (contendo boa parte da lógica de negócio e manipulação das classes de modelo).

Por fim, onde se encontra a camada Controller do tradicional MVC?

A resposta é que o próprio Django se encarrega de implementar esta camada, pois o framework controla, por exemplo, o mapeamento entre as URLs e as Views (o que normalmente é definido nas classes de Controller, de muitos outros frameworks WEB).

_Obs.: Nós não usaremos os Templates do Django, pois estaremos trabalhando como conceito de Single Page Application (que é mais recente do que a renderização de HTMLs no lado server). Também não usaremos os Modelos do Django, pois queremos exemplificar o acesso direto ao banco de dados (sem um framework ORM como peça intermediária)._

10. Instalando um pacote de utilitários da própria Nasajon

```sh
pip install sqlparams==3.0.0
pip install nsj-gcf-utils==0.0.7
```

11. Escrever um objeto para acesso ao banco de dados (Repository).

12. Escrever a View para manipulação das tarefas.

13. Escrever a View para recuperação e atualziação de uma tarefa em particular (marcar tarefa como conluída).

14. Criar um arquivo de mapeamento das rotas na aplicação ```mytodo/urls.py```.

15. Configurando o mapeamento das rotas da aplicação, no projeto ```minicurso/urls.py```.

16. Criar um arquiv ".rest" para testar todas as rotas

## Passos para o Backend com Cloud Functions (Flask)

TODO

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
