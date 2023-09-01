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