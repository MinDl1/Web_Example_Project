CREATE TABLE example1(
    id serial PRIMARY KEY,
    test text UNIQUE NOT NULL
);

CREATE TABLE D$Role(
    id serial PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE D$User(
    id serial PRIMARY KEY,
    role_id INTEGER NOT NULL DEFAULT 2,
    username VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(256) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (role_id) REFERENCES D$Role(id)
);


INSERT INTO D$Role (name)
VALUES ('admin');

INSERT INTO D$Role (name)
VALUES ('user');

INSERT INTO D$User (role_id, username, email, hashed_password, is_active)
VALUES (1, 'admin', 'admin@example.admin', '$2b$12$HLCCulVfOWd04.OptDk6zuCEdV4giC/WQGIMNNKVm7TjEDc5uuq5S', true);
