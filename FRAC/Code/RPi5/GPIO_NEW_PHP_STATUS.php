<!DOCTYPE html>
<html>
<head>
    <title>Sensor Status Dashboard</title>
    <script>
        function fetchStatus() {
            fetch('sensor_status.json')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('doorswitch').innerHTML = data.doorswitch ? '<b style=\"color:red;\">Open</b>' : '<b style=\"color:green;\">Closed</b>';
                    document.getElementById('duress').innerHTML = data.duress ? '<b style=\"color:red;\">Active</b>' : '<b style=\"color:green;\">Normal</b>';
                    document.getElementById('pir').innerHTML = data.PIR ? '<b style=\"color:red;\">Motion Detected</b>' : '<b style=\"color:green;\">No Motion</b>';
                })
                .catch(err => console.error('Error fetching status:', err));
        }

        setInterval(fetchStatus, 1000); // Refresh every second
        window.onload = fetchStatus;
    </script>
    <style>
        body { font-family: Arial, sans-serif; }
        .sensor { margin-bottom: 15px; }
    </style>
</head>
<body>
    <h2>Real-Time Sensor Status Dashboard</h2>

    <div class="sensor">Door Switch: <span id="doorswitch">Loading...</span></div>
    <div class="sensor">Duress Button: <span id="duress">Loading...</span></div>
    <div class="sensor">Motion Sensor (PIR): <span id="pir">Loading...</span></div>

</body>
</html>
