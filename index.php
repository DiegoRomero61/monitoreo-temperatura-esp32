<?php
$conexion = new mysqli("localhost", "root", "", "iot");

$resultado = $conexion->query("SELECT * FROM datos ORDER BY id DESC LIMIT 20");

$temps = [];
$hums = [];
$fechas = [];

while($fila = $resultado->fetch_assoc()){
    $temps[] = $fila['temperatura'];
    $hums[] = $fila['humedad'];
    $fechas[] = $fila['fecha'];
}
?>

<html>
<head>
    <title>Monitor IoT</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>

<h2>Gráfica de Temperatura y Humedad</h2>

<canvas id="grafica"></canvas>

<script>
const ctx = document.getElementById('grafica').getContext('2d');

const grafica = new Chart(ctx, {
    type: 'line',
    data: {
        labels: <?php echo json_encode($fechas); ?>,
        datasets: [
            {
                label: 'Temperatura',
                data: <?php echo json_encode($temps); ?>,
                borderWidth: 2
            },
            {
                label: 'Humedad',
                data: <?php echo json_encode($hums); ?>,
                borderWidth: 2
            }
        ]
    }
});
</script>

</body>
</html>
