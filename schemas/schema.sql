
DROP TABLE IF EXISTS graphs, edges, nodes CASCADE;

CREATE TABLE graphs (
    ID SERIAL PRIMARY KEY,
    name VARCHAR(40)
);

CREATE TABLE nodes (
    ID SERIAL PRIMARY KEY,
    email VARCHAR(40),
    graph_ID INT REFERENCES graphs(ID)
);

CREATE TABLE edges (
    ID SERIAL PRIMARY KEY,
    sender_ID INT REFERENCES nodes(ID),
    recipient_ID INT REFERENCES nodes(ID),
    graph_ID INT REFERENCES graphs(ID),
    email_count INT
);

CREATE TABLE analysis_results (
    edge_ID INT REFERENCES edges(ID) NOT NULL,
    analysis_key VARCHAR(6) NOT NULL,
    value FLOAT,
    PRIMARY KEY(edge_ID, analysis_key) 
);