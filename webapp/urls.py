# urls.py
from django.urls import path

from webapp import views
from webapp.views import logout_view
from webapp.views.HistoryAuditsViews import job_history_view, job_history_query
from webapp.views.JobCardPDFView import JobQuickView, JobCardPDFView
from webapp.views.KnowledgeBaseViews import knowledge_base_list, knowledge_base_detail, knowledge_base_create

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-job/', views.create_job, name='create_job'),
    # path('job_cards/', views.get_job_cards, name='job_cards'),
    path('success/', views.success_view, name='success_page'),
    path('success_update/', views.update_success_view, name='update_success_page'),
    path('success_item/', views.item_success_view, name='item_success_page'),
    path('open_job_cards/', views.open_job_cards, name='open_job_cards'),
    path('edit_job_card/<int:job_card_id>/', views.edit_job_card, name='edit_job_card'),
    path('close_job_card/<int:job_card_id>/', views.close_job_card, name='close_job_card'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-error-code/', views.add_error_code, name='add_error_code'),
    path('add-region/', views.add_region, name='add_region'),
    path('add-vendor/', views.add_vendor, name='add_vendor'),
    path('add-rma/', views.add_rma, name='add_rma'),
    path('open-rmas/', views.open_rmas, name='open_rmas'),
    path('edit-rma/<int:rma_id>/', views.edit_rma, name='edit_rma'),
    path('convert-rma/<int:rma_id>/', views.convert_rma, name='convert_rma'),
    path('logout/', logout_view, name='logout'),

    path('job-quick-view/', JobQuickView.as_view(), name='job_quick_view'),
    path('generate-pdf/<int:job_card_id>/', JobCardPDFView.as_view(), name='generate_pdf'),

    path('job_history/', job_history_query, name='job_history_query'),
    path('job_history/<int:job_card_id>/', job_history_view, name='job_history_view'),

    # Knowledge Base
    path('knowledge_base/', knowledge_base_list, name='knowledge_base_list'),
    path('knowledge_base/<int:kb_id>/', knowledge_base_detail, name='knowledge_base_detail'),
    path('knowledge_base/create/', knowledge_base_create, name='knowledge_base_create'),

]