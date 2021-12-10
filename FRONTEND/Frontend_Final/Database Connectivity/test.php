<?php
   class MyDB extends SQLite3
   {
      function __construct()
      {
         $this->open('ConnectFinal.db');
      }
   }
   $db = new MyDB();
   if(!$db){
      echo $db->lastErrorMsg();
   } else {
      echo "Opened database successfully\n";
   }

   $sql =<<<EOF
   
      CREATE TABLE IF NOT EXISTS users
      ( 
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         email varchar(50) NOT NULL,
         num int NOT NULL,
         CONSTRAINT name_unique UNIQUE (email, num)
      );
      
      CREATE TABLE IF NOT EXISTS username
      (
         num int NOT NULL,
         name varchar(125) DEFAULT 'XYZ'
      );

      

EOF;

   $ret = $db->exec($sql);
   if(!$ret){
      echo $db->lastErrorMsg();
   } else {
      echo "Table created successfully\n";
   }
   $db->close();
?>