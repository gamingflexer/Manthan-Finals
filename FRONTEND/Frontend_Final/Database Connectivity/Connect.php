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
       echo "\n";
    }
?>