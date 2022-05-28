drop database if exists shoe;
create database shoe;
use shoe;

create table Shoe_Items
(shoe_id varchar(64) not null primary key,
name varchar(64) not null,
price float default null,
quantity int default 1000,
description varchar(64) default null,
imagename varchar(64) default null);


INSERT INTO `Shoe_Items` (`shoe_id`, `name`, `price`, `description`,`imagename`) VALUES
(1, 'M and M Special', '221.50', 'Latest Drop of the season, get yours and fly now','mandmshoe'),
(2, 'Adidas Superstar 2022', '291.50', 'Be a superstar today','superstar'),
(3, 'Ultra Boost 2021', '101.50', '2021 but not a bad steal','ultraboost'),
(4,'Spidermen Yeezy 2022', '262.23','The Amazing Spiderman 3 is coming out real soon','spidermen'),
(5,'UltraFly Courtshoes', '22.23','Wear this and be one with the tennisball','ultraflycourtshoe'),
(6,'Takumi Sen Shoe', '62.21','Energize your running with this one of a kind shoe today','takumisen');
COMMIT;
