CREATE TABLE IF NOT EXISTS "data" (
	"uid"	INTEGER,
	"iid"	INTEGER,
	"year"	INTEGER,
	"value"	NUMERIC,
	FOREIGN KEY("uid") REFERENCES "universities"("uid"),
	FOREIGN KEY("iid") REFERENCES "indicators"("iid")
);
CREATE TABLE IF NOT EXISTS "indicators" (
	"iid"	INTEGER NOT NULL,
	"number"	TEXT,
	"name"	TEXT UNIQUE,
	"unit"	TEXT,
	PRIMARY KEY("iid")
);
CREATE TABLE IF NOT EXISTS "federal_districts" (
	"fdid"	INTEGER,
	"name"	TEXT UNIQUE,
	PRIMARY KEY("fdid")
);
CREATE TABLE IF NOT EXISTS "universities" (
	"uid"	INTEGER NOT NULL,
	"name"	TEXT,
	"address"	TEXT,
	"ministry"	TEXT,
	"website"	TEXT,
	"owner"	TEXT,
	"fdid"	INTEGER NOT NULL,
	PRIMARY KEY("uid"),
	FOREIGN KEY("fdid") REFERENCES "federal_districts"("fdid")
);
CREATE TABLE IF NOT EXISTS "ugn" (
	"ugnid"	INTEGER NOT NULL,
	"name"	TEXT UNIQUE,
	PRIMARY KEY("ugnid")
);
CREATE TABLE IF NOT EXISTS "uni_ugn" (
	"ugnid"	INTEGER NOT NULL,
	"uid"	INTEGER NOT NULL,
	"year"	INTEGER NOT NULL,
	"people"	NUMERIC NOT NULL,
	FOREIGN KEY("ugnid") REFERENCES "ugn"("ugnid"),
	FOREIGN KEY("uid") REFERENCES "universities"("uid")
);
CREATE VIEW count (X) AS
	WITH RECURSIVE
	  cnt(x) AS (
		 SELECT 1
		 UNION ALL
		 SELECT x+1 FROM cnt
		  LIMIT 36000
	  )
	SELECT x FROM cnt
/* count(X) */;
CREATE VIEW studentsege (year, students, ege) AS
	SELECT a.year as year, a.value as students, c.value as ege from data a
	INNER JOIN data c ON (a.uid = c.uid AND a.year = c.year)
	WHERE a.iid = 1 AND c.iid = 5 AND ege > 0
	ORDER BY a.value
/* studentsege(year,students,ege) */;
