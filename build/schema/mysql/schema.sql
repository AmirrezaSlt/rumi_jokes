CREATE DATABASE IF NOT EXISTS rumi;
USE rumi;
CREATE TABLE IF NOT EXISTS majors
(
  id   INT AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS users
(
    id INT AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255),
    password VARCHAR(255) UNIQUE,
    image_file CHAR(20) NOT NULL DEFAULT "default.jpg",
    major_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (major_id) REFERENCES
    majors(id) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS recommendations
(
    id INT AUTO_INCREMENT,
    user_id INT,
    joke_1 VARCHAR(255) NOT NULL,
    joke_2 VARCHAR(255) NOT NULL,
    expired BOOLEAN DEFAULT 0,
    priority INT DEFAULT NULL,
    winner BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES
    users(id) ON UPDATE CASCADE ON DELETE CASCADE
);
INSERT INTO majors(name) VALUES('Engineering');
INSERT INTO majors(name) VALUES('Business');
INSERT INTO majors(name) VALUES('Anthropology');
# INSERT INTO users(username, email, password, major_id, )