<?php
session_start();

include '../init.php';


if( isset($_SESSION['USER']) ) {
	//删除指定session
	unset($_SESSION['USER']);
	//销毁session
	//session_destroy();

	//判断客户端cookie信息
	if (isset($_COOKIE['user']) ) {
	   setcookie('user','',time()+3600,'localhost','localhost');
	   	//根据传过来的值判断跳转
	   if(
	    $_GET['page'] == 'index' ) {
	   	  jump('../index.php', '注销成功');}
    }else {
       jump('../index.php', '未登录，请先登录 !');
  }
}else {
	jump('../index.php', '未登录，请先登录 !');
}
