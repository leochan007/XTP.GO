$(document).ready(function() {
// 使用 jQuery异步提交表单
$('#login_form').submit(function() {
	console.log("aaa");
	jQuery.ajax({
		url:'/user/login',
		data:$('#login_form').serialize(),
		type:"POST",
		beforeSend:function()
		{
			$('#login_btn').attr("disabled","true");
			//$('#editRealMsgImg').show();
		},
		success:function(data)
		{
			console.log("success!" + JSON.stringify(data));
			console.log("success!" + data.ErrorCode);
			if (data.ErrorCode == 0) {
				$('#login_btn').attr("disabled","false");
				location.href="/main";
			}
		},
		failure:function(data)
		{
			console.log("failure!" + data);
		}
	});
	return false;
});

});
