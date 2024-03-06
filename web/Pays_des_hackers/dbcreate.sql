CREATE DATABASE challenge;
use challenge;

CREATE TABLE roles (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name varchar(20)
);

INSERT INTO roles(name) VALUES ('Administratorz_du_76');
INSERT INTO roles(name) VALUES ('Hunter');
INSERT INTO roles(name) VALUES ('Analyste SOC');
INSERT INTO roles(name) VALUES ('Mauvais Hacker...');
INSERT INTO roles(name) VALUES ('Pentester');

CREATE TABLE users (
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username varchar(30) NOT NULL,
    password varchar(61) NOT NULL,
    role INT NOT NULL,
    FOREIGN KEY (role) REFERENCES roles(id)
);

DELIMITER //
CREATE FUNCTION NewUser (
    input_username varchar(30), 
    input_password varchar(61), 
    input_role varchar(20)
) RETURNS varchar(50) DETERMINISTIC
BEGIN
    DECLARE roleId INT;
    DECLARE alreadyExist INT;
    SELECT count(username) into alreadyExist from users where username = input_username;
    IF alreadyExist > 0 THEN
        RETURN 'Erreur : L\'utilisateur existe déjà.';
        END IF;
    SELECT id into roleId from roles where name = input_role;
    IF roleId IS NULL THEN 
        RETURN 'Erreur : Rôle inconnu.';
        END IF;
    INSERT INTO users(username, password, role) VALUES (input_username, input_password, roleId);
    RETURN 'SUCCESS';
END//
DELIMITER ;
SELECT newuser('hunter', 'passpass', 'Hunter');

CREATE USER chall@localhost IDENTIFIED BY 'dsfFKJDSkjdsf!83274fjdsh';

GRANT SELECT, INSERT ON challenge.users TO chall@localhost;
GRANT EXECUTE ON challenge.* TO chall@localhost;
GRANT SELECT ON challenge.roles TO chall@localhost;

FLUSH PRIVILEGES;

