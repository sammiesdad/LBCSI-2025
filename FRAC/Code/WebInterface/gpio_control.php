<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $pin = escapeshellarg($_POST['pin']);
    $action = escapeshellarg($_POST['action']);
    
    $command = "python3 /home/frac-01/frac/gpio_control.py $pin $action";
    
    if ($pin == "doorcontact" && $action == "check") {
        $output = shell_exec($command);
        echo "<script>alert('$output');</script>";
    } else {
        shell_exec($command . " > /dev/null 2>&1 &");
        echo "<script>alert('$pin set to $action');</script>";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPIO Control</title>
</head>
<body>
    <h2>GPIO Control Panel</h2>
    <form method="post">
        <button type="submit" name="pin" value="alarm">Activate Alarm</button>
        <input type="hidden" name="action" value="on">
    </form>
    <form method="post">
        <button type="submit" name="pin" value="strike">Activate Strike</button>
        <input type="hidden" name="action" value="on">
    </form>
    <form method="post">
        <button type="submit" name="pin" value="doorcontact">Check Door Contact</button>
        <input type="hidden" name="action" value="check">
    </form>
</body>
</html>
