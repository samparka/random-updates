<?php

//密码修改页业务逻辑

include '../init.php';

include  DIR_CORE . 'conn.php';

error_reporting(E_ALL^E_NOTICE);

//接受表单数据
$user_name = trim($_POST['user_name']);
$user_name2 = trim($_POST['user_name2']);
$user_password1 = trim($_POST['user_password1']);
$user_password2 = trim($_POST['user_password2']);
$vcode = trim($_POST['vcode']);


//密码逻辑
if ( empty($user_name) || empty($user_password1) || empty($user_password2) ) {

	jump('./forgp.php', '用户名和密码不能为空请重新修改');

}else if ( strlen($user_name) <3 || strlen($user_name>10) ) {

	jump('./forgp.php', '用户名在3到10位之间请您重新修改');

}else if ( $user_username !== $user_username2 ) {

	jump('./forgp.php', '两次用户名输入的不一致请您重新修改');

}else if ( $user_password1 !== $user_password2 ) {

	jump('./forgp.php', '两次密码输入的不一致请您重新修改');

}else if ( strlen($user_password1) <6  ) {

	jump('./forgp.php', '密码不符合安全策略，请输入6位以上 重新修改!');

}else {
	//加密写入数据库
	$user_password = md5($user_password1);
	// $sql = "insert into user values (null,'$user_name','$user_password',default)";
	$sql = "update user set user_password = '$user_password' where user_name = '$user_name' ";
	$result = $conn->query($sql);

	if ( $result ) {

		$conn->close();
		jump('./login.php', '密码修改成功,即将跳转到登录页面');

	} else {

		jump('./forgp.php', '未知错误,修改失败');

	}
}
