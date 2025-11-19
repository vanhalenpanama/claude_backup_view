import json
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import DataEntry
from .forms import JSONUploadForm

class ClaudeHomeView(TemplateView):
    template_name = 'claude/home.html'

class JSONUploadView(FormView):
    template_name = 'claude/upload_json.html'
    form_class = JSONUploadForm
    success_url = reverse_lazy('claude:upload_json')

    def form_valid(self, form):
        json_file = form.cleaned_data['json_file']
        data = json.load(json_file)

        for item in data:
            name = item.get('name') or 'unnamed chat'
            DataEntry.objects.update_or_create(
                uuid=item.get('uuid'),
                defaults={
                    'name': name,
                    'created_at': item.get('created_at'),
                    'updated_at': item.get('updated_at'),
                    'chat_messages': item.get('chat_messages')
                }
            )
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = self.request.GET.get('message')
        return context

def list_entries(request):
    page = request.GET.get('page', '1')
    data_entries = DataEntry.objects.order_by('-created_at')
    paginator = Paginator(data_entries, 13)
    page_obj = paginator.get_page(page)

    context = {
        'entries': page_obj,
    }
    return render(request, 'claude/list_entries.html', context)

class DataEntryDetailView(DetailView):
    model = DataEntry
    template_name = 'claude/detail_entry.html'
    context_object_name = 'entry'

class DeleteAllDataView(TemplateView):
    template_name = 'claude/upload_json.html'
    
    def post(self, request, *args, **kwargs):
        DataEntry.objects.all().delete()
        remaining_count = DataEntry.objects.count()
        if remaining_count == 0:
            message = "데이터가 삭제되었습니다."
        else:
            message = "데이터 삭제에 실패했습니다."
        return redirect(f'{reverse_lazy("claude:upload_json")}?message={message}')