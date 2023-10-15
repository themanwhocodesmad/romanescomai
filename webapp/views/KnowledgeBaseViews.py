from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from webapp.forms.KnowledgeBaseForms import KnowledgeBaseForm
from webapp.models import KnowledgeBase


@login_required
def knowledge_base_list(request):
    kb_items = KnowledgeBase.objects.all()
    return render(request, 'webapp/knowledgebase/knowledge_base_list.html', {'kb_items': kb_items})


@login_required
def knowledge_base_detail(request, kb_id):
    kb_item = get_object_or_404(KnowledgeBase, id=kb_id)
    return render(request, 'webapp/knowledgebase/knowledge_base_detail.html', {'kb_item': kb_item})


@login_required
def knowledge_base_create(request):
    if request.method == 'POST':
        form = KnowledgeBaseForm(request.POST)
        if form.is_valid():
            kb_item = form.save(commit=False)
            kb_item.author = request.user
            kb_item.save()
            return redirect('knowledge_base_detail', kb_id=kb_item.id)
    else:
        form = KnowledgeBaseForm()
    return render(request, 'webapp/knowledgebase/knowledge_base_form.html', {'form': form})
