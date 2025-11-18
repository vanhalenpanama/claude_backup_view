from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q, F
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse

import logging


class HomeView(TemplateView):
    template_name = 'blog/index.html'


class PostListView(ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 2  # 페이지당 n개의 게시글

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        category = self.request.GET.get('category')
        order = self.request.GET.get('order', '-created_at')

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query))
        
        if category and category != '전체':
            queryset = queryset.filter(category__name=category)

        return queryset.order_by(order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category', '전체')
        context['search_query'] = self.request.GET.get('search', '')
        context['current_order'] = self.request.GET.get('order', '-created_at')
        return context



class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db() # detail.html
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        
        # 최상위 댓글만 가져오기
        top_level_comments = self.object.comments.filter(parent=None).order_by('created_at')
        
        # 각 최상위 댓글의 대댓글을 재귀적으로 가져오는 함수
        def get_replies(comment):
            replies = comment.replies.all().order_by('created_at')
            for reply in replies:
                reply.children = get_replies(reply)
            return replies

        # 각 최상위 댓글에 대해 대댓글 트리 구성
        for comment in top_level_comments:
            comment.children = get_replies(comment)

        context['comments'] = top_level_comments
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = get_object_or_404(Comment, id=parent_id)
            comment.save()
        return redirect('post_detail', pk=self.object.pk)


logger = logging.getLogger(__name__)
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/write.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        if 'image' in self.request.FILES:
            image_file = self.request.FILES['image']
            
        return super().form_valid(form)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        inappropriate_words = ['욕설1', '욕설2', '비속어1', '비속어2']  

        for word in inappropriate_words:
            if word in title or word in content:
                raise ValidationError("부적절한 단어가 포함되어 있습니다.")

        return cleaned_data


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/edit.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        if 'image' in self.request.FILES:
            image_file = self.request.FILES['image']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class PostSearchView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.kwargs.get('tag')
        return Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag')
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_update.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})    
    

