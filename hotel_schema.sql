-- Hotel Management System – CS480 Spring 2026
CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE Managers (
    SSN         CHAR(9)      PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE Client (
    email       VARCHAR(150) PRIMARY KEY,
    name        VARCHAR(100) NOT NULL
);

CREATE TABLE Address (
    street_name     VARCHAR(150) NOT NULL,
    street_number   VARCHAR(20)  NOT NULL,
    city            VARCHAR(100) NOT NULL,
    PRIMARY KEY (street_name, street_number, city)
);

-- Client can have multiple addresses
CREATE TABLE Client_Address (
    email         VARCHAR(150) NOT NULL REFERENCES Client(email) ON DELETE CASCADE,
    street_name   VARCHAR(150) NOT NULL,
    street_number VARCHAR(20)  NOT NULL,
    city          VARCHAR(100) NOT NULL,
    PRIMARY KEY (email, street_name, street_number, city),
    FOREIGN KEY (street_name, street_number, city) REFERENCES Address(street_name, street_number, city)
);

CREATE TABLE Credit_Card (
    card_number   VARCHAR(20)  PRIMARY KEY,
    email         VARCHAR(150) NOT NULL REFERENCES Client(email) ON DELETE CASCADE,
    street_name   VARCHAR(150) NOT NULL,
    street_number VARCHAR(20)  NOT NULL,
    city          VARCHAR(100) NOT NULL,
    FOREIGN KEY (street_name, street_number, city) REFERENCES Address(street_name, street_number, city)
);

CREATE TABLE Hotel (
    hotel_id      SERIAL       PRIMARY KEY,
    name          VARCHAR(150) NOT NULL,
    street_name   VARCHAR(150) NOT NULL,
    street_number VARCHAR(20)  NOT NULL,
    city          VARCHAR(100) NOT NULL,
    FOREIGN KEY (street_name, street_number, city) REFERENCES Address(street_name, street_number, city)
);

CREATE TABLE Room (
    hotel_id        INTEGER     NOT NULL REFERENCES Hotel(hotel_id) ON DELETE CASCADE,
    room_number     INTEGER     NOT NULL,
    windows         INTEGER     NOT NULL,
    year            INTEGER     NOT NULL,
    access_type     VARCHAR(10) NOT NULL CHECK (access_type IN ('elevator', 'stairs')),
    PRIMARY KEY (hotel_id, room_number)
);

CREATE TABLE Booking (
    booking_id    SERIAL        PRIMARY KEY,
    email         VARCHAR(150)  NOT NULL REFERENCES Client(email),
    hotel_id      INTEGER       NOT NULL,
    room_number   INTEGER       NOT NULL,
    start_date    DATE          NOT NULL,
    end_date      DATE          NOT NULL,
    price_per_day NUMERIC(10,2) NOT NULL,
    FOREIGN KEY (hotel_id, room_number) REFERENCES Room(hotel_id, room_number),
    CHECK (end_date > start_date),
    -- Prevents overlapping bookings for the same room
    EXCLUDE USING GIST (
        hotel_id    WITH =,
        room_number WITH =,
        daterange(start_date, end_date, '[]') WITH &&
    )
);

-- review_id is scoped per hotel
CREATE TABLE Review (
    review_id   SERIAL        NOT NULL,
    hotel_id    INTEGER       NOT NULL REFERENCES Hotel(hotel_id) ON DELETE CASCADE,
    email       VARCHAR(150)  NOT NULL REFERENCES Client(email),
    message     TEXT,
    rating      INTEGER       NOT NULL CHECK (rating BETWEEN 0 AND 10),
    PRIMARY KEY (hotel_id, review_id)
);
