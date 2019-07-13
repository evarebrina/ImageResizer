from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from . import forms
from . import models
import uuid
import requests
import json


def resize(request):
    if request.method == 'POST':
        form = forms.ResizeForm(request.POST, request.FILES)
        if form.is_valid():
            # save original_image
            image_id = str(uuid.uuid4())
            image_name = 'uploaded_' + image_id + '.jpg'
            image_path = 'static/uploaded_images/' + image_name
            f = open(image_path, 'wb+')
            for chunk in request.FILES['image'].chunks():
                f.write(chunk)
            f.close()
            model = models.UploadedImages(image=image_name)
            model.save()
            response = requests.get('http://' + request.get_host() + '/api/resize/?image_url=' + 'http://' +
                                    request.get_host() + "/" + image_path + '&width=' +
                                    str(form.cleaned_data['width']) + '&height=' + str(form.cleaned_data['height']))
            resp = json.loads(response.content)
            if resp['status'] == 'ok':
                return HttpResponseRedirect('/details/' + resp['details'] + '/')
            else:
                return HttpResponse('something went wrong...')
        else:
            # TODO case of error
            form = forms.ResizeForm()
            return render(request, 'resize.html', {
                'form': form,
            })
    else:
        form = forms.ResizeForm()
        return render(request, 'resize.html', {
            'form': form,
        })


def details(request, task_id):

    response = requests.get(
        'http://' + request.get_host() + '/api/details/' + task_id)
    resp = json.loads(response.content)
    if resp['status'] == 'successful':
        print(resp['url'])
        return render(request, 'details.html', {
            'status': resp['status'],
            'is_successful': True,
            'image_name': resp['url'],
        })
    if resp['status'] == 'failed':
        return render(request, 'details.html', {
            'status': resp['status'],
            'is_successful': False,
            'is_ready': True,
            'error_code': resp['error_code'],
            'message': resp['message'],
        })
    if resp['status'] == 'error':
        return render(request, 'details.html', {
            'status': resp['status'],
            'is_successful': False,
            'error_code': resp['error_code'],
            'message': resp['message'],
        })
    if resp['status'] == 'pending':
        return render(request, 'details.html', {
            'status': resp['status'],
            'is_successful': False,
            'is_ready': False,
        })
    else:
        return HttpResponse('Details ' + task_id + ' Status: ' + resp['status'])
