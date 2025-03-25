<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Raspberry Pi 5 Dashboard</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
      background: #f0f0f0;
    }
    .container {
      display: flex;
      flex-wrap: wrap;
    }
    .column {
      flex: 1;
      padding: 20px;
      box-sizing: border-box;
    }
    .left {
      border-right: 1px solid #ccc;
    }
    h1 {
      text-align: center;
      margin-bottom: 20px;
    }
    h2 {
      background-color: #007acc;
      color: #fff;
      padding: 10px;
      margin-top: 0;
      margin-bottom: 10px;
      border-radius: 5px;
    }
    .metric {
      margin-bottom: 10px;
      background: #fff;
      padding: 10px;
      border-radius: 5px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    table {
      border-collapse: collapse;
      width: 100%;
      margin-top: 10px;
      background: #fff;
      border-radius: 5px;
      overflow: hidden;
    }
    th, td {
      border: 1px solid #ddd;
      padding: 8px;
      text-align: center;
    }
    th {
      background-color: #007acc;
      color: white;
    }
    /* PiCamera2 live stream displayed using an img tag */
    #video {
      width: 100%;
      height: auto;
      border: 2px solid #007acc;
      border-radius: 5px;
      margin-bottom: 20px;
    }
  </style>
</head>
<body>
  <h1>Raspberry Pi 5 Dashboard</h1>
  <div class="container">
    <!-- Left Column: Hardware and Network Statistics -->
    <div class="column left">
      <h2>Hardware Statistics</h2>
      <div class="metric" id="hardware">
        <!-- CPU, memory, temperature, disk usage, etc. will be inserted here -->
    	<div class="metric" id="cpu"></div>
    	<div class="metric" id="memory"></div>
    	<div class="metric" id="temperature"></div>
    	<div class="metric" id="disk"></div>
      </div>
      
      <h2>Network Statistics</h2>
      <table id="networkTable">
        <thead>
          <tr>
            <th>Interface</th>
            <th>RX Bytes</th>
            <th>RX Packets</th>
            <th>TX Bytes</th>
            <th>TX Packets</th>
          </tr>
        </thead>
        <tbody>
          <!-- Network stats rows will be inserted here -->
        </tbody>
      </table>
    </div>
    
    <!-- Right Column: PiCamera2 Live Stream and GPIO Status -->
    <div class="column right">
      <h2>PiCamera2 Live Stream</h2>
      <!-- Update the src attribute to point to your actual live stream URL -->
      <img id="video" src="http://192.168.1.161:5000/video_feed" alt="PiCamera2 Live Stream">
      
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
    </div>
  </div>

  <script>
    // Update the dashboard every second.
    function updateDashboard() {
      fetch('getStats.php')
        .then(response => response.json())
        .then(data => {
          // Update Hardware Statistics (CPU, Memory, Temperature, Disk)
          document.getElementById('hardware').innerHTML =
            "<strong>CPU Usage:</strong> " + data.cpu_usage + "%<br>" +
            "<strong>Memory:</strong> " + data.memory.used + "MB / " + data.memory.total + "MB (" + data.memory.percent + "% used)<br>" +
            "<strong>Temperature:</strong> " + data.temperature + "<br>" +
            "<strong>Disk Usage:</strong> " + data.disk.used + "GB / " + data.disk.total + "GB (" + data.disk.percent + "% used)";
          
          // Update Network Statistics table
          let netRows = "";
          for (let iface in data.network) {
            let ifaceData = data.network[iface];
            netRows += "<tr><td>" + iface + "</td>" +
                       "<td>" + ifaceData.rx_bytes + "</td>" +
                       "<td>" + ifaceData.rx_packets + "</td>" +
                       "<td>" + ifaceData.tx_bytes + "</td>" +
                       "<td>" + ifaceData.tx_packets + "</td></tr>";
          }
          document.querySelector("#networkTable tbody").innerHTML = netRows;
          
          // Update GPIO Status table
          let gpioRows = "";
          if (typeof data.gpio === 'object') {
            for (let pin in data.gpio) {
              gpioRows += "<tr><td>" + pin + "</td><td>" + data.gpio[pin] + "</td></tr>";
            }
          } else {
            gpioRows = "<tr><td colspan='2'>" + data.gpio + "</td></tr>";
          }
          document.querySelector("#gpioTable tbody").innerHTML = gpioRows;
        })
        .catch(error => console.error('Error:', error));
    }

    // Refresh stats every second.
    setInterval(updateDashboard, 1000);
    updateDashboard();
  </script>
</body>
</html>
