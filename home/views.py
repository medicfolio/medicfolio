# home/views.py 

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
import json
from datetime import date
from decimal import Decimal

from .models import Client, Product, Transaction

# Vista para el home/dashboard
def home_view(request):
    if request.user.is_authenticated:
        return redirect('home:dashboard')  # Redirige al dashboard si está autenticado
    return render(request, 'home/home.html')  # Redirige al home público si no está autenticado

# Vista del dashboard
@login_required
def dashboard_view(request):
    return render(request, 'home/dashboard.html')


@login_required
def salon_view(request):
    """Pantalla principal del sistema de gestión de peluquería."""

    return render(request, 'home/salon_dashboard.html')


def _serialize_client(client: Client) -> dict:
    return {
        '__backendId': client.id,
        'type': 'client',
        'name': client.name,
        'phone': client.phone,
        'email': client.email,
        'birthday': client.birthday.isoformat() if client.birthday else '',
        'frequency': client.frequency,
        'notes': client.notes,
        'lastVisit': client.last_visit.isoformat() if client.last_visit else '',
    }


def _serialize_product(product: Product) -> dict:
    return {
        '__backendId': product.id,
        'type': 'product',
        'productName': product.product_name,
        'category': product.category,
        'quantity': product.quantity,
        'price': float(product.price),
        'minStock': product.min_stock,
        'forSale': product.for_sale,
    }


def _serialize_transaction(transaction: Transaction) -> dict:
    return {
        '__backendId': transaction.id,
        'type': 'transaction',
        'transactionType': transaction.transaction_type,
        'clientId': transaction.client_id or '',
        'description': transaction.description,
        'amount': float(transaction.amount),
        'date': transaction.date.isoformat(),
        'items': transaction.items,
    }


@login_required
def salon_data(request):
    """Devuelve todos los datos del sistema para el frontend."""

    clients = [_serialize_client(c) for c in Client.objects.all()]
    products = [_serialize_product(p) for p in Product.objects.all()]
    transactions = [_serialize_transaction(t) for t in Transaction.objects.all()]
    return JsonResponse({
        'clients': clients,
        'products': products,
        'transactions': transactions,
    })


def _parse_date(value):
    if not value:
        return None
    try:
        cleaned = value.split('T')[0]
        return date.fromisoformat(cleaned)
    except ValueError:
        return None


@login_required
@require_http_methods(["POST"])
def salon_clients(request):
    payload = json.loads(request.body or '{}')
    client = Client.objects.create(
        name=payload.get('name', ''),
        phone=payload.get('phone', ''),
        email=payload.get('email', ''),
        birthday=_parse_date(payload.get('birthday')),
        frequency=int(payload.get('frequency') or 30),
        notes=payload.get('notes', ''),
        last_visit=_parse_date(payload.get('lastVisit')),
    )
    return JsonResponse({'isOk': True, 'data': _serialize_client(client)})


@login_required
@require_http_methods(["PUT"])
def salon_clients_detail(request, client_id: int):
    payload = json.loads(request.body or '{}')
    client = Client.objects.filter(id=client_id).first()
    if not client:
        return JsonResponse({'isOk': False, 'error': 'Cliente no encontrado'}, status=404)

    for field, value in {
        'name': payload.get('name'),
        'phone': payload.get('phone'),
        'email': payload.get('email', ''),
        'birthday': _parse_date(payload.get('birthday')),
        'frequency': int(payload.get('frequency')) if payload.get('frequency') is not None else None,
        'notes': payload.get('notes', ''),
        'last_visit': _parse_date(payload.get('lastVisit')),
    }.items():
        if value is not None:
            setattr(client, field, value)
    client.save()
    return JsonResponse({'isOk': True, 'data': _serialize_client(client)})


@login_required
@require_http_methods(["DELETE"])
def salon_clients_delete(request, client_id: int):
    client = Client.objects.filter(id=client_id).first()
    if not client:
        return JsonResponse({'isOk': False, 'error': 'Cliente no encontrado'}, status=404)
    client.delete()
    return JsonResponse({'isOk': True})


@login_required
@require_http_methods(["POST"])
def salon_products(request):
    payload = json.loads(request.body or '{}')
    product = Product.objects.create(
        product_name=payload.get('productName', ''),
        category=payload.get('category', ''),
        quantity=int(payload.get('quantity') or 0),
        price=Decimal(str(payload.get('price') or 0)),
        min_stock=int(payload.get('minStock') or 0),
        for_sale=bool(payload.get('forSale')),
    )
    return JsonResponse({'isOk': True, 'data': _serialize_product(product)})


@login_required
@require_http_methods(["PUT"])
def salon_products_detail(request, product_id: int):
    payload = json.loads(request.body or '{}')
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return JsonResponse({'isOk': False, 'error': 'Producto no encontrado'}, status=404)

    for field, value in {
        'product_name': payload.get('productName'),
        'category': payload.get('category'),
        'quantity': int(payload.get('quantity')) if payload.get('quantity') is not None else None,
        'price': Decimal(str(payload.get('price'))) if payload.get('price') is not None else None,
        'min_stock': int(payload.get('minStock')) if payload.get('minStock') is not None else None,
        'for_sale': payload.get('forSale'),
    }.items():
        if value is not None:
            setattr(product, field, value)
    product.save()
    return JsonResponse({'isOk': True, 'data': _serialize_product(product)})


@login_required
@require_http_methods(["DELETE"])
def salon_products_delete(request, product_id: int):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return JsonResponse({'isOk': False, 'error': 'Producto no encontrado'}, status=404)
    product.delete()
    return JsonResponse({'isOk': True})


@login_required
@require_http_methods(["POST"])
def salon_transactions(request):
    payload = json.loads(request.body or '{}')
    client = None
    client_id = payload.get('clientId') or None
    if client_id:
        client = Client.objects.filter(id=client_id).first()

    transaction = Transaction.objects.create(
        transaction_type=payload.get('transactionType'),
        client=client,
        description=payload.get('description', ''),
        amount=Decimal(str(payload.get('amount') or 0)),
        date=_parse_date(payload.get('date')) or date.today(),
        items=payload.get('items', ''),
    )

    # Actualiza la última visita del cliente cuando se registra un servicio
    if transaction.transaction_type == Transaction.SERVICE and client:
        client.last_visit = transaction.date
        client.save(update_fields=['last_visit'])

    return JsonResponse({'isOk': True, 'data': _serialize_transaction(transaction)})


@login_required
@require_http_methods(["DELETE"])
def salon_transactions_delete(request, transaction_id: int):
    transaction = Transaction.objects.filter(id=transaction_id).first()
    if not transaction:
        return JsonResponse({'isOk': False, 'error': 'Transacción no encontrada'}, status=404)
    transaction.delete()
    return JsonResponse({'isOk': True})
