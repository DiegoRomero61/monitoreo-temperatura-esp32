<?php
$conexion = new mysqli("localhost", "root", "", "iot");

$data = json_decode(file_get_contents("php://input"), true);

$temp = $data['temperatura'];
$hum = $data['humedad'];

$sql = "INSERT INTO datos (temperatura, humedad, fecha) 
        VALUES ('$temp', '$hum', NOW())";

$conexion->query($sql);
?>
