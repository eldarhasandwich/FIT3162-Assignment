
-- drop RATINGS database and connect
DROP DATABASE IF EXISTS snagraphs;
CREATE DATABASE snagraphs;
\c snagraphs;

-- generate structure
\i schema.sql;

INSERT INTO graphs (ID) VALUES (1);
INSERT INTO graphs (ID) VALUES (2);
INSERT INTO graphs (ID) VALUES (3);

INSERT INTO nodes (ID, email, graph_ID) VALUES (1, 'a@a.a', 1);
INSERT INTO nodes (ID, email, graph_ID) VALUES (2, 'b@b.b', 1);
INSERT INTO nodes (ID, email, graph_ID) VALUES (3, 'c@c.c', 1);