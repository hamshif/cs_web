

var csrftoken;

$(document).ready(function()
{
	csrftoken = getCookie('csrftoken');
//	console.log("csrftoken: ", csrftoken);


    $div_notice_form = $('<div>',
        {
            id:"div_notice_form"
        }
    );

    $('body').append($div_notice_form);

//    var too = new Notice_CMS_GUI()
//
//    too.createGUI($div_notice_form, {});


	var starter = new Starter();
	starter.start($div_notice_form, Notice_CMS_GUI, EditNotice);






});




