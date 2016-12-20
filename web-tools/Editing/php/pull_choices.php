<?php
include "config.php";
include "connect.php";

$sql = $conn->prepare("SELECT * FROM `selected_text` WHERE `selected_length` < ? AND active IS NULL ORDER BY RAND()*score ASC LIMIT 5");
$sql->bind_param("i", $MAX_SELECTED_LENGTH);
$sql->execute();
$result = $sql->get_result();
 
if ($result->num_rows >= 5) {
	$data = $result->fetch_all( MYSQLI_ASSOC );
	echo json_encode( $data );
	} else {
    echo json_encode("reload");
	}
$conn->close();
?>