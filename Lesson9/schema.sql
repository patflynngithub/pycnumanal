create table algorithms (
    name         text primary key,
    description  text,
    program      text
);

-- Stores the timings for the above algorithms
create table timings (
    id           integer primary key autoincrement not null,
    problem_size integer,
    time         real,
    algorithm    text not null references algorithms(name)
);

