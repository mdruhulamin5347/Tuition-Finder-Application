from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import PostModel, Subject, ClassIn, Comment, PhotoAddModel, District, Category
from .forms import PostForm, PhotoAddForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from notifications.signals import notify
from .templatetags import tag
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


@login_required
def post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        
        if form.is_valid():
            subjects = form.cleaned_data['subject']
            classins = form.cleaned_data['classin']
            categories = form.cleaned_data.get('category', '')
          
            if len(subjects) > 3:
                form.add_error('subject', 'You cannot select more than 3 subjects.')         

            if categories:
                if categories.name == 'Teacher' :
                    if len(classins) > 2:
                        form.add_error('classin', 'You cannot select more than 2 classin options.')
                else:
                    if len(classins) > 1:
                        form.add_error('classin', 'You cannot select more than 1 classin option.')
    
            if form.errors:
                return render(request, 'post/post.html', {'form': form})           

            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            obj.subject.set(subjects)
            obj.classin.set(classins)
            

            messages.success(request, 'Successfully submitted your post')
            return redirect('post_list')
    else:
        form = PostForm()

    return render(request, 'post/post.html', {'form': form})




class PostListView(ListView):
    template_name = 'post/list.html'
    queryset = PostModel.objects.all()  
    def get_queryset(self):
        queryset = PostModel.objects.all()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category=category_id)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['posts'] = context.get('object_list')
        context['subjects'] = Subject.objects.all()
        context['classin'] = ClassIn.objects.all()
        context['categories'] = Category.objects.all()
        return context

class PostDetailView(DetailView):
    model = PostModel
    template_name = 'post/details.html'

    def get_context_data(self, *args, **kwargs):
        self.object.views.add(self.request.user)
        liked = False
        if self.object.likes.filter(id=self.request.user.id).exists():
            liked = True
        context = super().get_context_data(*args, **kwargs)
        object = context.get('object')
        comments = Comment.objects.filter(post=object.id, parent=None)
        replies = Comment.objects.filter(post=object.id).exclude(parent=None)
        dictofreply = {}
        for reply in replies:
            if reply.parent.id not in dictofreply:
                dictofreply[reply.parent.id] = [reply]
            else:
                dictofreply[reply.parent.id].append(reply)

        context['comments'] = comments
        context['dictofreply'] = dictofreply
        context['liked'] = liked
        return context

def like_post(request, id):
    if request.method == 'POST':
        post = PostModel.objects.get(id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            if request.user != post.user:
                notify.send(request.user, recipient=post.user, verb="has liked your post" + f'''<a href="/post-details/{post.id}"> Go </a>''')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def notification(request):
    return render(request, 'post/notifications.html')

class PostUpdateView(UpdateView):
    model = PostModel
    form_class = PostForm
    template_name = 'post/post.html'

    def get_success_url(self):
        id = self.object.id
        return reverse_lazy('post_detail', kwargs={'pk': id})

def post_delete(request, id):
    post = PostModel.objects.get(id=id)
    post.delete()
    return HttpResponseRedirect('/post/list/')

def search(request):
    query = request.POST.get('search', ' ')
    if query:
        queryset = (Q(user__username__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query) |
                    Q(district__name__icontains=query) |
                    Q(created_at__icontains=query) | 
                    Q(title__icontains=query) |
                    Q(salary__icontains=query) | 
                    Q(details__icontains=query) | 
                    Q(language__icontains=query) | 
                    Q(category__name__icontains=query) | 
                    Q(subject__name__icontains=query) | 
                    Q(classin__name__icontains=query))
        posts = PostModel.objects.filter(queryset).distinct()
    else:
        posts = []
    subject = Subject.objects.all()
    classin = ClassIn.objects.all()
    categories = Category.objects.all()
    return render(request, 'post/list.html', {'posts': posts,'subjects':subject, 'classin':classin,'categories':categories})



def filter(request):
    posts = []
    subjects = Subject.objects.all()
    classin = ClassIn.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        category = request.POST.get('category', '').strip()
        subject = request.POST.get('subject', '').strip()
        classin_value = request.POST.get('classin', '').strip()
        available = request.POST.get('available', '').strip()
        salary_from = request.POST.get('salary_from', '').strip()
        salary_to = request.POST.get('salary_to', '').strip()

        # Build the query using Q objects
        queryset = Q()
        if category:
            queryset &= Q(category__name__icontains=category)
        if subject:
            queryset &= Q(subject__name__icontains=subject)
        if classin_value:
            queryset &= Q(classin__name__icontains=classin_value)
        if available:
            queryset &= Q(available=True)
        elif available:
            queryset &= Q(available=False)
        if salary_from:
            queryset &= Q(salary__gte=salary_from)
        if salary_to:
            queryset &= Q(salary__lte=salary_to)

        # Apply the filters if any are set
        if queryset:
            posts = PostModel.objects.filter(queryset).distinct()

    return render(request, 'post/list.html', {'posts': posts, 'subjects': subjects, 'classin': classin,'categories':categories})


def comment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        parentid = request.POST.get('parentid')
        postid = request.POST.get('postid')
        post = PostModel.objects.get(id=postid)
        if parentid:
            parent = Comment.objects.get(id=parentid)
            newcom = Comment(text=comment, user=request.user, post=post, parent=parent)
        else:
            newcom = Comment(text=comment, user=request.user, post=post)
        newcom.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_photo(request, id):
    post = PostModel.objects.get(id=id)
    if request.method == 'POST':
        form = PhotoAddForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            obj = PhotoAddModel(image=image, post=post)
            obj.save()
            messages.success(request, 'Successfully uploaded your picture')
            return redirect(f"/post/details/{id}")
    else:
        form = PhotoAddForm()

    context = {
        'form': form,
        'id': id,
    }
    return render(request, 'picadd.html', context)

def apply(request, id):
    post = PostModel.objects.get(id=id)
    notify.send(request.user, recipient=post.user, verb="has applied for tuition" + f'''<a href="/post-details/{post.id}"> Go </a>''')
    messages.success(request, "Your request has been successfully submitted")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

import requests
import json

def post_views(request):
    try:
        api_integration = requests.get("https://jsonplaceholder.typicode.com/posts")
        api = api_integration.json()  # Use .json() method directly
    except requests.RequestException as e:
        api = {"error": str(e)}  # Return the error as part of the response
    return render(request, "post/postviews.html", {'api': api})
