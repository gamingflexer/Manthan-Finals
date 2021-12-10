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

 

?>



 <?php 
    
    $email=$_REQUEST['email']; 
    $num=$_REQUEST['num']; 

   
   $sql =<<<EOF
      INSERT INTO users (email, num)
      VALUES ('$email', '$num');

      INSERT INTO username(num)
      VALUES('$num');
EOF;

   $ret = $db->exec($sql);
   if(!$ret){
     echo $db->lastErrorMsg();
   } else {
     echo "Records created successfully\n";
   }
   $db->close();
?>