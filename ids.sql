-- Schema for ids application database

create table flows (
    id integer primary key autoincrement not null,
    sequence integer not null,
    cookie integer not null,
    dpid text not null,
    in_port integer not null,
    dl_src text not null,
    dl_dst text not null,
    type integer  not null,
    vlan integer,
    ip_src text not null,
    ip_dst text  not null,
    ip_proto integer  not null,
    s_port integer,
    d_port integer,
    pkts integer not null,
    bytes integer not null,
    duration integer not null
);
