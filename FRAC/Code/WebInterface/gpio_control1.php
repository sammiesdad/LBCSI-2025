<?php
// Function to get the real-time GPIO status
function get_status() {
    $command = "sudo /usr/bin/python3 /home/frac-01/frac/gpio_control2.py status check 2>&1";
    $output = shell_exec($command);
    $status = json_decode($output, true);

    if ($status === null) {
        return ["error" => "Failed to retrieve status", "output" => $output];
    }
    return $status;
}

// Handle button press and execute corresponding action
$command_output = "";
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $pin = escapeshellarg($_POST['pin']);
    $action = escapeshellarg($_POST['action']);
    $command = "sudo /usr/bin/python3 /home/frac-01/frac/gpio_control2.py $pin $action --duration 4 2>&1";
    $command_output = shell_exec($command);
}

// Get the latest GPIO status
$status = get_status();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPIO Control</title>
    <style>
        .status-text {
            font-weight: bold;
        }
        .closed { color: green; }
        .open { color: red; }
    </style>
</head>
<body>
    <h2>GPIO Control Panel</h2>

    <h3>Real-Time GPIO Status:</h3>
    <p><strong>Alarm Status:</strong> <?php echo htmlspecialchars($status["alarm"]); ?></p>
    <p><strong>Strike Status:</strong> <?php echo htmlspecialchars($status["strike"]); ?></p>
    <p><strong>Door Contact Status:</strong> 
        <span class="status-text <?php echo ($status["doorcontact"] == "CLOSED") ? "closed" : "open"; ?>">
            <?php echo htmlspecialchars($status["doorcontact"]); ?>
        </span>
    </p>

    <h3>Command Output:</h3>
    <p><?php echo nl2br(htmlspecialchars($command_output)); ?></p>

    <form method="post">
        <button type="submit" name="pin" value="alarm">
            <?php echo ($status["alarm"] == "ON") ? "Deactivate Alarm" : "Activate Alarm"; ?>
        </button>
        <input type="hidden" name="action" value="<?php echo ($status["alarm"] == "ON") ? "off" : "on"; ?>">
    </form>

    <form method="post">
        <button type="submit" name="pin" value="strike">
            <?php echo ($status["strike"] == "ON") ? "Deactivate Strike" : "Activate Strike"; ?>
        </button>
        <input type="hidden" name="action" value="<?php echo ($status["strike"] == "ON") ? "off" : "on"; ?>">
    </form>

    <form method="post">
        <button type="submit" name="pin" value="status">Refresh Status</button>
        <input type="hidden" name="action" value="check">
    </form>
</body>
</html>
