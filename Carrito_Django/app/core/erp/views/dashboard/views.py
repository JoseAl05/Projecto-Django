from django.urls.base import reverse_lazy
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Admin Panel'
        context['entity'] = 'Categories' 
        context['list_url'] = reverse_lazy('category_list')
        return context