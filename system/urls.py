from django.urls import path

from .customer_responses.survey import CustomerSatisfactionFormView, SurveySuccessView
from .views import DashboardDataView, CreateNewJobView, JobQueryView, CloseJobView, FetchJobView, UpdateJobView, \
    DatabaseDownloadView, DownloadJobCardView, UploadImagesView, UserAssignedJobsList

urlpatterns = [


    path('dashboard-repair-statistics/', DashboardDataView.as_view(), name='dashboard-data'),
    path('jobs/create-new-job/', CreateNewJobView.as_view(), name='new-job'),
    path('jobs/query/<str:queryType>/<str:inputQuery>/', JobQueryView.as_view(), name='query-job'),
    path('jobs/close-job/<str:job_number>/', CloseJobView.as_view(), name='close-job'),
    path('jobs/fetch-job/<str:job_number>/', FetchJobView.as_view(), name='fetch-job'),
    path('jobs/update-job/<str:job_number>/', UpdateJobView.as_view(), name='update-job'),
    path('jobs/download/database/', DatabaseDownloadView, name='database-download'),
    path('jobs/download/jobcard/<str:job_number>/', DownloadJobCardView.as_view(), name='download-job-card'),
    path('jobs/pictures/upload/<str:job_number>/', UploadImagesView.as_view(), name='upload_images'),
    path('jobs/assigned/', UserAssignedJobsList.as_view(), name='assigned_jobs'),

    # Customer survey
    path('review-form/<str:job_number>/', CustomerSatisfactionFormView.as_view(), name='customer-satisfaction'),
    path('survey-success/', SurveySuccessView.as_view(), name='survey-success'),


    # path('create-job/', views.create_job, name='job-card-create'),
    #
    # path('query-job/', views.QueryJobView.as_view(), name='query-job'),
    #
    # path('database-details/', views.DatabaseDetailsView.as_view(), name='database-details'),
    #
    # path('download-job-cards/', views.export_job_cards, name='export_job_cards'),
    #
    # path('job-card-pdf/<str:job_number>/', views.JobCardPDFViewAlt.as_view(), name='job_card_pdf'),
    #
    # path('job-card/<int:id>/', views.JobCardDetailView.as_view(), name='jobcard-detail'),
    #
    # path('job-cards/update/<int:id>/', views.JobCardUpdateView.as_view(), name='jobcard-update'),
    #
    # path('job-card/images/<int:job_id>/', views.JobImagesUploadView.as_view(), name='job-images-upload'),
    #
    # path('job-card/close/<int:id>/', views.CloseJobCardView.as_view(), name='close-jobcard'),

]
