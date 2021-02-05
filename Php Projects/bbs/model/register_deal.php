<?php

//注册页业务逻辑

include '../init.php';

include  DIR_CORE . 'conn.php';

error_reporting(E_ALL^E_NOTICE);

//接受表单数据
$user_name = trim($_POST['user_name']);
$user_password1 = trim($_POST['user_password1']);
$user_password2 = trim($_POST['user_password2']);
$vcode = trim($_POST['vcode']);



//用户名查询语句
$sql = "select * from user where user_name='$user_name' ";

$result = $conn->query($sql);



//注册逻辑
if ( empty($user_name) || empty($user_password1) || empty($user_password2) ) {

	jump('./register.php', '用户名和密码不能为空请重新注册');

}else if ( strlen($user_name) <3 || strlen($user_name>10) ) {

	jump('./register.php', '用户名在3到10位之间请您重新注册');

}else if ( $user_password1 !== $user_password2 ) {

	jump('./register.php', '两次密码输入的不一致请您重新注册');

}else if ( strlen($user_password1) <6  ) {

	jump('./register.php', '密码不符合安全策略，请输入6位以上 重新注册!');
	
}else if ( $result->num_rows >0  ) {

	jump('./register.php', '您输入的用户名已经存在请您重新注册');

}else {
	//加密写入数据库
	$user_password = md5($user_password1);
	$sql = "insert into user values (null,'$user_name','$user_password',default)";
	$result = $conn->query($sql);

	if ( $result ) {

		$conn->close();
		jump('./login.php', '注册成功,即将跳转到登录页面');

	} else {

		jump('./register.php', '未知错误,注册失败');

	}
}





















