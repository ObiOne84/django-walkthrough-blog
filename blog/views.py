from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post
from .forms import CommentForm


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class PostDetail(View):

    def get(self, request, slug, *arg, **kwargs):
        # below, we filer arguments by status 1 = published
        queryset = Post.objects.filter(status=1)
        # here we get published post with the correct slug
        post = get_object_or_404(queryset, slug=slug)
        # below we get any comments that are attached to the post and
        # are approved, filter and order in asceding order
        comments = post.comments.filter(approved=True).order_by('created_on')
        # we set liked to false
        liked = False
        # we use the if statement to check if used id is acutally there
        # to say that they've liked the post, if they are we set liked to true
        # otherwise it will remain false
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        # we send all this information to our redner method
        # we are going to send request through
        # next we supply the template post_detail.html
        # and we will create dictionary to supply our context, so our post
        # will be post, our comments key will be the comments we got back
        # and liked will be our liked boolean
        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': False,
                'liked': liked,
                'comment_form': CommentForm()
            },
        )


    def post(self, request, slug, *arg, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
 
        # create a new variable that will get all data from the form
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': True,
                'liked': liked,
                'comment_form': CommentForm()
            },
        )