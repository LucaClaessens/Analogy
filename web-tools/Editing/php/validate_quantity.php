<?php

header('Access-Control-Allow-Origin: *');

include "config.php";
include "connect.php";

$sql ="SELECT sentence_id FROM source_material WHERE active = 1";
$result = $conn->query($sql);

if ($result->num_rows < $MIN_POOL) {
	echo json_encode(array('config_ip' => $CONFIG_IP, 'config_port' => $CONFIG_PORT));
} else {
	echo json_encode("True");
}
$conn->close();

?>