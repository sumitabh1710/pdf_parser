
from django.http import JsonResponse
from .models import Transaction
from django.db.models import Sum, Max, Count
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from .serializers import TransactionSerializer

@api_view(['GET'])
def total_loan_amount(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    total_loan_amount = Transaction.objects.filter(settlement_date__range=[start_date, end_date]).aggregate(total_loan_amount_during_period=Sum('total_loan_amount'))['total_loan_amount_during_period']
    return JsonResponse({'total_loan_amount_during_period': total_loan_amount})

@api_view(['GET'])
def highest_loan_amount_by_broker(request):
    broker_with_highest_loan = Transaction.objects.values('broker').annotate(highest_loan_amount=Max('total_loan_amount')).order_by('-highest_loan_amount').first()
    return JsonResponse({'broker_with_highest_loan': broker_with_highest_loan['broker'], 'highest_loan_amount': broker_with_highest_loan['highest_loan_amount']})

@api_view(['GET'])
def loan_amount_by_date_report(request):
    loan_amounts_by_date = Transaction.objects.values('settlement_date').annotate(total_loan_amount=Sum('total_loan_amount'))
    return JsonResponse(list(loan_amounts_by_date), safe=False)

@api_view(['GET'])
def broker_loan_report(request):
    broker_name = request.GET.get('broker_name')
    period = request.GET.get('period')
    if period == 'daily':
        start_date = datetime.now().date()
        end_date = start_date - timedelta(days=1)
    elif period == 'weekly':
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
    elif period == 'monthly':
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
    else:
        return JsonResponse({'error': 'Invalid period provided'}, status=400)

    transactions = Transaction.objects.filter(broker=broker_name, settlement_date__range=[start_date, end_date]).order_by('-total_loan_amount')
    serializer = TransactionSerializer(transactions, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def tier_level_report(request):
    transactions = Transaction.objects.all()
    for transaction in transactions:
        if transaction.total_loan_amount > 100000:
            transaction.tier_level = 'Tier 1'
        elif transaction.total_loan_amount > 50000:
            transaction.tier_level = 'Tier 2'
        elif transaction.total_loan_amount > 10000:
            transaction.tier_level = 'Tier 3'
        else:
            transaction.tier_level = 'Tier 4'
    serializer = TransactionSerializer(transactions, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def loans_by_tier_and_date_report(request):
    loans_by_tier_and_date = Transaction.objects.values('settlement_date', 'tier_level').annotate(count=Count('id'))
    return JsonResponse(list(loans_by_tier_and_date), safe=False)


