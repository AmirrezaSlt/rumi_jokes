CREATE KEYSPACE IF NOT EXISTS dbms
  WITH REPLICATION = { 
   'class' : 'SimpleStrategy', 
   'replication_factor' : 1 
  };
USE dbms;
DROP TABLE IF EXISTS skills;
  WITH REPLICATION = {
   'class' : 'SimpleStrategy',
   'replication_factor' : 1
  };
CREATE TABLE IF NOT EXISTS skills
(
	user INT PRIMARY KEY,
	sname SET<TEXT>
);

