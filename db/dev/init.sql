-- Time function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

-- Custom Location Composite Type
CREATE TYPE loc AS (
    name      VARCHAR(255),
    lat       DOUBLE PRECISION,
    long      DOUBLE PRECISION,
    address   VARCHAR(255)
);

-- User table
CREATE TABLE Users (
    user_id VARCHAR(255) UNIQUE,
    org_id VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL  UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE  NOT NULL  DEFAULT current_timestamp,
    updated_at TIMESTAMP WITH TIME ZONE  NOT NULL  DEFAULT current_timestamp,
    PRIMARY KEY (user_id)
);

-- Event Table
CREATE TABLE Events (
    event_id VARCHAR(255) UNIQUE,
    event_name VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    event_description TEXT,
    event_location loc,
    event_start_time TIMESTAMP WITH TIME ZONE  NOT NULL  DEFAULT current_timestamp,
    event_end_time TIMESTAMP WITH TIME ZONE  NOT NULL  DEFAULT current_timestamp,
    attendee_limit INTEGER,
    has_started BOOLEAN,
    has_ended BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE  NOT NULL  DEFAULT current_timestamp,
    updated_at TIMESTAMP WITH TIME ZONE  NOT NULL  DEFAULT current_timestamp,
    PRIMARY KEY (event_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    CONSTRAINT attendee_limit_check CHECK(attendee_limit >= 0),
    CONSTRAINT time_validity CHECK(event_end_time >= event_start_time)
);

-- Attendence Table
CREATE TABLE Attendance (
    event_id VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    user_role VARCHAR(255),
    personal_code VARCHAR(255),
    is_invited BOOLEAN,
    is_rsvped BOOLEAN,
    is_checked_in BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE  NOT NULL  DEFAULT current_timestamp,
    updated_at TIMESTAMP WITH TIME ZONE  NOT NULL  DEFAULT current_timestamp,
    PRIMARY KEY (event_id, user_email),
    FOREIGN KEY (event_id) REFERENCES Events
);

-- Updated_at trigger
CREATE TRIGGER tg_sampleusers_updated_at
    BEFORE UPDATE
    ON Users
    FOR EACH ROW
    EXECUTE PROCEDURE update_updated_at_column();