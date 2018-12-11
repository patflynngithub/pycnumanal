            insert into programs (program_name, description, cmd_line_prefix)
            values ('l2 vector norm', 'l2 vector norm in C', 'l2vecnorm');

            insert into programs (program_name, description, cmd_line_prefix)
            values ('second program', 'second program description', 'second_program_prefix');

            insert into timings (problem_size, timing, program_name)
            values (100, 0.000004, 'l2 vector norm' );

            insert into timings (problem_size, timing, program_name)
            values (1000, 0.000012, 'l2 vector norm' );

            insert into timings (problem_size, timing, program_name)
            values (10000, 0.000088, 'l2 vector norm' );

            insert into timings (problem_size, timing, program_name)
            values (100000, 0.001262, 'l2 vector norm' );

            insert into timings (problem_size, timing, program_name)
            values (1000000, 0.011269, 'l2 vector norm' );

            insert into timings (problem_size, timing, program_name)
            values (1, 2, 'second program' );

