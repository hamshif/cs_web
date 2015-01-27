
function BaseMap(callback, followup_callback, endless)
{
	this.callback = callback;

    if(endless=== undefined)
    {
        this.endless = false;
    }

    this.endless = endless;

	this.map;
	this.map_url;
	this.submit_url;
	this.followup_url;
    this.followup_callback = followup_callback;
	this.interval;
	this.tries;
}

BaseMap.prototype.getMapURL = function()
{
	if(this.map_url == undefined)
	{
		throw new Error('The inheriting class must define this.map_url!!!');
	}
	else
	{
		return this.map_url;
	}
};


BaseMap.prototype.getSubmitURL = function()
{
	if(this.submit_url == undefined)
	{
		throw new Error('The inheriting class must define this.map_url!!!');
	}
	else
	{
		return this.submit_url;
	}
};


BaseMap.prototype.getFollowupUrl = function()
{
	if(this.followup_url == undefined)
	{
		throw new Error('The inheriting class must define followup_url!!!');
	}
	else
	{
		return this.followup_url;
	}
};


BaseMap.prototype.getFollowupInterval = function()
{
	if(this.interval == undefined)
	{
		throw new Error('The inheriting class must define followup_delay!!!');
	}
	else
	{
		return this.interval;
	}
};

BaseMap.prototype.getFollowupTries = function()
{
	if(this.tries == undefined)
	{
		throw new Error('The inheriting class must define followup_tries!!!');
	}
	else
	{
		return this.tries;
	}
};



BaseMap.prototype.getMap = function(json_query)
{
	//console.log('this.getMapURL(): ', this.getMapURL());
	if(json_query === undefined)
	{
		json_query = {'default_query':'why does a chicken?'};
	}
	
	var baseMap = this;
	
	$.ajax({
	    url: this.getMapURL(),
	    type: 'POST',
	    contentType: 'application/json; charset=utf-8',
	    data: JSON.stringify(json_query),
	    dataType: 'json',
	    
	    beforeSend: function(xhr) {
			//console.log('xhr', xhr);
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		},
	    success: function(json) 
		{
			  //console.log('response rom ', url, ':');
			  //console.log(JSON.stringify(json));	 
			  baseMap.map = json;
			  baseMap.callback(baseMap);
		}
	});	
};


BaseMap.prototype.submitFormData = function (formData)
{
	//console.log('formData');
	//console.log(formData);
	
	//console.log(this.getSubmitURL());
	formData.append('counter', 0);

	var baseMap = this;
	
	var xhr = new XMLHttpRequest();
	xhr.onload = function()
    {
        var j = JSON.parse(this.responseText);

        console.log('this.responseText:', j);

//
//			j['counter'] = 0;


        var stop = baseMap.followup_callback(j);


        if(stop !== undefined && stop)
        {
            return;
        }

        baseMap.followup(j);
    };
	xhr.open('POST', this.getSubmitURL(), true);
	xhr.setRequestHeader("X-CSRFToken", csrftoken);
//	console.log(xhr);
	
	xhr.send(formData);
};


BaseMap.prototype.followup = function(j)
{	
//	console.log('JSON.stringify(j): ', JSON.stringify(j));
	var message = j['message'];
//	console.log("message: ", message);

//    console.log('data:');
//    console.log(j)
	//console.log('getFollowupUrl(): ', this.getFollowupUrl());

	var baseMap = this;
	
	$.ajax({
	    url: this.getFollowupUrl(),
	    type: 'POST',
	    contentType: 'application/json; charset=utf-8',
	    data: JSON.stringify(j),
	    dataType: 'json',
	    
	    beforeSend: function(xhr) 
	    {
//			console.log('xhr', xhr);

//            console.log('baseMap.tries: ', baseMap.tries)

			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		},
	    success: function(json) 
		{
//		  	console.log(JSON.stringify(json));

            if(baseMap.recovered1 == false)
            {
                location.reload();
            }

            baseMap.recovered1 = true;


            baseMap.dafault_query = json;

//            console.log('baseMap.endless: ', baseMap.endless);

            if(baseMap.endless === true)
            {
                baseMap.followup_delay(json);
            }
            else
            {
                var counter = json['counter'];

                console.log('counter: ', counter);

                if(counter === undefined)
                {
                    return;
                }

                if( counter > baseMap.getFollowupTries())
                {
                    console.log('to many followups');
                }
                else
                {
                    json['counter'] = counter + 1;
                    baseMap.followup_delay(json);
                }
            }
//            console.log('    Charlie: ', baseMap);


            baseMap.followup_callback(json);
		},
        error: function (request, status, error)
        {
            baseMap.recovered1 = false;

            console.log(request.responseText);
//            console.log(request);
            console.log(status);
            console.log(error);

            setTimeout
            (
                function(){baseMap.followup(baseMap.dafault_query);},
                50
            );
        }
	});	
};


BaseMap.prototype.followup_delay = function(query)
{
	var baseMap = this;
	
	setTimeout
	(	
		function(){baseMap.followup(query);},
		baseMap.getFollowupInterval()
	);
};


