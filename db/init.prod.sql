-- Time function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updatedAt = now();
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

-- User table
CREATE TABLE Users (
    userID VARCHAR(255) UNIQUE,
    username VARCHAR(255) NOT NULL,
    createdAt TIMESTAMP WITH TIME ZONE  NOT NULL  DEFAULT current_timestamp,
    updatedAt TIMESTAMP WITH TIME ZONE  NOT NULL  DEFAULT current_timestamp,
    PRIMARY KEY (userID)
);

-- UpdatedAt trigger
CREATE TRIGGER tg_users_updated_at
    BEFORE UPDATE
    ON Users
    FOR EACH ROW
    EXECUTE PROCEDURE update_updated_at_column();
