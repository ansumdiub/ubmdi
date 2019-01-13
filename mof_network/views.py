from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView)
from .forms import PostForm, CommentForm, MofForm
from .models import *
import json
import base64
import logging
logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'mof_network/index.html'


class AboutView(TemplateView):
    template_name = 'mof_network/about.html'


class MapView(TemplateView):
    context_object_name = 'mofs'
    model = Mof
    template_name = 'mof_network/map_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Node'] = Mof.objects \
            .raw('SELECT name, fingerprint FROM mof_network_mof WHERE name="OWITAQ"')[0]
        print(context)
        return context


@csrf_exempt
def ajax_render(request):
    model = Mof
    name = str(request.POST.get('mof_name'))
    mof = Mof.objects.all().filter(name__exact=name).get()
    print(mof.fingerprint)
    with open(mof.fingerprint.path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read())
    response = HttpResponse(encoded_string, content_type='image/png')
    return response


class MofListView(ListView):
    context_object_name = 'mofs'
    model = Mof
    paginate_by = 10

    def get_queryset(self):
        return Mof.objects.order_by('name')


class MofDetailView(DetailView):
    context_object_name = 'mof_detail'
    model = Mof
    template_name = 'mof_network/mof_detail.html'


# create, read, update, and delete (CRUD)
class MofCreateView(CreateView):
    # login_url = '/login/'
    # redirect_field_name = 'mof_network/mof_list.html'
    form_class = MofForm
    model = Mof
    success_url = reverse_lazy('mof:mof_list')


class MofUpdateView(UpdateView):
    # login_url = '/login/'
    # redirect_field_name = 'mof_network/mof_detail.html'
    form_class = MofForm
    model = Mof
    # success_url = reverse_lazy('mof:mof_list')

    @staticmethod
    def get_redirect_url(self, param):
        return reverse_lazy('mof:mof_detail', kwargs={'pk': Mof.pk})


class MofDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    model = Mof
    success_url = reverse_lazy('mof:mof_list')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'mof_network/post_draft_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(date_publish__isnull=True).order_by('date_create')


def add_comment_to_mof(request, pk):
    mof = get_object_or_404(Mof, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.mof = mof
            comment.save()
            return redirect('mof:mof_detail', pk=mof.pk)

        else:
            form = CommentForm()

        return render(request, 'mof_network/comment_form.html', {'form': form})
    else:
        return render(request, 'mof_network/comment_form.html')


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('mof:post_list')


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('mof:post_detail_view', pk=Comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = Comment.post.pk
    comment.delete()
    return redirect('mof:post_detail_view', pk=post_pk)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('mof:index'))
                # Redirect to a success page.

            else:
                return HttpResponse('Your account is not active!')

        else:
            return HttpResponse("Invalid login credentials!")

    else:
        return render(request, 'login/login.html', {})
        # Return an 'invalid login' error message.


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('mof:index'))
    # Redirect to a success page.
