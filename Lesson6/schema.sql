create table algorithm (
    name         text primary key,
    description  text,
    command_line text
);

-- Stores the timing for the run of one of the above algorithms
create table timings (
    id           integer primary key autoincrement not null,
    problem_size integer,
    time         real,
    algorithm    text not null references algorithm(name)
);

