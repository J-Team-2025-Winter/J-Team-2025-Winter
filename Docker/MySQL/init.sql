
DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE customers (
    customer_id VARCHAR(255) PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(11) NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL
);

CREATE TABLE stylists (
    stylist_id VARCHAR(255) PRIMARY KEY,
    store_id INT,
    stylist_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(11) NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    profile_picture_url VARCHAR(255),
    comment VARCHAR(255)
);

 CREATE TABLE customers_stylists (
-- AUTO_INCREMENT→順番に情報が更新されるようにする
     customers_stylists_id INT AUTO_INCREMENT PRIMARY KEY,
     customer_id VARCHAR(255) NOT NULL,
     stylist_id VARCHAR(255) NOT NULL
);

 CREATE TABLE Messages (
     message_id INT AUTO_INCREMENT PRIMARY KEY,
     content VARCHAR(255) NOT NULL,
     image_url INT NOT NULL,
     sent_at DATETIME NOT NULL,
     reservation_id TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
     customers_stylists_id,
     FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
     FOREIGN KEY (cid) REFERENCES channels(id) ON DELETE CASCADE
 );
--CREATE TABLE Messages (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     uid VARCHAR(255) NOT NULL,
--     cid INT NOT NULL,
--     message TEXT,
--     created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
--     FOREIGN KEY (cid) REFERENCES channels(id) ON DELETE CASCADE
-- ); 

INSERT INTO customers(customer_id, customer_name, email, password, phone, gender) VALUES('00000000-0000-0000-0000-000000000000','Customer Zero','customerzero@gmail.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578', '00011112222', 'Male');
INSERT INTO stylists(stylist_id, store_id, stylist_name, email, password, phone, gender, profile_picture_url, comment) VALUES('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '1', 'Stylist Zero','stylistzero@gmail.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578', '33344445555', 'Male', 'profile-picture', 'hasami no koto nara omakase kudasai');
INSERT INTO customers_stylists(customers_stylists_id, customer_id, stylist_id) VALUES('1','00000000-0000-0000-0000-000000000000','aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa');
-- INSERT INTO channels(id, uid, name, abstract) VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8','ぼっち部屋','テストさんの孤独な部屋です');
INSERT INTO Messages(id, uid, cid, message) VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8', '1', '誰かかまってください、、')
--INSERT INTO Messages(id, uid, cid, message) VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8', '1', '誰かかまってください、、')