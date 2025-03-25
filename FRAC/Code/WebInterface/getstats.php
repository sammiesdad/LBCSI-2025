<?php
header('Content-Type: application/json');
$data = [];

// --- CPU Usage ---
$cpuLine = shell_exec("/usr/bin/top -bn1 | grep 'Cpu(s)'");
$cpu_usage = "N/A";
if ($cpuLine) {
    preg_match('/(\d+\.\d+)\s*\%?id/', $cpuLine, $matches);
    if (isset($matches[1])) {
        $idle = floatval($matches[1]);
        $cpu_usage = round(100 - $idle, 2);
    }
}
$data['cpu_usage'] = $cpu_usage;

// --- Memory Usage ---
$free = shell_exec('free -m');
$lines = explode("\n", trim($free));
if (isset($lines[1])) {
    $mem = preg_split('/\s+/', $lines[1]);
    $total = isset($mem[1]) ? intval($mem[1]) : 0;
    $used = isset($mem[2]) ? intval($mem[2]) : 0;
    $mem_percent = ($total > 0) ? round(($used / $total) * 100, 2) : 0;
    $data['memory'] = ['total' => $total, 'used' => $used, 'percent' => $mem_percent];
} else {
    $data['memory'] = ['total' => "N/A", 'used' => "N/A", 'percent' => "N/A"];
}

// --- Temperature ---
$temp = shell_exec("/opt/vc/bin/vcgencmd measure_temp");
if ($temp) {
    $data['temperature'] = trim($temp);
} else {
    $raw = @file_get_contents("/sys/class/thermal/thermal_zone0/temp");
    if ($raw) {
        $data['temperature'] = round($raw / 1000, 1) . "°C";
    } else {
        $data['temperature'] = "N/A";
    }
}

// --- Disk Usage ---
$total_space = disk_total_space("/");
$free_space = disk_free_space("/");
$used_space = $total_space - $free_space;
$total_gb = round($total_space / (1024 * 1024 * 1024), 2);
$used_gb = round($used_space / (1024 * 1024 * 1024), 2);
$disk_percent = ($total_space > 0) ? round(($used_space / $total_space) * 100, 2) : 0;
$data['disk'] = ['total' => $total_gb, 'used' => $used_gb, 'percent' => $disk_percent];

// --- Network Statistics ---
$net_data = file_get_contents("/proc/net/dev");
$network_stats = [];
if ($net_data) {
    $lines = explode("\n", trim($net_data));
    // Skip the first two header lines
    for ($i = 2; $i < count($lines); $i++) {
        $line = trim($lines[$i]);
        if (empty($line)) continue;
        list($iface, $stats_str) = explode(":", $line, 2);
        $iface = trim($iface);
        $stats = preg_split('/\s+/', trim($stats_str));
        $network_stats[$iface] = [
            'rx_bytes'   => isset($stats[0]) ? $stats[0] : 0,
            'rx_packets' => isset($stats[1]) ? $stats[1] : 0,
            'tx_bytes'   => isset($stats[8]) ? $stats[8] : 0,
            'tx_packets' => isset($stats[9]) ? $stats[9] : 0,
        ];
    }
}
$data['network'] = $network_stats;

// --- GPIO Status using read_gpio.py ---
// Execute the Python script to get current GPIO values.
$gpio_output = shell_exec('python3 read_gpio.py');
if ($gpio_output) {
    $gpio_values = json_decode($gpio_output, true);
    if (is_array($gpio_values)) {
        $data['gpio'] = $gpio_values;
    } else {
        $data['gpio'] = "Error: Unable to decode GPIO JSON.";
    }
} else {
    $data['gpio'] = "Error: Unable to execute GPIO script.";
}

echo json_encode($data);
?>
