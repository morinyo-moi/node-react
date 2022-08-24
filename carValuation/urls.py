from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('valuation/', views.valuation, name='valuation'),
    path('insurance_companies/', views.insuranceCompanies, name='insurance_companies'),
    path('personal_details/', views.personalDetails, name='personal_details'),
    path('personalDetails/', views.personalDetail, name='personalDetails'),
    path('details_summary/', views.detailsSummary, name='details_summary'),
    path('payment_option/', views.paymentOption, name='payment_option'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('valuate/',views.valuate, name='valuate'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('insurance/', views.insurance, name='insurance'),
    path('model/<str:id>', views.modelbymake, name='make'),
    path('mobilePayment/', views.mobilePayment, name='lipa_na_mpesa'),
    path('signLogbook_s3/', views.signLogbook_s3, name='signLogbook_s3'),
    path('signNatid_s3/', views.signNatid_s3, name='signNatid_s3'),
    path('showConfirmation/', views.showConfirmation, name='showConfirmation'),
    path('saveContact/', views.saveContact, name='saveContact'),
    path('saveRating/', views.saveRating, name='saveRating'),
]