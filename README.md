# monvoscrap

Data scraping tool of Russian govt HE data. VERY WIP, but kind of usable.

The data comes from [Monitoring of Higher Education Organizations](https://monitoring.miccedu.ru/?m=vpo), organized by Russian Ministry of Higher Education & Sciences. 2013 & 2014 editions of the Monitoring use a different layout of their data pages, so these years' data is still WIP.

This repo contains SQLite database `db.sqlite`, which contains data of the Monitoring from 2015 and 2022 (each monitoring contain a previous year's data). Feel free to use it for your research or download the data yourself using `download_2015_plus.py`.

The script fills an SQLite database `db.sqlite` with following tables:
* `indicators` contain all indicators found in the Monitoring (`iid` being the primary key of the table)
* `federal_districts` contains federal districts (`fdid` being the primary key)
* `universities` contains universities' data: primary key `uid`, `name`, `address`, `ministry` (if it's a govt university), `owner`, `fdid` 
* `ugn` contains УГН (Укрупненные группы направлений подготовки) - a list of major specialization groupings, used by the Ministry to keep track of students' majors;
* `uni_ugn` contains yearly data regarding universities' `ugn` composition (`ugnid`, `uid`, `year` and `people`);
* `data` contains Monitoring data (`uid`, `iid`, `year` and `value`).