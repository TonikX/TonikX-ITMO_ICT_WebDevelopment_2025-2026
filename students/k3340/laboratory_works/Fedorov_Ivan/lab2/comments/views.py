from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import CommentForm
from .models import Comment
from races.models import Race


@login_required
def add_comment(request, race_id):
    race = get_object_or_404(Race, id=race_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.race = race
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий успешно добавлен!')
            return redirect('race_detail', race_id=race_id)
    else:
        form = CommentForm()

    return render(request, 'comments/add_comment.html', {
        'form': form,
        'race': race,
    })


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    race_id = comment.race.id
    comment.delete()
    messages.success(request, 'Комментарий удален!')
    return redirect('race_detail', race_id=race_id)


def comment_list(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    comments_list = Comment.objects.filter(race=race).order_by('-created_at')

    paginator = Paginator(comments_list, 10)  # 10 комментариев на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'comments/comment_list.html', {
        'race': race,
        'page_obj': page_obj,
    })