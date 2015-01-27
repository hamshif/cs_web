
var csrftoken;

$(document).ready(function()
{
	csrftoken = getCookie('csrftoken');
//	console.log("csrftoken: ", csrftoken);


    $div_notice = $('#div_notice');

	var starter = new Starter();
	starter.start($div_notice, Notice_GUI, Notice);

    $b_submit.hide();
    $b_submit.click();
});