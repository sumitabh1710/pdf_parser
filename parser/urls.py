from django.urls import path
from .views import total_loan_amount, highest_loan_amount_by_broker, loan_amount_by_date_report, broker_loan_report, tier_level_report, loans_by_tier_and_date_report

urlpatterns = [
    path('total-loan-amount/', total_loan_amount, name='total_loan_amount'),
    path('highest-loan-broker/', highest_loan_amount_by_broker, name='highest_loan_amount_by_broker'),
    path('loan_amount_by_date_report/', loan_amount_by_date_report, name='loan_amount_by_date_report'),
    path('broker_loan_report/', broker_loan_report, name='broker_loan_report'),
    path('tier_level_report/', tier_level_report, name='tier_level_report'),
    path('loans_by_tier_and_date_report/', loans_by_tier_and_date_report, name='loans_by_tier_and_date_report'),
]
