CREATE TABLE if not exists "City"(
    id serial PRIMARY KEY,
    name varchar(255) not null
);


CREATE TABLE if not exists "Users"(
    id serial PRIMARY KEY,
    login varchar(255) not null,
    passwd varchar not null,
    name varchar(255) not null,
    city integer ,
    state boolean not null DEFAULT TRUE ,
    is_admin boolean not null DEFAULT FALSE,
    FOREIGN KEY(city) REFERENCES "City"(id) ON DELETE SET NULL
);

CREATE TABLE if not exists "Publication"(
    id serial PRIMARY KEY,
    name varchar(255) not null,
    users integer,
    city integer,
    body varchar not null,
    price real not null,
    state boolean not null DEFAULT TRUE,
    FOREIGN KEY(city) REFERENCES "City"(id) ON DELETE SET NULL,
    FOREIGN KEY(users) REFERENCES "Users"(id) ON DELETE SET NULL
);


CREATE INDEX if not exists user_email ON "Users"(login);
CREATE INDEX if not exists user_name ON "Users"(name);
CREATE INDEX if not exists city_name ON "City"(name);
CREATE INDEX if not exists publication_find ON "Publication"(name,body);

INSERT INTO "City" (name) VALUES  ('Красноярск'),
                                ('Москва'),
                                ('Казань'),
                                ('New York'),
                                ('Los Angeles');

INSERT INTO "Users" (login, passwd, name,city, state, is_admin) VALUES ('www.kraken@mail.ru','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','Александр',1,TRUE,TRUE),
                                                                     ('test@mail.ru','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','Justin',4,TRUE,FALSE),
                                                                     ('Willy','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','Willy Wonka',2,TRUE, FALSE);

INSERT INTO "Publication"(name,users,city,body,price,state) VALUES ('Продам котят',1,1,'Продам породистых котят, порода мейнкун',500.50, TRUE ),
                                                                 ('Travel to dreams',3,2,'It`s your lucky day! Buy your dream',990.99, TRUE);