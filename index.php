<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TruePrice</title>
</head>
<body>
    <!-- The data encoding type, enctype, MUST be specified as below -->
    <form enctype="multipart/form-data" action="index.php" method="POST">
        <!-- MAX_FILE_SIZE must precede the file input field -->
        <input type="hidden" name="MAX_FILE_SIZE" value="3000000000" />
        <!-- Name of input element determines name in $_FILES array -->
        Send this file: <input name="userfile" type="file" />
        <input type="submit" value="Send File" />
    </form>

    <?php
        ini_set('display_errors', 1);
        ini_set('display_startup_errors', 1);
        error_reporting(E_ALL);
        if(isset($_FILES["userfile"])){
            echo("Analyzing...    ");
            $output = shell_exec(command: "python3 analyze.py Albert " . $_FILES["userfile"]['tmp_name']);
            echo $output;
            echo "Done.";
        }else{
            echo("No set file");
        }
    ?>
</body>
</html>