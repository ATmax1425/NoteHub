from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('upload_profile_image/', views.upload_profile_image, name='upload-profile-image'),
    path('register_int/', views.register_int, name='register-int'),
    path('set_password/', views.set_pasword_for_social_account, name='set-password'),
    path('send_code/', views.send_verification_code, name='send-code'),
    path('<str:encoded_email>/verify/', views.verify_user, name='verify-user'),
    path('user_verification_status/', views.user_verification_status, name='user-verification-status'),
    path('resend_verification_email/', views.resend_verification_email, name='resend-verification-email'),
    path('validate_code/', views.validate_verification_code, name='validate-code'),
    path('update_password/', views.update_password, name='update-password'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('feed/', views.feed, name='feed'),
    path('upload_document_file/', views.upload_document_file, name='upload-document-file'),
    path('add_notes/', views.add_notes, name='add-notes'),
    path('load_posts/<int:limit>/<str:last_doc_id>/', views.load_posts, name='load-posts'),
]