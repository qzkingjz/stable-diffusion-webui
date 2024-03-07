from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from taggit.models import Tag
from .forms import CommentForm
from .models import Post

def post_list(request,tag_slug=None):
    if tag_slug:
        tag = Tag.objects.filter(slug=tag_slug).first()
        post_list = Post.objects.filter(tags__in=[tag])
    else:
        post_list = Post.objects.all()
    tag_list = Tag.objects.all()
    paginator = Paginator(post_list,3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        posts = Paginator.page(Paginator.num_pages)
    return render(
           request,
           'blog/post/list.html',
           {'posts':posts,'tag_list':tag_list}
    )

def post_detail(request,year,month,day,slug):
    post = Post.objects.filter(
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=slug
    ).first()
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            #Assign  the current post to the comment
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
        # pass
    return render(
        request,
        'blog/post/detail.html',
        {
            'post':post,
            'comments':comments,
            'new_comment':new_comment,
            'comment_form':comment_form
        }
    )

def comment_list(request):
    comment_list = Comment.objects.all()
    return render(
        request,
        'blog/post/list.html',
        {'comments':comments}
    )
# Create your views here.
