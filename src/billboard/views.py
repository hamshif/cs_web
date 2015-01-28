import os, sys, traceback, json,logging

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



logger = logging.getLogger(__name__)






@never_cache
def CMS(request):

    return respond_html(request, "/billboard/templates/billboard/CMS.html")



@never_cache
def edit_notice(request):

    """
    """
    logger.debug("this is a debug message!")


    r = {}

    if request.method == 'POST':

        p = request.POST

        # logger.debug('request')
        # logger.debug(request)

        if not request.is_ajax():

            logger.debug("request isn't ajax")

            r['special message'] = "request isn't ajax"

        try:

            j = (p.__getitem__('j'))
            logger.debug('j: ' + j)

            j = json.loads(j)

            create = j['create']

            if not create:

                r['client_index'] = j['client_index']

                notice_id = j['id']
                logger.debug('notice_id: ' + str(notice_id))

                notice = Notice_Model.objects.get(pk = notice_id)

                r['message'] = "created"

                _delete = j['_delete']
                logger.debug('_delete: ' + str(_delete))


                if _delete:

                    notice.delete()

                    # TODO delete old notice file from disk

                    r['message'] = "deleted"

                    r['id'] = notice_id

                    return HttpResponse(json.dumps(r))


                else:

                    i_creator = j['creator']
                    logger.debug('creator: ' + i_creator)

                    i_text = j['text']
                    logger.debug('text: ' + i_text)

                    notice.creator = i_creator
                    notice.text = i_text

                    r['message'] = "edited"

            else:

                i_creator = j['creator']
                logger.debug('creator: '+ i_creator)

                i_text = j['text']
                logger.debug('text: ' + i_text)

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

                logger.debug('up_file.name: ' + up_file.name)

                # logger.debug('data type:', type(up_file))

                # logger.debug('data.read() type: ', type(up_file.read()))

                path_ = os.path.join(settings.NOTICE_FILES_DIR, notice.creator)

                if validatePath(path_):

                    db_file_path = os.path.join(notice.creator, str(notice.pk) + '_' + up_file.name)


                    if save_uploaded_file(up_file, os.path.join(path_, str(notice.pk) + '_' + up_file.name)):

                        img_stored = True
                        logger.debug('file saved')

                        # TODO delete old notice file from disk

                        notice.file_path = db_file_path

                    else:

                        logger.debug("couldn't save uploaded file")


            notice.save()

            r['notice'] = notice.as_dict()

        except Exception:

            traceback.print_exc()
            print('exception: ' , sys.exc_info)

            r['message'] = sys.exc_info

    else:

        r['message'] = "request method isn't POST"



    return HttpResponse(json.dumps(r))



def edit_notice_followup(request):
    """
    """
    logger.debug('')
    try:

        if request.is_ajax():
            if request.method == 'POST':

                j = json.loads(request.body.decode("utf-8"))

                logger.debug('j: ' + j)


        j['message'] = 'followup'
        logger.debug("j['counter']:" + j['counter'])


    except Exception:
        print(sys.exc_info())





    logger.debug("type(j): " + type(j))

    r = j
    # r['counter'] = counter

    try:

        r['random_stam'] = randint(0,9)

    except Exception:
        print('exception: ' , sys.exc_info)
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

    logger.debug('pssss')


    r = {}

    try:

        r['text'] = randint(0,9)

    except Exception:
        print('exception: ' , sys.exc_info)
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
    # logger.debug('notice_followup')
    try:

        if request.is_ajax():
            if request.method == 'POST':

                j = json.loads(request.body.decode("utf-8"))

                # logger.debug('j: ' + j)


        j['message'] = 'followup'
        # logger.debug("j['counter']:" + j['counter'])

        j['text'] = randint(0,9)


    except Exception:

        print(sys.exc_info())
        traceback.print_exc()


    try:

        notices = Notice_Model.objects.all().order_by('time_stamp')[:10]


        random_index = randint(0,len(notices)-1)

        d_notices = []

        d_notices.append(notices[random_index].as_dict())

        # logger.debug(d_notices)

        # for notice in notices:
        #
        #    d_notices.append(notice.as_dict())

        j['notices'] = d_notices


    except Exception:

        print(sys.exc_info())
        traceback.print_exc()


    # logger.debug("type(j): " + type(j))
    # logger.debug("j: " + j)

    return HttpResponse(json.dumps(j))


@never_cache
def get_image(request):
    """
    """
    logger.debug('')
#     logger.debug('reached getImage')
#     logger.debug('')

    try:
        g = request.GET

        relative_path = g.__getitem__('image_full_path')
    #     logger.debug('relative_path:' + relative_path)
        full_path = os.path.join(settings.NOTICE_FILES_DIR, relative_path)
    #     logger.debug('full_path: ' + full_path)


        image_data = open(full_path, "rb").read()

    except Exception:
        print('exception: ' , sys.exc_info)
        traceback.print_exc()

        logger.debug('because of error returning default image')

        try:
            path = os.path.join(settings.STATIC_ROOT, 'billboard/img/bugs.jpeg')

#             logger.debug('returning empty')

            image_data = open(path, "rb").read()
            return HttpResponse(image_data, content_type="image/jpeg")

        except Exception:
            print('exception: ' , sys.exc_info)
            traceback.print_exc()

    return HttpResponse(image_data, content_type="image/jpeg")