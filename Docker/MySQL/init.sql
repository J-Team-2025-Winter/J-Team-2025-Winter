
DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users (
    CustomerID VARCHAR(255) PRIMARY KEY,
    CustomerName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Phone VARCHAR(11) NOT NULL,
    Gender ENUM('Male', 'Female', 'Other') NOT NULL
);

CREATE TABLE stylists (
    StylistID VARCHAR(255) PRIMARY KEY,
    StoreID INT,
    StylistName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Phone VARCHAR(11) NOT NULL,
    Gender ENUM('Male', 'Female', 'Other') NOT NULL,
    ProfilePictureURL VARCHAR(255),
    Comment VARCHAR(255)
);

-- CREATE TABLE channels (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     uid VARCHAR(255) NOT NULL,
--     name VARCHAR(255) UNIQUE NOT NULL,
--     abstract VARCHAR(255),
--     FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE
-- );

-- CREATE TABLE messages (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     uid VARCHAR(255) NOT NULL,
--     cid INT NOT NULL,
--     message TEXT,
--     created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
--     FOREIGN KEY (cid) REFERENCES channels(id) ON DELETE CASCADE
-- );

INSERT INTO users(CustomerID, CustomerName, Email, Password, Phone, Gender) VALUES('00000000-0000-0000-0000-000000000000','Customer Zero','customerzero@gmail.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578', '00011112222', 'Male');
INSERT INTO stylists(StylistID, StoreID, StylistName, Email, Password, Phone, Gender, ProfilePictureURL, Comment) VALUES('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '1', 'Stylist Zero','stylistzero@gmail.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578', '33344445555', 'Male', 'profile-picture', 'hasami no koto nara omakase kudasai');
-- INSERT INTO channels(id, uid, name, abstract) VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8','ぼっち部屋','テストさんの孤独な部屋です');
-- INSERT INTO messages(id, uid, cid, message) VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8', '1', '誰かかまってください、、')