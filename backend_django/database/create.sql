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