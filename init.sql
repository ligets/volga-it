CREATE DATABASE timetable_db
       OWNER "user";

CREATE DATABASE hospital_db
       OWNER "user";

CREATE DATABASE account_db
       OWNER "user";

CREATE DATABASE documents_db
       OWNER "user";



GRANT ALL PRIVILEGES ON DATABASE timetable_db TO "user";
GRANT ALL PRIVILEGES ON DATABASE hospital_db TO "user";
GRANT ALL PRIVILEGES ON DATABASE account_db TO "user";
GRANT ALL PRIVILEGES ON DATABASE documents_db TO "user";
