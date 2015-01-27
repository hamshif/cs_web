


var Notice_CMS_GUI = Object.extend(Object,
	{
		createGUI : function (parent_element, baseMap)
		{
            $h_CMS = $('<h2>',
                {
                    id:"h_CMS",
                    text: "Notice Management"
                }
            );

			parent_element.append($h_CMS);

            $dev_qt_0 = $("<dev>",
                {
                    id: "dev_qt_0"
                }
            );

            parent_element.append($dev_qt_0);


            this.createNoticeEdit($dev_qt_0, baseMap);


            this.createNoticeFilter($dev_qt_0);


		},

		populateGUI : function (editNotice) {
//            console.log(editNotice.map.notices);

            focused_notice_index = undefined;

//            console.log(this);


            this.populateNotices();

//            console.log(this.editCallback)
        },


		sendFormData : function(baseMap)
		{
//            console.log('shwaa');


            var formData = new FormData();

            if($tx_creator.val() == '')
            {
                alert('Please choose a creator');
                return;
            }

            if($ta_notice_text.val() == '')
            {
                alert('Please enter notice text');
                return;
            }

            formData.append('creator', $tx_creator.val());
            formData.append('text', $ta_notice_text.val());
            formData.append('new', true);

            var files = $input_file[0].files;

            for (var i = 0; i < files.length; i++)
            {
              var file = files[i];
               console.log('file.name: ', file.name);
              console.log('file.type: ', file.type);
              // Check the file type.
              // if (!file.type.match('image.*')) {
                // continue;
              // }

              // Add the file to the request.
              formData.append('input_file', file, file.name);
            }


//			console.log("formData");
//			console.log(formData.toString());

			baseMap.submitFormData(formData);
		},


        updateGUI : function(json)
		{
            console.log('json');
            console.log(json);
//            console.log("json['notice']: ", json['notice'])
//            notices.append(json['notice'])

            if(json['notice'] !== undefined)
            {
                return this.registerCallback(json['notice']);
            }
		},

        createNoticeEdit : function(parent_element, baseMap)
        {
            $dev_notice_edit = $("<dev>",
                {
                    id: "dev_notice_edit"
                }
            );

                parent_element.append($dev_notice_edit);


                $dev_notice_edit.append($('<p>',
                    {
                        class: "field_header",
                        text: "Creator"
                    }
                ));

                $tx_creator = $('<input>',
                    {
                        id: "tx_creator",
                        type: "text"
                    }
                );

                $dev_notice_edit.append($tx_creator);

                $dev_notice_edit.append('<br>');

                $dev_notice_edit.append($('<p>',
                    {
                        class: "field_header",
                        text: "Notice Text"
                    }
                ));

                $ta_notice_text = $('<textarea>',
                    {
                        id: "ta_notice_text",
                        rows: 4,
                        cols: 50
                    }
                );

                $dev_notice_edit.append($ta_notice_text);
                $dev_notice_edit.append('<br>');


                $img_notice = $('<img>',
                    {
                        id: "img_notice",
                        src : "/static/billboard/img/bugs.jpeg"
                    }
                );

                $dev_notice_edit.append($img_notice);


                $input_file = $('<input>', {
                    id: "input_file",
                    type:"file",
                    name: "input_file"

                });

                $dev_notice_edit.append('<br>');

                $dev_notice_edit.append($input_file);



                $dev_notice_edit.append('<br>');
                $dev_notice_edit.append('<br>');

                var notice_gui = this;

                $b_submit_notice = $('<input>',
                    {
                        type:"button",
                        id: "b_submit_notice",
                        value: "Submit Notice",
                        click: function(){notice_gui.sendFormData(baseMap);}
                    }
                );

                $dev_notice_edit.append($b_submit_notice);

                $b_edit_notice = $('<input>',
                    {
                        type:"button",
                        id: "b_edit_notice",
                        value: "Edit Notice",
                        click: function()
                        {
                            baseMap.map['notices'][baseMap.focused_notice_index]['text'] = $ta_notice_text.val();
                            baseMap.map['notices'][baseMap.focused_notice_index]['creator'] = $tx_creator.val();

                            notice_gui.edit_notice_xhr(baseMap, false);
                        }
                    }
                );



                $dev_notice_edit.append($b_edit_notice);


                $b_delete_notice = $('<input>',
                    {
                        type:"button",
                        id: "b_delete_notice",
                        value: "Delete Notice",
                        click: function()
                        {
                            notice_gui.edit_notice_xhr(baseMap, true);
                        }
                    }
                );

                $dev_notice_edit.append($b_delete_notice);
        },

        createNoticeFilter : function(parent_element)
        {
            $dev_notice_filter = $("<dev>",
                {
                    id: "dev_notice_filter"
                }
            );

            parent_element.append($dev_notice_filter);

                $dev_notice_filter.append($('<p>',
                    {
                        class: "field_header",
                        text: "Available Notices"
                    }
                ));

                $select_notices = $('<select multiple>',
                    {
                        id: "select_notices"
                    }
                );

                $dev_notice_filter.append($select_notices);

                $dev_notice_filter.append($('<p>',
                    {
                        class: "field_header",
                        text: "Notice Filter"
                    }
                ));

                $select_creator = $('<select multiple>',
                    {
                        id: "select_creator"
                    }
                );

                $dev_notice_filter.append($select_creator);
        },


        edit_notice_ajax : function(baseMap, _delete)
        {
            console.log('fakashta');

            if(baseMap.focused_notice_index === undefined)
            {
                alert('Please choose a notice to edit!');
                return;
            }

            console.log(this);

            $.ajax({
                url: baseMap.submit_url,
                type: 'POST',
                contentType: 'application/json; charset=utf-8',
                data: JSON.stringify(
                    {
                        'id': baseMap.map['notices'][baseMap.focused_notice_index]['id'],
                        'text': baseMap.map['notices'][baseMap.focused_notice_index]['text'],
                        'creator': baseMap.map['notices'][baseMap.focused_notice_index]['creator'],
                        'client_index': baseMap.focused_notice_index,
                        'delete': _delete
                    }),
                dataType: 'json',
//                _callback : edit_notice.editCallback,
                context: this,
                beforeSend: function(xhr)
                {
                    console.log('xhr', xhr);
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },

                success: function(json)
                {
                    console.log(json);

                    if(json['message'] == 'deleted')
                    {
                        baseMap.map['notices'].splice(json['client_index'], 1);
                        baseMap.focused_notice_index = undefined;

                        baseMap.populateNotices();
                    }
                    else if(json['message'] == 'edited')
                    {
                        baseMap.map['notices'].splice(json['client_index'], 1, json['new_value']);
                        baseMap.focused_notice_index = json['client_index'];

                        baseMap.populateNotices();
                    }


                }
            });
        },

        edit_notice_xhr : function(baseMap, _delete)
        {
            console.log('Shrubbery');

            if(baseMap.focused_notice_index === undefined)
            {
                alert('Please choose a notice to edit!');
                return;
            }

            console.log(this);

            if($tx_creator.val() == '')
            {
                alert('Please choose a creator');
                return;
            }

            if($ta_notice_text.val() == '')
            {
                alert('Please enter notice text');
                return;
            }

            var formData = new FormData();

            formData.append('create', 'false');
            formData.append('id', baseMap.map['notices'][baseMap.focused_notice_index]['id']);
            formData.append('client_index', baseMap.focused_notice_index);


            if(!_delete)
            {
                formData.append('_delete', 'false');
                formData.append('creator', $tx_creator.val());
                formData.append('text', $ta_notice_text.val());

                var files = $input_file[0].files;

                for (var i = 0; i < files.length; i++)
                {
                  var file = files[i];
                   console.log('file.name: ', file.name);
                  console.log('file.type: ', file.type);
                  // Check the file type.
                  // if (!file.type.match('image.*')) {
                    // continue;
                  // }

                  // Add the file to the request.
                  formData.append('input_file', file, file.name);
                }
            }
            else
            {
                formData.append('_delete', 'true');
            }

//			console.log("formData");
//			console.log(formData.toString());

            var xhr = new XMLHttpRequest();
            xhr.onload = function()
            {
                console.log('this.responseText: ', this.responseText);

                var json = JSON.parse(this.responseText);

                if(json['message'] == 'deleted')
                {
                    baseMap.map['notices'].splice(json['client_index'], 1);
                    baseMap.focused_notice_index = undefined;

                    baseMap.populateNotices();
                }
                else if(json['message'] == 'edited')
                {
                    baseMap.map['notices'].splice(json['client_index'], 1, json['notice']);
                    baseMap.focused_notice_index = json['client_index'];

                    baseMap.populateNotices();
                }
                else if(json['message'] == 'created')
                {
                    baseMap.map['notices'].push(json['notice']);
                    baseMap.focused_notice_index = json['client_index'];

                    baseMap.populateNotices();
                }
            };
            xhr.open('POST', "/billboard/set_notice/", true);
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        //	console.log(xhr);

            xhr.send(formData);
        }
	}
).implement(BaseGUI);
