from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from blog.models import *
from django.forms import ModelForm
from django.core.context_processors import csrf


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]

def main(request):
    """Main listing"""
    posts = Post.objects.all().order_by("-created")
    paginator = Paginator(posts, 2)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    return render_to_response("list.html", dict(posts=posts, user=request.user))

def post(request, pk):
    """Single post with comments and a comment form"""
    post = Post.objects.get(pk=int(pk))
    d = dict(post=post, user=request.user)
    return render_to_response('post.html', d)

def add_comment(request, pk):
    """Add a new comment"""
    p = request.POST

    if p.has_key('body') and p['body']:
        author = "Anonymouse"
        if p['author']: autho = p['author']

        comment = Comment(post=Post.objects.get(k=pk))
        cf = CommentForm(p, instance=comment)
        cf.fields['author'].required = False

        comment = cf.save(commit=False)
        comment.author = author
        comment.save()

    return HttpResponseRedirect(reverse('blog.views.post', args=[pk]))

def post(request, pk):
    """Single post with comments and a comment form"""
    post=Post.objects.get(pk=int(pk))
    comments = Comment.objects.filter(post=post)
    d = dict(post=post, comments=comments, form=CommentForm(), user=request.user)
    d.update(csrf(request))
    return render_to_response('post.html', d)


