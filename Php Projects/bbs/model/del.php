<?php

include '../init.php';

include DIR_CORE . 'conn.php';



//  接收pub_id
$pub_id = $_GET['pub_id']; 
$rep_id = $_GET['rep_id']; 

// 删除回复
$sql = "delete from reply where rep_id=$rep_id";
$conn->query($sql); // 连接数据库执行删除


// 提取楼主的帖子的信息
$sql = "select * from publish where pub_id=$pub_id";
$result = $conn->query($sql); // 得到了资源结果集
$row = $result->fetch_assoc(); // 楼主的帖子的信息

// 以下的代码跟分页有关
//  接收当前页码数
$pageN = isset($_GET['num']) ? $_GET['num'] : 1;
// 定义每一页显示的记录数
$rowsPerPage = 5;
// 查询总记录数
$sql = "select count(*) as sum from reply where rep_pub_id=$pub_id";
$result = $conn->query($sql);
$row_num = $result->fetch_assoc(); // 还是一个数组
$rowCount = $row_num['sum']; // 得到总记录数
// 计算总页数
$sum_page = ceil($rowCount / $rowsPerPage);

// 拼凑出页码字符串
$strPage = '';
// 拼凑出“首页”
$strPage .= "<a href='./showlist.php?pub_id=$pub_id&action=reply&num=1'>首页</a>";
// 拼凑出“上一页”
$preN = $pageN == 1 ? 1 : $pageN - 1;
$strPage .= "<a href='./showlist.php?pub_id=$pub_id&action=reply&num=$preN'><<上一页</a>";
// 确定显示的第1个页码$startN的值
if($pageN <= 3) {
	$startN = 1;
}else {
	$startN = $pageN - 2;
}
// 确定$startN的最大值
if($startN > $sum_page - 4) {
	$startN = $sum_page - 4;
}
// 防止$startN出现负值
if($startN <= 1) {
	$startN = 1;
}
// 确定显示的最后1个页码$endN的值
$endN = $startN + 4;
// 防止$endN越界
if($endN > $sum_page) {
	$endN = $sum_page;
}

// 拼凑出中间的页码
for($i=$startN;$i<=$endN;$i++) {
	if($i == $pageN) {
		$strPage .= "<a href='./showlist.php?pub_id=$pub_id&action=reply&num=$i' style='background:#105cb6;color:white;'>$i</a>";
	}else {
		$strPage .= "<a href='./showlist.php?pub_id=$pub_id&action=reply&num=$i'>$i</a>";
	}	
}
// 拼凑出“下一页”
$nextN = $pageN == $sum_page ? $sum_page : $pageN + 1;
$strPage .= "<a href='./showlist.php?pub_id=$pub_id&action=reply&num=$nextN'>下一页>></a>";
// 拼凑出“尾页”
$strPage .= "<a href='./showlist.php?pub_id=$pub_id&action=reply&num=$sum_page'>尾页</a>";
// 拼凑出“总页数”
$strPage .= "总页数:$sum_page";
// 分页到此结束

// 提取回帖的资源结果集
$offset = ($pageN - 1) * $rowsPerPage;
$rep_sql = "select * from reply where rep_pub_id = $pub_id order by rep_time limit $offset, $rowsPerPage";
$rep_result = $conn->query($rep_sql);


include DIR_VIEW . 'showlist.html';

$conn->close();