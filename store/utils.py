import json
from . import models

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except KeyError:
        cart = {}
    print('Cart:', cart)
    items = []
    order = {'cart_total': 0, 'cart_items': 0, 'shipping': False}
    cartItems = order['cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = models.Product.objects.get(id=i)
            total = product.price * cart[i]['quantity']

            order['cart_total'] += total
            order['cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[i]['quantity'],
                'total_price': total
            }
            items.append(item)

            if product.digital is False:
                order['shipping'] = True
        except Exception:
            pass
    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = models.Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems': cartItems, 'order': order, 'items': items}
