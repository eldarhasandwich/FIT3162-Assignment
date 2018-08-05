
-- drop RATINGS database and connect
DROP DATABASE IF EXISTS testsnagraphs;
CREATE DATABASE testsnagraphs;
\c testsnagraphs;

-- generate structure
\i schema.sql;

INSERT INTO graphs (name) VALUES ('First Graph');
INSERT INTO graphs (name) VALUES ('Second Graph');
INSERT INTO graphs (name) VALUES ('Third Graph');

INSERT INTO nodes (email, graph_ID) VALUES ('a@a.a', 1);
INSERT INTO nodes (email, graph_ID) VALUES ('b@b.b', 1);
INSERT INTO nodes (email, graph_ID) VALUES ('c@c.c', 1);

INSERT INTO edges (sender_ID, recipient_ID, email_count) VALUES (1, 2, 10); 
INSERT INTO edges (sender_ID, recipient_ID, email_count) VALUES (2, 1, 20); 
INSERT INTO edges (sender_ID, recipient_ID, email_count) VALUES (1, 3, 10); 
INSERT INTO edges (sender_ID, recipient_ID, email_count) VALUES (3, 2, 5); 
INSERT INTO edges (sender_ID, recipient_ID, email_count) VALUES (2, 3, 15); 