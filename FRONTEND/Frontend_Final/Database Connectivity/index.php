<?php
        include_once('Connect.php');
        $db = new MyDB();
        $db = new SQLite3('ConnectFinal.db'); 
    $result = $db->query("SELECT u.id, n.name,u.num,u.email from Users u, username n where u.num=n.num"); 

    ?>

    <!DOCTYPE html>
    <html>
    <body background="2.png">
    <head>
     <title>Saved Profiles</title>
    </head>
    <style>
figure 
{
  display: inline-block;
  margin: 0px; 
}
figure img 
{
  float: left;
  width: 100px;
  height: 100px;
  background: #555;
}
figcaption 
{
  color: black;
  font-family: Montserrat;
  text-align: center;
  font-size: 12px;
}
.header p 
{
  text-align: left;
  position: center;
  top: 5px;
  left: 0px;
  font-family: Montserrat;
  font-size: 25px;
}
table.scrolldown {
            width: 100%;
              
            /* border-collapse: collapse; */
            border-spacing: 0;
            border: 2px solid black;
        }

</style>

<figure>
<img src="Logo.png" alt='missing'/>
</figure> 


<body>
    <table class="scrolldown" align="center" border="1px"  style="width:600px"; line-height:"40px;">
        <tr>
            <th colspan="4"><h2>Users Record</h2></th>
        </tr>
        <t>
            <th> ID</th>
            <th> Name </th>
            <th> Number </th>
            <th> Email </th>
        </t>
        <div>
<button class="button" style="position: absolute;right : 10px; top: 15px;width:150px; height:40px; border: 1px solid #888; font-weight: bolder;border-radius: 12px;"><a style="text-decoration:none" href="./home page.html">Go Back</a></button>
<button class="button" style="position: absolute; right: 10px; top: 60px;width:150px; height:40px; border: 1px solid #888; font-weight: bolder;border-radius: 12px"><a style="text-decoration:none" href="./network graph.html">Network Graph</a></button>
</div>

        <?php
      while($rows = $result->fetchArray())
        {
            ?>
            <tr>
                <td><?php echo $rows['id']; ?> </td>
                <td><?php echo $rows['name']; ?></td>
                <td><?php echo $rows['num']; ?></td>
                <td><?php echo $rows['email']; ?></td>
            </tr>
            <?php 
        }
        ?>
    </table>
</body>
</html>

