<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Raspberry Pi 5 Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    .metric { margin-bottom: 10px; }
    table { border-collapse: collapse; width: 100%; margin-top: 20px; }
    th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
  </style>
</head>
<body>
  <h1>Raspberry Pi 5 Dashboard</h1>
  <div id="stats">
    <!-- Metrics will be updated here -->
    <div class="metric" id="cpu"></div>
    <div class="metric" id="memory"></div>
    <div class="metric" id="temperature"></div>
    <div class="metric" id="disk"></div>
  </div>
  
  <h2>GPIO Status</h2>
  <table id="gpioTable">
    <thead>
      <tr>
        <th>GPIO Pin</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      <!-- GPIO status rows will be inserted here -->
    </tbody>
  </table>

<script>
// This function fetches the latest stats every second.
function updateDashboard() {
  fetch('getstats.php')
    .then(response => response.json())
    .then(data => {
      // Update performance metrics
      document.getElementById('cpu').innerHTML = "<strong>CPU Usage:</strong> " + data.cpu_usage + "%";
      document.getElementById('memory').innerHTML = "<strong>Memory:</strong> " + data.memory.used + "MB / " + data.memory.total + "MB (" + data.memory.percent + "% used)";
      document.getElementById('temperature').innerHTML = "<strong>Temperature:</strong> " + data.temperature;
      document.getElementById('disk').innerHTML = "<strong>Disk Usage:</strong> " + data.disk.used + "GB / " + data.disk.total + "GB (" + data.disk.percent + "% used)";
      
      // Update GPIO table
      let gpioRows = "";
      for (let pin in data.gpio) {
        gpioRows += "<tr><td>" + pin + "</td><td>" + data.gpio[pin] + "</td></tr>";
      }
      document.querySelector("#gpioTable tbody").innerHTML = gpioRows;
    })
    .catch(error => console.error('Error:', error));
}

// Refresh stats every 1 second
setInterval(updateDashboard, 1000);
updateDashboard();
</script>
</body>
</html>
