<?php
include "config.php";
include "connect.php";

$stmt = $conn->prepare("INSERT INTO selected_text (selected_length, selected_data, score) VALUES (?, ?, 1) ON DUPLICATE KEY UPDATE score = (score+1)");	
$stmt->bind_param("is", $length, $data);

$length = $_POST["selected_length"];
$data = $_POST["selected_data"];
$stmt->execute();

$stmt = $conn->prepare("UPDATE selected_text SET active = 1 WHERE score >= ?");
$stmt->bind_param("s", $SELECTED_ACTIVE_MIN);
$stmt->execute();


echo "New records created successfully.";

$stmt->close();
$conn->close();
?>