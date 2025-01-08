CREATE OR REPLACE FUNCTION log_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO logs.postgres(operation_type, table_name, old_values, new_values)
        VALUES ('DELETE', TG_TABLE_NAME, row_to_json(OLD), NULL);
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO logs.postgres(operation_type, table_name, old_values, new_values)
        VALUES ('UPDATE', TG_TABLE_NAME, row_to_json(OLD), row_to_json(NEW));
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO logs.postgres(operation_type, table_name, old_values, new_values)
        VALUES ('INSERT', TG_TABLE_NAME, NULL, row_to_json(NEW));
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER log_auth_role_changes
AFTER INSERT OR UPDATE OR DELETE ON auth.role
FOR EACH ROW EXECUTE FUNCTION log_changes();

CREATE TRIGGER log_auth_user_changes
AFTER INSERT OR UPDATE OR DELETE ON auth.user
FOR EACH ROW EXECUTE FUNCTION log_changes();

CREATE TRIGGER log_auth_tag_changes
AFTER INSERT OR UPDATE OR DELETE ON auth.tag
FOR EACH ROW EXECUTE FUNCTION log_changes();

CREATE TRIGGER log_auth_endpoint_changes
AFTER INSERT OR UPDATE OR DELETE ON auth.endpoint
FOR EACH ROW EXECUTE FUNCTION log_changes();

CREATE TRIGGER log_auth_role_right_changes
AFTER INSERT OR UPDATE OR DELETE ON auth.role_right
FOR EACH ROW EXECUTE FUNCTION log_changes();

CREATE TRIGGER log_auth_user_right_changes
AFTER INSERT OR UPDATE OR DELETE ON auth.user_right
FOR EACH ROW EXECUTE FUNCTION log_changes();
