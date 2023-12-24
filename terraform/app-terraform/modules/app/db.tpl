<?php
session_start();

$conn = mysqli_connect(
  '${db_cluster}',
  'admin',
  '${db_password}',
  'php_mysql_crud'
) or die(mysqli_erro($mysqli));

?>