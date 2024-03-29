-- This script was generated by a beta version of the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE public."softcartDimDate"
(
    dateid integer,
    date date,
    "Year" integer,
    "Quarter" integer,
    "QuearterName" "char",
    "Month" integer,
    "Monthname" "char",
    "Day" integer,
    "WeekdayName" "char",
    PRIMARY KEY (dateid)
);

CREATE TABLE public."softcartDimCategory"
(
    categoryid integer,
    category "char",
    PRIMARY KEY (categoryid)
);

CREATE TABLE public."softcartDImItem"
(
    itemid integer,
    item "char",
    PRIMARY KEY (itemid)
);

CREATE TABLE public."softcartDimCountry"
(
    countryid integer,
    country "char",
    PRIMARY KEY (countryid)
);

CREATE TABLE public."softcartFactSales"
(
    "Orderid" integer,
    dateid integer,
    countryid integer,
    categoryid integer,
    amount integer,
    itemid integer,
    PRIMARY KEY ("Orderid")
);

ALTER TABLE public."softcartFactSales"
    ADD FOREIGN KEY (dateid)
    REFERENCES public."softcartDimDate" (dateid)
    NOT VALID;


ALTER TABLE public."softcartFactSales"
    ADD FOREIGN KEY (countryid)
    REFERENCES public."softcartDimCountry" (countryid)
    NOT VALID;


ALTER TABLE public."softcartFactSales"
    ADD FOREIGN KEY (itemid)
    REFERENCES public."softcartDImItem" (itemid)
    NOT VALID;


ALTER TABLE public."softcartFactSales"
    ADD FOREIGN KEY (categoryid)
    REFERENCES public."softcartDimCategory" (categoryid)
    NOT VALID;

END;