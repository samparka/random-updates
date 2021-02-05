<?php
session_start();
include '../init.php';

include DIR_CORE . 'conn.php';

// 分页代码
// 接收当前页
$pageN = isset($_GET['num']) ? $_GET['num'] : 1;
// 定义每页显示页数
$rowsPerPage = 5;
// 查询总数
$sql = "select count(*) as sum from publish";
$result = $conn->query($sql);
$row = $result->fetch_assoc(); // 此处是存有总数的数组
$rowCount = $row['sum']; // 得到总数
// 计算总页数
$sum_page = ceil($rowCount / $rowsPerPage);

// 页码拼串
$strPage = '';
// 首页拼串
$strPage .= "<a href='./list.php?num=1'>首页</a>";
// 上一页拼串
$preN = $pageN == 1 ? 1 : $pageN - 1;
if($pageN != 1) {
	$strPage .= "<a href='./list.php?num=$preN'><<上一页</a>";
}

// $startN的值
if($pageN <= 3) {
	$startN = 1;
}else {
	$startN = $pageN - 2;
}
// $startN的最大值
if($startN > $sum_page - 4) {
	$startN = $sum_page - 4;
}
// $startN最小值1
if($startN <= 1) {
	$startN = 1;
}
// $endN的值定义
$endN = $startN + 4;
// 防止$endN取值超过总数
if($endN > $sum_page) {
	$endN = $sum_page;
}

// 中间页码拼串
for($i=$startN;$i<=$endN;$i++) {
	if($i == $pageN) {
		$strPage .= "<a href='./list.php?num=$i' style='background:#105cb6;color:white;'>$i</a>";
	}else {
		$strPage .= "<a href='./list.php?num=$i'>$i</a>";
	}	
}
// 下一页拼串
$nextN = $pageN == $sum_page ? $sum_page : $pageN + 1;
if($pageN != $sum_page) {
	$strPage .= "<a href='./list.php?num=$nextN'>下一页>></a>";
}
// 尾页拼串
$strPage .= "<a href='./list.php?num=$sum_page'>尾页</a>";
// 总页数拼串
$strPage .= "总页数:$sum_page";

// 分页代码结束

// 3.取出publish表中数据
$offset = ($pageN - 1) * $rowsPerPage;
$sql = "select * from publish order by pub_time desc limit $offset, $rowsPerPage";
$result = $conn->query($sql);

if ( $result->num_rows == 0 ) {
	$row  = array('pub_content' => '数据走丢了', 'pub_owner' => '');
}


include DIR_VIEW . 'list.html';
