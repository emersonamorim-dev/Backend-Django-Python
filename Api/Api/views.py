import paypalrestsdk
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

class MyAPI(viewsets.ViewSet):
    def list(self, request):
        # Implemente sua lógica de API aqui
        return Response({'message': 'Api Rest Django!'})

@api_view(['POST'])
@swagger_auto_schema(request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Montante a ser pago'),
        'currency': openapi.Schema(type=openapi.TYPE_STRING, description='Moeda'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='Descrição de pagamento'),
    },
    required=['amount', 'currency', 'description'],
))
def paypal_payment_view(request):
    amount = request.data['amount']
    currency = request.data['currency']
    description = request.data['description']

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8000/paypal/success",
            "cancel_url": "http://localhost:8000/paypal/cancel"
        },
        "transactions": [{
            "amount": {
                "total": str(amount),
                "currency": currency
            },
            "description": description
        }]
    })

    if payment.create():
        return Response({'redirect_url': payment.links[1].href})
    else:
        return Response({'error': payment.error})


@api_view(['GET'])
def paypal_payment_success_view(request):
    payment_id = request.GET.get('paymentId')
    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({'payer_id': request.GET.get('PayerID')}):
        return Response({'message': 'Pagamento concluído com sucesso.'})
    else:
        return Response({'error': payment.error})
