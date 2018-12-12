-- Master table of programs
create table programs (
    program_name    text primary key,
    description     text,
    cmd_line_prefix text
);

-- Stores the timings for the above programs
--   12/12/2018:  added "on delete cascade" to program_name foreign key
create table timings (
    id           integer primary key autoincrement not null,
    problem_size integer,
    timing       real,
    program_name text not null references programs(program_name) on delete cascade
);

