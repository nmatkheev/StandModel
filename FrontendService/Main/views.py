import os
import sys

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
# from reportlab.pdfgen import canvas
from .forms import AttributesForm, DocumentForm, ExtractForm

from .models import Document

from django.conf import settings
from django.core.files import File

from django.utils.encoding import smart_text, smart_str, smart_bytes
from django.views.decorators.csrf import csrf_exempt

import logging
import datetime, time

import subprocess
import shutil
import re
import uuid
import requests


from Portal.settings import BACKEND_URL, BASE_DIR


def cabinet(request):
    # return render(request, 'cabinet.html', {'username': request.user.username}, context_instance=RequestContext(request))
    return render(request, 'cabinet.html')


"""----------------------------------------------------------------------------------
    Вьюшки для: личного кабинета
----------------------------------------------------------------------------------"""


def parser(string, separator):
    result = ""
    components = string.split(separator)

    for x in range(0, len(components) - 1):
        if separator == "/":
            result += components[x] + "/"
        else:
            result += components[x]
    return result


def waitfile(processed_file_path):
    """
        Отдаем файл.
        TODO: Нужны присвоить новому файлу атрибуты старого файла
    """
    file_ready = False
    while not file_ready:
        try:
            os.stat(processed_file_path)
            file_ready = True
        except FileNotFoundError:
            pass

    return True


def validate_pdf(incoming):
    task = subprocess.Popen(["qpdf", "--check", incoming], stdout=subprocess.PIPE)
    try:
        task.wait(10)
        outs, errs = task.communicate()
    except subprocess.TimeoutExpired:
        task.kill()

    # if task.returncode > 50 or task.returncode < 0:
    if task.returncode != 2:
        return -1
    else:
        return 0


def handle_upload(f):
    _path = os.path.join(BASE_DIR, 'file_storage', f._name)

    if not os.path.exists(os.path.join(BASE_DIR, 'file_storage')):
        os.mkdir(os.path.join(BASE_DIR, 'file_storage'))

    if os.path.exists(_path):
        _path = _path.replace('.pdf', '') + '_{0}'.format(datetime.datetime.today().strftime("%d%m%Y_%H%M%S")) + '.pdf'

    with open(_path, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    return _path


@csrf_exempt
def submit_stego_object(request):
    logger = logging.getLogger('custom')
    fatalog = logging.getLogger('exceptions')

    if request.method == 'POST':
        uploadform = DocumentForm(request.POST, request.FILES)
        attributeform = AttributesForm(request.POST, request.FILES)

        if uploadform.is_valid() and attributeform.is_valid():
            attrdata = attributeform.cleaned_data

            _uuid = attributeform.data['uuid']
            payload = smart_text(attrdata.get('payload'))
            password = smart_text(attrdata.get('password'))

            income_file = handle_upload(request.FILES['docfile'])

            # validate_code = validate_pdf(income_file)
            # if validate_code != 0:
            #     status = 'Плохой файл'
            #     return render(request, 'submit_stego.html',
            #            {'uploadform': uploadform,
            #             'attributeform': attributeform, 'status': status}, context_instance=RequestContext(request))

            exec_code = -100
            logger.info("SUBMIT,began,uuid,%s,TIME,%d",
                        _uuid, 0)
            try:
                # exec_code = embed_comment(income_file, payload, password)
                r = requests.post(BACKEND_URL+'/submit', data={
                    'uuid': _uuid,
                    'file': request.FILES['docfile'],
                    'payload': payload,
                    'password': password,
                })
            except Exception as e:
                fatalog.exception(e, exc_info=True)
                status = 'Что-то пошло не так. Но мы уже об этом знаем'
                logger.info("SUBMIT,failed,uuid,%s,TIME,%d",
                            _uuid, 0)
                return render(request, 'submit_stego.html', {'uploadform': uploadform,
                                                             'attributeform': attributeform, 'status': status}
                              )
            else:
                logger.info("SUBMIT,ended,uuid,%s,TIME,%d",
                            _uuid, r.elapsed.seconds)
                filename = os.path.split(income_file)[1]
                django_file = File(open(income_file, "rb"))
                response = HttpResponse(django_file, content_type='application/pdf')
                response['Content-Disposition'] = smart_bytes('attachment; filename*=''{0}'.format(filename))
                return response

        else:  # Если форма не валидна:
            upload_error = uploadform.errors
            other_errors = attributeform.errors
            return render(request, 'submit_stego.html',
                          {'uploaderr': upload_error, 'othererr': other_errors, 'uploadform': uploadform,
                           'attributeform': attributeform})  # , context=RequestContext(request))

    uploadform = DocumentForm()
    attributeform = AttributesForm()

    return render(request, 'submit_stego.html', {'uploadform': uploadform, 'attributeform': attributeform})


@csrf_exempt
def extract_stego_object(request):
    logger = logging.getLogger('custom')
    fatalog = logging.getLogger('exceptions')

    if request.method == 'POST':
        uploadform = DocumentForm(request.POST, request.FILES)
        extractform = ExtractForm(request.POST, request.FILES)

        if uploadform.is_valid() and extractform.is_valid():
            attrdata = extractform.cleaned_data
            password = smart_text(attrdata.get('password'))
            income_file = handle_upload(request.FILES['docfile'])
            _uuid = extractform.data['uuid']

            extracted = 'Extracted content of file...'
            logger.info("EXTRACT,began,uuid,%s,TIME,%d",
                        _uuid, 0)
            try:
                r = requests.post(BACKEND_URL + '/extract', data={
                    'uuid': _uuid,
                    'file': request.FILES['docfile'],
                    'password': password,
                })
            except Exception as e:
                fatalog.exception(e, exc_info=True)
                status = 'Что-то пошло не так. Но мы уже об этом знаем'
                logger.info("EXTRACT,failed,uuid,%s,TIME,%d",
                            _uuid, 0)
                return render(request, 'extract_stego.html',
                              {'status': status, 'uploadform': uploadform,
                               'extractform': extractform})
            else:
                logger.info("EXTRACT,ended,uuid,%s,TIME,%d",
                            _uuid, r.elapsed.seconds)
                _path = os.path.split(income_file)[0]
                filename = os.path.split(income_file)[1].replace('.pdf', '')

                file = os.path.join(_path, filename + '.message.txt')
                pushfile = filename + '.message.txt'

                with open(file, 'w') as f:
                    f.write(extracted)

                django_file = File(open(file, "rb"))
                processed_response = HttpResponse(django_file, content_type='text/plain')
                processed_response['Content-Disposition'] = smart_bytes('attachment; filename*=''{0}'.format(pushfile))

                return processed_response

        else:
            upload_error = uploadform.errors
            other_errors = extractform.errors
            return render(request, 'extract_stego.html',
                          {'uploaderr': upload_error, 'othererr': other_errors, 'uploadform': uploadform,
                           'extractform': extractform})  # , context=RequestContext(request))

    uploadform = DocumentForm()
    extractform = ExtractForm()

    return render(request, 'extract_stego.html', {'uploadform': uploadform, 'extractform': extractform})
