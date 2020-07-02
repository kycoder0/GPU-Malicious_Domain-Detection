CREATE DATABASE domains;
USE domains;

CREATE TABLE dataset (
	staticip VARCHAR(255),
	domain VARCHAR(255) PRIMARY key,
	TIMESTAMP timestamp
);