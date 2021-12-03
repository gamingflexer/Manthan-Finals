<?php
    $email = _POST['email'];

   //Database connection
    $conn = new mysqli('localhost','root','','manthan_final');
    if($conn->connection_error){
        die('Connection Failed' : $conn->connection_error);
    }
    else{
        $stmt = $conn->prepare("insert into email(Email) values(?)");
        $stmt->bind_param("s",$Email);
        $stmt-?execute();
        echo "Finding...";
        $stmt->close();
        $conn->close();
    }

?>