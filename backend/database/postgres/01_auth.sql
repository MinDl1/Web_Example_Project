CREATE SCHEMA auth;

CREATE TABLE auth.role(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(256),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    id_created_by INTEGER NOT NULL,
    created_date TIMESTAMP NOT NULL DEFAULT NOW(),
    id_last_update_by INTEGER,
    last_update_date TIMESTAMP,
    id_deleted_by INTEGER,
    deleted_date TIMESTAMP
);

CREATE INDEX idx_role_is_deleted ON auth.role (is_deleted);
CREATE UNIQUE INDEX idx_unique_role_name ON auth.role (name) WHERE is_deleted = FALSE;

INSERT INTO auth.role (name, id_created_by)
VALUES ('admin', 1),
('user', 1);

CREATE TABLE auth.user(
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(256) NOT NULL,
    id_base_role INTEGER NOT NULL,
    id_extra_role INTEGER,
    date_start_extra_role TIMESTAMP WITH TIME ZONE,
    date_stop_extra_role TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    id_created_by INTEGER,
    created_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    id_last_update_by INTEGER,
    last_update_date TIMESTAMP WITH TIME ZONE,
    id_deleted_by INTEGER,
    deleted_date TIMESTAMP WITH TIME ZONE,
    FOREIGN KEY (id_base_role) REFERENCES auth.role(id),
    FOREIGN KEY (id_extra_role) REFERENCES auth.role(id),
    FOREIGN KEY (id_created_by) REFERENCES auth.user(id),
    FOREIGN KEY (id_last_update_by) REFERENCES auth.user(id),
    FOREIGN KEY (id_deleted_by) REFERENCES auth.user(id)
);

INSERT INTO auth.user (username, hashed_password, id_base_role)
VALUES ('admin', '$2b$12$HLCCulVfOWd04.OptDk6zuCEdV4giC/WQGIMNNKVm7TjEDc5uuq5S', 1);

ALTER TABLE auth.role
ADD CONSTRAINT fk_id_created_by
FOREIGN KEY (id_created_by)
REFERENCES auth.user (id),
ADD CONSTRAINT fk_id_last_update_by
FOREIGN KEY (id_last_update_by)
REFERENCES auth.user (id),
ADD CONSTRAINT fk_id_deleted_by
FOREIGN KEY (id_deleted_by)
REFERENCES auth.user (id);

CREATE INDEX idx_user_is_deleted ON auth.user (is_deleted);
CREATE UNIQUE INDEX idx_unique_user_username ON auth.user (username) WHERE is_deleted = FALSE;

CREATE TABLE auth.tag(
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    swagger_name VARCHAR(128) UNIQUE NOT NULL,
    description VARCHAR(256)
);

CREATE TABLE auth.endpoint(
    id SERIAL PRIMARY KEY,
    id_tag INTEGER NOT NULL,
    url VARCHAR(128) NOT NULL,
    method VARCHAR(10) NOT NULL,
    name VARCHAR(128) NOT NULL,
    description VARCHAR(256),
    FOREIGN KEY (id_tag) REFERENCES auth.tag(id)
);

CREATE TABLE auth.role_right(
    id SERIAL PRIMARY KEY,
    id_role INTEGER NOT NULL,
    id_endpoint INTEGER NOT NULL,
    id_created_by INTEGER NOT NULL,
    created_date TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (id_role) REFERENCES auth.role(id),
    FOREIGN KEY (id_endpoint) REFERENCES auth.endpoint(id),
    FOREIGN KEY (id_created_by) REFERENCES auth.user(id)
);

CREATE INDEX idx_role_right_id_role ON auth.role_right (id_role);
CREATE INDEX idx_role_right_id_endpoint ON auth.role_right (id_endpoint);

CREATE TABLE auth.user_right(
    id SERIAL PRIMARY KEY,
    id_user INTEGER,
    id_endpoint INTEGER,
    is_allow BOOLEAN NOT NULL,
    id_created_by INTEGER NOT NULL,
    created_date TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (id_user) REFERENCES auth.user(id),
    FOREIGN KEY (id_endpoint) REFERENCES auth.endpoint(id),
    FOREIGN KEY (id_created_by) REFERENCES auth.user(id)
);

CREATE INDEX idx_user_right_id_user ON auth.user_right (id_user);
CREATE INDEX idx_user_right_id_endpoint ON auth.user_right (id_endpoint);
