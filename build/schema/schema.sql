USE dbms;
DROP TABLE IF EXISTS recommendations;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS majors;
CREATE TABLE majors
(
  id   INT AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);
CREATE TABLE users
(
    id INT AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255),
    password VARCHAR(255) UNIQUE,
    image_file CHAR(20) NOT NULL DEFAULT "default.jpg",
    mid INT,
    PRIMARY KEY (id),
    FOREIGN KEY (mid) REFERENCES
    majors(id) ON UPDATE CASCADE ON DELETE CASCADE
);
# INSERT INTO majors(name) VALUES('Engineering');
# INSERT INTO majors(name) VALUES('Business');
# INSERT INTO majors(name) VALUES('Anthropology');
CREATE TABLE recommendations
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
)
