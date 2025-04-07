-- Script to create the PostgreSQL database 'nba_stats_db' with UTF-8 encoding.

-- IMPORTANT: Execute this script while connected to PostgreSQL with a user
-- that has database creation privileges (e.g., the 'postgres' user).
-- You can use psql: psql -U postgres -f init_db.sql

-- Attempt to create the database.
-- If the database already exists, this command will fail, which is acceptable
-- in most cases, or you can manually drop it first if needed.
CREATE DATABASE nba_stats_db
    WITH
    OWNER = postgres -- Ensure this user exists or use the one from your .env file
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8' -- Or an appropriate UTF-8 locale for your system
    LC_CTYPE = 'en_US.UTF-8'   -- Or an appropriate UTF-8 locale for your system
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    TEMPLATE = template0 -- Using template0 to avoid locale issues
    IS_TEMPLATE = False;

-- Display success message (will only show if CREATE DATABASE succeeds)
\echo "Database 'nba_stats_db' successfully created with UTF-8 encoding."

