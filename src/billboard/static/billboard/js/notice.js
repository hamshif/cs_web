
function Notice(callback, followup_callback)
{
	this.base = BaseMap;
	this.base(callback, followup_callback, true);
	this.map_url = "/billboard/notice_map/";
	this.submit_url = "/billboard/notice/";
	this.followup_url = "/billboard/notice_followup/";
	this.interval = 5000;
	this.tries = 10;
}

Notice.prototype = new BaseMap(this.callback, this.followup_callback);


Notice.prototype.base_log = function()
{
	//console.log("callback: ", this.callback, " map: ", this.map);


};