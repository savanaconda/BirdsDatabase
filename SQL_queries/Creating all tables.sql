CREATE SCHEMA Birds;
GO


/* Primary table */
DROP TABLE Birds.SpeciesSightings;

CREATE TABLE Birds.SpeciesSightings
(SightingID INTEGER IDENTITY PRIMARY KEY,
SpeciesID INTEGER NOT NULL,
AbsoluteDate DECIMAL(9,0) NOT NULL,
X_coordinates DECIMAL(7,0) NOT NULL,
Y_coordinates DECIMAL(7,0) NOT NULL,
Z_coordinates DECIMAL(7,0) NOT NULL);


/* Classification table */
DROP TABLE Birds.Classifications;

CREATE TABLE Birds.Classifications
(SpeciesID INTEGER IDENTITY PRIMARY KEY,
Species VARCHAR(100) NOT NULL,
Genus VARCHAR(100) NOT NULL);


/* Dates table */
DROP TABLE Birds.Dates;

CREATE TABLE Birds.Dates
(AbsoluteDate DECIMAL(9,0) IDENTITY PRIMARY KEY,
SightingDate DATE NOT NULL);


/* Locations table */
DROP TABLE Birds.Locations;

CREATE TABLE Birds.Locations
(X_coordinates DECIMAL(7,0) NOT NULL,
Y_coordinates DECIMAL(7,0) NOT NULL,
Z_coordinates DECIMAL(7,0) NOT NULL,
Latitude DECIMAL(9,6) NOT NULL,
Longitude DECIMAL(9,6) NOT NULL,
CONSTRAINT ThreeDim_Space PRIMARY KEY (X_coordinates, Y_coordinates, Z_coordinates));




SELECT COUNT(*)
FROM Birds.SpeciesSightings;


SELECT TOP 5 *
FROM Birds.SpeciesSightings;

SELECT TOP 5 *
FROM Birds.Classifications;

SELECT TOP 5 *
FROM Birds.Locations;

SELECT TOP 5 *
FROM Birds.Dates;