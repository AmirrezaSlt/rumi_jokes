CREATE KEYSPACE IF NOT EXISTS rumi
  WITH REPLICATION = { 
   'class' : 'SimpleStrategy', 
   'replication_factor' : 1 
  };
USE rumi;
CREATE TABLE IF NOT EXISTS skills
(
	user INT PRIMARY KEY,
	sname SET<TEXT>
);

