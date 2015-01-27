import os, sys, traceback, json

from datetime import datetime


from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.middleware import csrf
from django.views.decorators.csrf import csrf_protect
from random import randint

from billboard.models import Notice_Model

from cs_res.util import respond_html, save_uploaded_file, validatePath

from cs_web import settings


@never_cache
def CMS(request):

    return respond_html(request, "/billboard/templates/billboard/CMS.html")



@never_cache
def set_notice(request):

    """
    Create edit or delete a notice including fields and files.

    """

    r = {}

    if request.method == 'POST':

        p = request.POST

        # print('request')
        # print(request)

        if not request.is_ajax():

            print("request isn't ajax")

            r['special message'] = "request isn't ajax"

        try:

            create = (p.__getitem__('create'))
            print('create: ', create)

            if create == 'false':

                r['client_index'] = int(p.__getitem__('client_index'))

                notice_id = int(p.__getitem__('id'))
                print('notice_id: ', str(notice_id))

                notice = Notice_Model.objects.get(pk = notice_id)

                r['message'] = "created"

                _delete = (p.__getitem__('_delete'))
                print('_delete: ', _delete)


                if _delete == 'true':

                    notice.delete()

                    # TODO delete old notice file from disk

                    r['message'] = "deleted"

                    r['id'] = notice_id

                    return HttpResponse(json.dumps(r))


                else:

                    i_creator = p.__getitem__('creator')
                    print('creator: ', i_creator)

                    i_text = p.__getitem__('text')
                    print('text: ', i_text)

                    notice.creator = i_creator
                    notice.text = i_text

                    r['message'] = "edited"

            else:

                i_creator = p.__getitem__('creator')
                print('creator: ', i_creator)

                i_text = p.__getitem__('text')
                print('text: ', i_text)

                notice = Notice_Model.objects.create(
                    creator = i_creator,
                    text = i_text,
                    time_stamp = datetime.now(),
                )

                r['message'] = "created"



            print('request.FILES: ', request.FILES)

            files = request.FILES.items()

            is_empty = True

            for key1, valu1 in request.FILES.items():

                print ("key1: ", key1 , "    valu1: ", valu1)

                is_empty = False


            if not is_empty:

                up_file = request.FILES['input_file']

                print('up_file.name: ', up_file.name)

                # print('data type:', type(up_file))

                # print('data.read() type: ', type(up_file.read()))

                path_ = os.path.join(settings.NOTICE_FILES_DIR, notice.creator)

                if validatePath(path_):

                    db_file_path = os.path.join(notice.creator, str(notice.pk) + '_' + up_file.name)


                    if save_uploaded_file(up_file, os.path.join(path_, str(notice.pk) + '_' + up_file.name)):

                        img_stored = True
                        print('file saved')

                        # TODO delete old notice file from disk

                        notice.file_path = db_file_path

                    else:

                        print("couldn't save uploaded file")


            notice.save()

            r['notice'] = notice.as_dict()

        except Exception:
            print('exception: ', sys.exc_info)
            traceback.print_exc()

            r['message'] = sys.exc_info

    else:

        r['message'] = "request method isn't POST"



    return HttpResponse(json.dumps(r))





@never_cache
def edit_notice(request):

    """
    """

    if request.method == 'POST':


        # for key in request.FILES.keys():
        #     print('key: ' + key)
        #     print('file_name: ' + str(request.FILES[key]))

        p = request.POST

        print('request')
        print(request)

        try:

            # this is a questionable check to see if json was sent it works but smacks of a hack treat with care!
            if request.is_ajax():

                # print('request')
                # print(request)


                # print('request.body')
                # print(request.body)

                j = json.loads(request.body.decode("utf-8"))

                print('j: ', j)

                notice_id = j['id']

                notice = Notice_Model.objects.get(pk = notice_id)

                # print(notice.__str__())

                r = {'id': notice.pk}

                if j['delete'] == True:

                    r['message'] = 'deleted'
                    r['client_index'] = j['client_index']

                    notice.delete()

                else:

                    notice.creator = j['creator']
                    notice.text = j['text']

                    notice.save()

                    r['new_value'] = notice.as_dict()
                    r['client_index'] = j['client_index']

                    r['message'] = 'edited'

                return HttpResponse(json.dumps(r))

            else:

                print("request isn't ajax")

        except Exception:
            print('exception: ', sys.exc_info)
            traceback.print_exc()
            r = {}
            r['message'] = 'error'
            r['error'] = sys.exc_info

            return HttpResponse(json.dumps(r))

        try:

            counter = int(p.__getitem__('counter'))
            print('counter: ', str(counter))

            i_creator = p.__getitem__('creator')
            print('creator: ', i_creator)

            i_text = p.__getitem__('text')
            print('text: ', i_text)

            i_new = p.__getitem__('new')
            print('new: ', i_new)



            print('request.FILES: ', request.FILES)

            files = request.FILES.items()


            is_empty = True

            for key1, valu1 in request.FILES.items():

                print ("key1: ", key1 , "    valu1: ", valu1)

                is_empty = False

            notice = Notice_Model.objects.create(
                creator = i_creator,
                text = i_text,
                time_stamp = datetime.now(),
            )


            if not is_empty:

                up_file = request.FILES['input_file']

                print(up_file.name)
                # print('data type:', type(up_file))

                # print('data.read() type: ', type(up_file.read()))

                path_ = os.path.join(settings.NOTICE_FILES_DIR, notice.creator)

                if validatePath(path_):

                    db_file_path = os.path.join(notice.creator, str(notice.pk) + '_' + up_file.name)


                    if save_uploaded_file(up_file, os.path.join(path_, str(notice.pk) + '_' + up_file.name)):

                        img_stored = True
                        print('file saved')

                        notice.file_path = db_file_path

                        notice.save()


                    else:

                        print("couldn't save uploaded image")


            r = {}
            r['notice'] = notice.as_dict()


        except Exception:
            print('exception: ', sys.exc_info)
            traceback.print_exc()


    print('edit_notice')

    if not r:

        r = {}

    r['counter'] = counter


    try:

        r['text'] = randint(0,9)

    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()


    return HttpResponse(json.dumps(r))


def edit_notice_followup(request):
    """
    """
    print('edit_notice_followup')
    try:

        if request.is_ajax():
            if request.method == 'POST':

                j = json.loads(request.body.decode("utf-8"))

                print('j: ', j)


        j['message'] = 'followup'
        print("j['counter']:", j['counter'])


    except Exception:
        print(sys.exc_info())





    print("type(j): ", type(j))

    r = j
    # r['counter'] = counter

    try:

        r['random_stam'] = randint(0,9)

    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()




    return HttpResponse(json.dumps(r))



@never_cache
def billboard(request):

    return respond_html(request, "/billboard/templates/billboard/billboard.html")


@never_cache
def notice_map(request):


    r = {'crunch': 'flablab'}

    try:

        notices = Notice_Model.objects.all().order_by('time_stamp')


        random_index = randint(0,len(notices)-1)

        d_notices = []

        for notice in notices:

           d_notices.append(notice.as_dict())

        r['notices'] = d_notices


    except Exception:

        print(sys.exc_info())
        traceback.print_exc()


    return HttpResponse(json.dumps(r))









@never_cache
def notice(request):

    print('pssss')


    r = {}

    try:

        r['text'] = randint(0,9)

    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()


    try:

        notices = Notice_Model.objects.filter().order_by('time_stamp')[:10]

        d_notices = []

        for notice in notices:

           d_notices.append(notice.__str__())

        r['notices'] = d_notices


    except Exception:
        print(sys.exc_info())



    return HttpResponse(json.dumps(r))


@never_cache
def notice_followup(request):

    """
    """
    # print('notice_followup')
    try:

        if request.is_ajax():
            if request.method == 'POST':

                j = json.loads(request.body.decode("utf-8"))

                # print('j: ', j)


        j['message'] = 'followup'
        # print("j['counter']:", j['counter'])

        j['text'] = randint(0,9)


    except Exception:

        print(sys.exc_info())
        traceback.print_exc()


    try:

        notices = Notice_Model.objects.all().order_by('time_stamp')[:10]


        random_index = randint(0,len(notices)-1)

        d_notices = []

        d_notices.append(notices[random_index].as_dict())

        # print(d_notices)

        # for notice in notices:
        #
        #    d_notices.append(notice.as_dict())

        j['notices'] = d_notices


    except Exception:

        print(sys.exc_info())
        traceback.print_exc()


    # print("type(j): ", type(j))
    # print("j: ", j)

    return HttpResponse(json.dumps(j))


@never_cache
def get_image(request):
    """
    """
#     print('')
#     print('reached getImage')
#     print('')

    g = request.GET

    relative_path = g.__getitem__('image_full_path')
#     print('relative_path:', relative_path)
    full_path = os.path.join(settings.NOTICE_FILES_DIR, relative_path)
#     print('full_path: ', full_path)

    try:
        image_data = open(full_path, "rb").read()

    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()

        print('because of error returning default image')

        try:
            path = os.path.join(settings.STATIC_ROOT, 'billboard/img/bugs.jpeg')

#             print('returning empty')

            image_data = open(path, "rb").read()
            return HttpResponse(image_data, content_type="image/jpeg")

        except Exception:
            print('exception: ', sys.exc_info)
            traceback.print_exc()

    return HttpResponse(image_data, content_type="image/jpeg")