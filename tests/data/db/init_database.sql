PRAGMA writable_schema = 1;
DELETE FROM sqlite_master WHERE type IN ('table', 'index', 'trigger');
PRAGMA writeable_schema = 0;
VACUUM;

CREATE TABLE `events` (
    `eventId`          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `internalName`     TEXT NOT NULL,
    `externalName`     TEXT NOT NULL,
    `startTime`        INTEGER NOT NULL,
    `endTime`          INTEGER NOT NULL,
    `currencyId`       TEXT NOT NULL,
    `startingAmount`   REAL,
    `targetAmount`     REAL NOT NULL,
    `sourceUrl`        TEXT NOT NULL,
    `updateDelay`      INTEGER
);

CREATE TABLE `donations` (
    `donationId`     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `eventId`        INTEGER NOT NULL,
    `timeRecorded`   INTEGER NOT NULL,
    `donationAmount` REAL NOT NULL,
    `runningTotal`   REAL NOT NULL,
    `notes`          TEXT,
    `valid`          INTEGER NOT NULL CHECK (valid BETWEEN 0 AND 1),
    FOREIGN KEY(eventId) REFERENCES events(eventId)
);

CREATE TABLE `donationRegressions` (
    `donationRegressionId`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `eventId`               INTEGER NOT NULL,
    `donationId`            INTEGER NOT NULL,
    `previousTotal`         REAL NOT NULL,
    `newTotal`              REAL NOT NULL,
    FOREIGN KEY(eventId) REFERENCES events(eventId),
    FOREIGN KEY(donationId) REFERENCES donations(donationId)
);

INSERT INTO `events` (eventId, internalName, externalName, startTime, endTime, currencyId, startingAmount, targetAmount, sourceUrl, updateDelay)
VALUES
(1, "TestOne", "Test One Title", 1477256983, 1477256985, "GBP", 0, 1000, "http://127.0.0.1:5000/justgiving", 5),
(2, "TestTwo", "Test Two Title", 1477256989, 1477256995, "USD", 10.0, 1000, "http://127.0.0.1:5000/justgiving", 5),
(3, "TestThree", "Test Three Title", 1477256999, 1477257999, "GBP", 3000.5, 5000, "http://127.0.0.1:5000/justgiving", 5),
(4, "TestFour", "Test Four Title", 1477256999, 1477257999, "GBP", 0, 5000, "http://127.0.0.1:5000/justgiving", 5),
(5, "NoDonations", "Test Five Title", 0, 9999999999999, "EUR", 100, 1000, "http://127.0.0.1:5000/justgiving", 5),
(6, "LastOneInvalid", "Last Donation Invalid", 0, 9999999999999, "EUR", 0, 1000, "http://127.0.0.1:5000/justgiving", 5),
(7, "OnlyInvalid", "Only Invalid Donations", 0, 9999999999999, "EUR", 100, 1000, "http://127.0.0.1:5000/justgiving", 5);

INSERT INTO `donations` (donationId, eventId, timeRecorded, donationAmount, runningTotal, notes, valid)
VALUES
(1, 1, 1477256983, 10.5, 10.5, NULL, 1),
(2, 1, 1477256988, 10.5, 21.0, NULL, 1),
(3, 1, 1477256990, 5.33, 26.33, NULL, 1),
(4, 1, 1477256999, 10.5, 36.83, NULL, 1),
(5, 1, 1477256999, 63.17, 100.0, NULL, 1),

(6, 2, 1477257000, 10.0, 20.0, NULL, 1),
(7, 2, 1477257010, 10.0, 30.0, NULL, 1),
(8, 2, 1477257020, -10.0, 20.0, "Mistake", 0),

(9, 3, 1477257030, -10.0, 10.0, "Mistake 2", 0),
(10, 3, 1477257040, 100.0, 3100.0, NULL, 1),
(11, 3, 1477257050, 100.0, 3200.0, NULL, 1),
(12, 3, 1477257060, 100.0, 3300.0, NULL, 1),

(13, 4, 1477257070, 100.0, 100.0, NULL, 1),
(14, 4, 1477257081, -25.0, 75.0, "Chargeback", 0),
(15, 4, 1477257092, 75.0, 150.0, NULL, 1),

(16, 6, 1477257102, 100, 100, NULL, 1),
(17, 6, 1477257104, 50, 150, NULL, 1),
(18, 6, 1477257114, -100, 50.0, "Regression", 0),

(19, 7, 1477257122, -50, 50.0, "Regression", 0),
(20, 7, 1477257133, -50, 0.0, "Regression", 0);

INSERT INTO `donationRegressions` (donationRegressionId, eventId, donationId, previousTotal, newTotal)
VALUES
(1, 2, 8, 30.0, 20.0),
(2, 2, 9, 20.0, 10.0),
(3, 4, 14, 100, 75.0),
(4, 6, 18, 150, 50.0),
(5, 7, 18, 100, 50.0),
(6, 7, 19, 50, 0);