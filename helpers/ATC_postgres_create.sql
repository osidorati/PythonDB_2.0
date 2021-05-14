CREATE TABLE "atc" (
	"id_atc" serial NOT NULL,
	"caption" varchar(255) NOT NULL UNIQUE,
	"id_district" int NOT NULL,
	"address" varchar(255) NOT NULL,
	"year" DATE NOT NULL,
	"atc_state" BOOLEAN NOT NULL,
	"license" varchar(255) NOT NULL,
	CONSTRAINT "atc_pk" PRIMARY KEY ("id_atc")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "abonents" (
	"id" serial NOT NULL,
	"id_atc" int NOT NULL,
	"surname" varchar(255) NOT NULL,
	"name" varchar(255) NOT NULL,
	"middlename" varchar(255) NOT NULL,
	"phone_number" varchar(255) NOT NULL,
	"address" varchar(255) NOT NULL,
	"id_position" int NOT NULL,
	"id_benefit" int,
	"document" varchar(255),
	CONSTRAINT "abonents_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "benefit" (
	"id" serial NOT NULL,
	"type" varchar(255) NOT NULL UNIQUE,
	"terms" varchar(255) NOT NULL,
	"tarriff" float4 NOT NULL,
	CONSTRAINT "benefit_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "position" (
	"id" serial NOT NULL,
	"type_positon" varchar(255) NOT NULL UNIQUE,
	CONSTRAINT "position_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "district" (
	"id" serial NOT NULL,
	"name_district" varchar(255) NOT NULL UNIQUE,
	CONSTRAINT "district_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "calls" (
	"id" serial NOT NULL,
	"id_abonent" serial NOT NULL,
	"id_city" integer NOT NULL,
	"telephone_in" varchar(255) NOT NULL,
	"date" DATE NOT NULL,
	"duration" integer NOT NULL,
	"id_tariff" integer NOT NULL,
	"price_min" float4 NOT NULL,
	CONSTRAINT "calls_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "country" (
	"id" serial NOT NULL,
	"name_country" varchar(255) NOT NULL UNIQUE,
	"price" float4 NOT NULL,
	CONSTRAINT "country_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "city" (
	"id" serial NOT NULL,
	"id_country" integer NOT NULL,
	"name_city" varchar(255) NOT NULL,
	CONSTRAINT "city_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "tariff" (
	"id" serial NOT NULL,
	"type_tariff" varchar(255) NOT NULL UNIQUE,
	"time_start" TIME NOT NULL UNIQUE,
	"time_finish" TIME NOT NULL UNIQUE,
	"coefficient" float4 NOT NULL,
	CONSTRAINT "tariff_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



ALTER TABLE "atc" ADD CONSTRAINT "atc_fk0" FOREIGN KEY ("id_district") REFERENCES "district"("id") ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE "abonents" ADD CONSTRAINT "abonents_fk0" FOREIGN KEY ("id_atc") REFERENCES "atc"("id_atc") ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE "abonents" ADD CONSTRAINT "abonents_fk1" FOREIGN KEY ("id_position") REFERENCES "position"("id") ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE "abonents" ADD CONSTRAINT "abonents_fk2" FOREIGN KEY ("id_benefit") REFERENCES "benefit"("id") ON UPDATE CASCADE ON DELETE CASCADE;




ALTER TABLE "calls" ADD CONSTRAINT "calls_fk0" FOREIGN KEY ("id_abonent") REFERENCES "abonents"("id") ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE "calls" ADD CONSTRAINT "calls_fk1" FOREIGN KEY ("id_city") REFERENCES "city"("id") ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE "calls" ADD CONSTRAINT "calls_fk2" FOREIGN KEY ("id_tariff") REFERENCES "tariff"("id") ON UPDATE CASCADE ON DELETE CASCADE;


ALTER TABLE "city" ADD CONSTRAINT "city_fk0" FOREIGN KEY ("id_country") REFERENCES "country"("id") ON UPDATE CASCADE ON DELETE CASCADE;

