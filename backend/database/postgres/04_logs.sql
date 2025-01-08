CREATE SCHEMA logs;

CREATE TABLE logs.postgres(
    id SERIAL PRIMARY KEY,
    operation_type TEXT NOT NULL,
    table_name TEXT NOT NULL,
    old_values JSONB,
    new_values JSONB,
    write_date_time TIMESTAMP DEFAULT NOW()
);

CREATE TABLE logs.api(
    id SERIAL PRIMARY KEY,
    id_user INTEGER,
    client_host CIDR NOT NULL,
    client_port INTEGER NOT NULL,
    url TEXT NOT NULL,
    method VARCHAR(10) NOT NULL,
    query_params TEXT,
    path_params TEXT,
    response_code INTEGER,
    response_error TEXT,
    api_date_time TIMESTAMP NOT NULL,
    write_date_time TIMESTAMP NOT NULL DEFAULT NOW(),
    execution_time FLOAT
);
