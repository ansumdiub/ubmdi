from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView)
from .forms import PostForm, CommentForm, MofForm
from .models import *
import logging
logger = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = 'mof_network/index.html'


class AboutView(TemplateView):
    template_name = 'mof_network/about.html'


class MapView(TemplateView):
    template_name = 'mof_network/map_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Node'] = Mof.objects.raw('SELECT name, fingerprint FROM mof_network_mof WHERE name="AA"')[0].fingerprint
        return context


# def graph(request):
#     data = Post.objects.filter(name__startswith='Test') \ #change here for filter. can be any kind of filter really
#                        .extra(select={'month': connections[Play.objects.db].ops.date_trunc_sql('month', 'date')}) \
#                        .values('month') \
#                        .annotate(count_items=Count('id'))
#
#     formattedData =json.dumps([dict(item) in list(data)])
#     #This is a two-fer. It converts each item in the Queryset to a dictionary and
#     #then formats it using the json from import json above
#     #now we can pass formattedData via the render request
#     return render(request, 'mof_network/map_view.html', {'formattedData':formattedData})


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
    success_url = reverse_lazy('mof:mof_detail', pk=Mof.pk)


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
