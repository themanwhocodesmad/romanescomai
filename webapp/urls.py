# urls.py
from django.urls import path

from webapp import views
from webapp.views import logout_view

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-job/', views.create_job, name='create_job'),
    path('success/', views.success_view, name='success_page'),
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


]