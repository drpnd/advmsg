create table cert (
        serial char(40) primary key not null,
        cn char(64) not null,
        cert text,
        active bool not null
);
create index cert_index on cert (cn, active);
insert into cert (serial, cn, cert, active) values ('0000000000000000000000000000000000000001', '', null, 1);

