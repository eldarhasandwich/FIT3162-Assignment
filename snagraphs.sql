
-- drop RATINGS database and connect
DROP DATABASE IF EXISTS snagraphs;
CREATE DATABASE snagraphs;
\c snagraphs;

-- generate structure
\i schema.sql;

