
-- drop RATINGS database and connect
DROP DATABASE IF EXISTS snagraphs;
CREATE DATABASE snagraphs;
\c snagraphs;

-- generate structure
\i schema.sql;

INSERT INTO graphs (name) VALUES ('First Graph');
INSERT INTO graphs (name) VALUES ('Second Graph');
INSERT INTO graphs (name) VALUES ('Third Graph');

INSERT INTO nodes (email, graph_ID) VALUES ('a@a.a', 1);
INSERT INTO nodes (email, graph_ID) VALUES ('b@b.b', 1);
INSERT INTO nodes (email, graph_ID) VALUES ('c@c.c', 1);