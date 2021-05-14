select atc.id_atc, atc.caption, district.name_district, atc.address, atc.year, atc.atc_state, atc.license from atc join district on atc.id_district = district.id;

select abonents.id, atc.caption, abonents.surname, abonents.name, abonents.middlename, abonents.phone_number, abonents.address, position.type_positon, benefit.type, abonents.document
from abonents join atc on abonents.id_atc = atc.id_atc
join position on abonents.id_position = position.id
left join benefit on abonents.id_benefit = benefit.id;

INSERT INTO city(id_country, name_city) values(3, 'Makeevka')

select city.id, country.name_country, city.name_city
from city join country on city.id_country = country.id;

select calls.id, abonents.surname, abonents.name, abonents.middlename, abonents.phone_number, city.name_city, calls.telephone_in, calls.date, calls.duration, tariff.type_tariff
from calls join abonents on calls.id_abonent = abonents.id
join city on calls.id_city = city.id
join tariff on calls.id_tariff = tariff.id;