
function EditNotice(callback, followup_callback)
{
	this.base = BaseMap;
	this.base(callback, followup_callback);
	this.map_url = "/billboard/notice_map/";
	this.submit_url = "/billboard/edit_notice/";
	this.followup_url = "/billboard/edit_notice_followup/";
	this.interval = 1000;
	this.tries = 1;

    this.focused_notice_index = undefined;
}

EditNotice.prototype = new BaseMap(this.callback, this.followup_callback);


EditNotice.prototype.base_log = function()
{
	//console.log("callback: ", this.callback, " map: ", this.map);


};

EditNotice.prototype.populateNotices = function ()
{
    var edit_notice = this;

    console.log(this.map);

    $tx_creator.val('');
    $ta_notice_text.val('');

    $select_creator.empty();
    $select_notices.empty();

    for(i=0; i < this.map['notices'].length; i++)
    {
        $select_creator.append($('<option>',{
            text: this.map['notices'][i]['creator'],
            value: this.map['notices'][i]['id']
        }));

        $select_creator.multiSelect('refresh');


        $select_notices.append($('<option>',{
            text: this.map['notices'][i]['creator'],
            value: i,
            click: function()
            {
                console.log(this.value);
                $tx_creator.val(edit_notice.map['notices'][this.value]['creator']);
                $ta_notice_text.val(edit_notice.map['notices'][this.value]['text']);

                var img_path = edit_notice.map['notices'][this.value]['file_path'];
                var request = ''.concat('/billboard/get_image/?image_full_path=', img_path, "&random=" + Math.random());
		        $img_notice.attr('src', request);


                edit_notice.focused_notice_index = this.value;
            }
        }));
    }
}

EditNotice.prototype.editCallback = function ()
{
    console.log('farook');

    console.log(JSON.stringify(json));

    if(json['message'] == 'deleted')
    {
        this.map['notices'].splice(json['client_index'], 1);
        this.focused_notice_index = undefined;

        console.log(this);

        this.populateNotices();


    }
}

EditNotice.prototype.registerCallback = function (notice)
{
    console.log('fooshak');
    this.counter = this.getFollowupTries() + 1;

    this.map['notices'].push(notice);

    this.populateNotices();

    return true;
}