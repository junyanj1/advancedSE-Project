-- Time function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

-- User table
CREATE TABLE Users (
    user_id VARCHAR(255) UNIQUE,
    username VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE  NOT NULL  DEFAULT current_timestamp,
    updated_at TIMESTAMP WITH TIME ZONE  NOT NULL  DEFAULT current_timestamp,
    PRIMARY KEY (user_id)
);

-- Updated_at trigger
CREATE TRIGGER tg_users_updated_at
    BEFORE UPDATE
    ON Users
    FOR EACH ROW
    EXECUTE PROCEDURE update_updated_at_column();
