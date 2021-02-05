<?php 
session_start(); 
date_default_timezone_set('PRC');
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-cn">
<head>
	<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
	<title>BBS首页</title>
	<meta name="keywords" content="关键字列表" />
	<meta name="description" content="网页描述" />
     <!-- 用PHP常量定义 引入样式文件 -->
	<link rel="stylesheet" type="text/css" href="<?php echo DIR_PUBLIC;?>/css/public.css" />
	<link rel="stylesheet" type="text/css" href="<?php echo DIR_PUBLIC;?>/css/index.css" />
	<style type="text/css"></style>
	<script type="text/javascript"></script>
</head>
<body>
	<div class="header_wrap">
		<div id="header" class="auto">
			<div class="logo">重工论坛<span style="font-size: 10px"> by PHP</span></div>
			<div class="nav"> 
				<a class="hover" href="#">首页</a>
				<a class="hover" href="./model/list_hot.php">热帖</a>
				<a class="hover" href="./model/list.php">看帖</a>
				<a class="hover" href="./model/publish.php">发帖</a>
			</div>
			<div class="serarch">
				<form>
					<input class="keyword" type="text" name="keyword" placeholder="输入搜索内容" />
					<input class="submit" type="submit" name="submit" value="" />
				</form>
			</div>
			<div class="login" style="width: 300px;">
			<!-- 	用户信息登录判断 -->
				  <?php  
				  	if(isset($_SESSION['USER'])) {
				  	$arr = $_SESSION['USER'];
				  		echo  '<a href="./model/userinfo.php">&nbsp;用户' . ' ' .$arr["user_name"]. '</a>' . '&nbsp;<img style="width:32px;height: 32px" src="./uploads/images/default.jpg"/>' . ' ' .' ' . '<a href="./model/logout.php?page=index">注销</a>';
				  }else {
				  	    echo '<a href="./model/login.php">&nbsp;' . '登录' . '</a>' . ' ' . '<a href="./model/register.php">注册</a>&nbsp;';
				} 
				   ?> 
			</div>
		</div>
	</div>