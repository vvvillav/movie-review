create database movie;
CREATE TABLE reviews (
    productId VARCHAR(255),
    userId VARCHAR(255),
    profileName TEXT,
    helpfulness VARCHAR(50),
    score DECIMAL,
    reviewTime BIGINT,
    summary TEXT,
    reviewText TEXT
);
\copy reviews FROM 'movie.csv' WITH CSV;
