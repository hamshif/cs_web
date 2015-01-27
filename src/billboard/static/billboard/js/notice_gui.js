
var Notice_GUI = Object.extend(Object,
	{
		createGUI : function (parent_element, baseMap)
		{
//            console.log('floopsh');

            $notice = $('<pre>',
                {
                    id: "notice",
                    text: "Notices"
                }
            );
0

			parent_element.append($notice);

             var notice_gui = this;

			$b_submit = $('<input>',
				{
					type:"button",
					id: "b_start_notices",
					value: "start notices",
					click: function(){notice_gui.sendFormData(baseMap);}
				}
			);

            parent_element.append($b_submit);


            $img_notice = $('<img>',
                {
                    id: "img_notice",
                    src : "/static/billboard/img/bugs.jpeg"

                }
            );

//            parent_element.append($img_notice);

            $('body').append($img_notice);
		},

		populateGUI : function (notice)
		{
			//console.log('JSON.stringify(notice.map): ');
			//console.log(JSON.stringify(notice.map));

			//console.log(notice);

			//console.log(Object.keys(notice.map));

			var d = Object.keys(notice.map);

//            console.log(d);

			for (var i=0; i<d.length; i++)
			{
//				console.log(notice.map[d[i]]);
			}
		},

		sendFormData : function(baseMap)
		{
//            console.log('shwaa');


            var formData = new FormData();

            formData.append('stam', 'kishkoosh');

//			console.log("formData");
//			console.log(formData);

			baseMap.submitFormData(formData);
		},


        updateGUI : function(json)
		{
            console.log('json');
            console.log(json);
            $notice.empty();

            var text = json.text + '\n';
            var img_path = ""

            for(notice in json['notices'])
            {
                text += '\n' + json['notices'][notice]['text'];

                img_path = json['notices'][notice]['file_path']
            }

            console.log('img_path: ', img_path)

            $notice.text(text);

            if(img_path != null)
            {
                putImageIn(img_path, $img_notice);
            }

		}

	}
).implement(BaseGUI);




function putImageIn(img_path, recepticle)
{
	if(img_path.indexOf('/static') === 0)
	{
		recepticle.attr('src', img_path);
	}
	else
	{
		var request = ''.concat('/billboard/get_image/?image_full_path=', img_path, "&random=" + Math.random());
		recepticle.attr('src', request);
	}

	//console.log('put: ', img_path, ' in: ', recepticle.attr('id'));
}