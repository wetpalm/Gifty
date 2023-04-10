from django.urls import path
from . import views

urlpatterns = [
     path('', views.index, name="roothome"),
     path('our-partners', views.partners, name='partners'),
     path('validate-card', views.confam, name='confirm-card'),
     path('user_login', views.loginuser, name="user-login"),
     path('logout_user', views.loogout, name="logoutuser"),
     path('manage_partners', views.mnpartners, name="manage-partners"),
     path('manage_clients', views.mnclients, name="manage-clients"),
     path('client_details/<int:id>', views.clientana, name="client-detail"),
     path('batch-details/<int:batch>', views.batchview, name='batch-details'),
     path('card_templates/<int:id>', views.card_tempa, name='printer-viewa'),
     path('print_templates/<int:bat>', views.card_tempb, name='printer-viewb'),
     path('blockbatch/<int:bat>', views.block_batch, name='block-batch'),
     path('contact-us', views.contact, name="contactus"),
     path('verify/<str:cdno>', views.validatepage, name = 'valid-card'),

]
   