<?php
$ds = DIRECTORY_SEPARATOR;
 
$storeFolder = 'uploads';
 
if (!empty($_FILES)) {
    // check if name is valid
    if(!isset($_POST['name']) || empty($_POST['name'])) {
        $json = json_encode(["success" => false, "error" => "No nickname has been received"]);
        header('Content-type: application/json');
        header('Expires: 0');
        print($json);
        exit;
    } 

    $nickname = $_POST['name'];
    
    // new folder is nickname with a timestamp to make unique folder names
    $folderName = $nickname . "___" . time() . $ds;
    $targetPath = dirname( __FILE__ ) . $ds. $storeFolder . $ds . $folderName;
    mkdir($targetPath, 0777);

    for($i = 0; $i < count($_FILES['file']['name']); $i++) {
        // temporary file
        $tempFile = $_FILES['file']['tmp_name'][$i];
        // destination file: use $_FILES['file']['name'][$i] for picking the original file name
        $name = $i . ".";
        $ext = pathinfo($_FILES['file']['name'][$i], PATHINFO_EXTENSION);

        // create a new file in the target folder
        $targetFile =  $targetPath . $name . $ext;

        move_uploaded_file($tempFile, $targetFile);
        chmod($targetFile, 0777);
    }

    // Convert to JSON
    $json = json_encode(["success" => true]);
    header('Content-type: application/json');
    header('Expires: 0');   // Prevent caching
    
    print($json);
    exit;
     
} else {

    $json = json_encode(["success" => false, "error" => "No file has been received"]);
    header('Content-type: application/json');
    header('Expires: 0');
    
    print($json);
    exit;

}
?>   