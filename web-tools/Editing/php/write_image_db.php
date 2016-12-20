<?php
include "config.php";
include "connect.php";
$return;

$stmt = $conn->prepare('SELECT image_id from images
WHERE image_url = ? and image_key = ? LIMIT 1');
$stmt->bind_param('ss', $url,$key);
$url = $_POST["source"];
$key = $_POST["text"];
$stmt->execute();
$stmt->bind_result($match_row); 
$stmt->fetch();

if ($stmt->num_rows > 0) {  
	$return=$match_row; 
	$stmt = $conn->prepare("UPDATE images SET key_score = key_score + 1 WHERE image_id = ?");
	$stmt->bind_param("s", $return);
	$stmt->execute();
	echo "entry existed, updated succesfully.";	
} else {
	$stmt = $conn->prepare("INSERT INTO images (image_url, image_key) VALUES (?, ?)");	
	$stmt->bind_param("ss", $url, $key);
	$stmt->execute();
	echo "entry new, inserted successfully.";	
}

$stmt = $conn->prepare("UPDATE images SET active = 1 WHERE score > ? AND active != 1");
$stmt->bind_param("s", $IMAGE_ACTIVE_MIN);
$stmt->execute();

$stmt->close();
$conn->close();
?>