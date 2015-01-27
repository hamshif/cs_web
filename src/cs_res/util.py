
import os, sys, traceback

from django.http import HttpResponse
from django.core.context_processors import csrf

from cs_web import settings





def get_or_create_csrf_token(request):

    token = request.META.get('CSRF_COOKIE', None)

    if token is None:

        token = csrf._get_new_csrf_key()
        request.META['CSRF_COOKIE'] = token

    request.META['CSRF_COOKIE_USED'] = True

    return token



def respond_html(request, html_path):

    print('goolash & beer')

    try:

        print(os.path.dirname(os.path.realpath(__file__)))
        print(settings.BASE_DIR)
        html = open(settings.BASE_DIR + html_path).read()



        print("csrf(request): ", csrf(request))

        response = HttpResponse(html)

#         response.set_cookie('stam_cookie', 'nechratz', expires=2) #, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

        print('response: ')
        # print(response._h)


        csrf_cookie = get_or_create_csrf_token(request)

        print("csrf_cookie: ", csrf_cookie)


    except Exception:
        print('exception: ', sys.exc_info)
        traceback.print_exc()

    return response


def save_uploaded_file(file, full_file_name):

    try:

        with open(full_file_name, 'wb+') as destination:

            for chunk in file.chunks():

                destination.write(chunk)

        return True

    except Exception:

        print('exception: ', sys.exc_info)
        traceback.print_exc()

        return False



def validatePath(path_):

    try:

        if not os.path.exists(path_):

            split_path = path_.split('/')

            tmpath = ''

            for s in split_path:

                tmpath = '/'.join([tmpath, s])

                print('tmpath: ', tmpath)

                if not os.path.exists(tmpath):

                    os.mkdir(tmpath)

        else:

            for root, dirs, files in os.walk(path_):
                print('')
                print("Current directory: " + root)
#                 print("Sub directories: " + str(dirs))
#                 print("Files: " + str(files))
            #this is to save versions of images
#                 for f in files:
#
#                     semantic = str(f)[0:-5].split('_')
#
#                     s_plate_num = int(semantic[1])
#                     s_version = int(semantic[3])

    except Exception:

        print(sys.exc_info())
        print('just printed exception')

        return False

    return True