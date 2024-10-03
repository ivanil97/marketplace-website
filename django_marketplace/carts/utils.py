

def solve_total_price(carts) -> int:
    """Дополнительная функция для подсчета полной стоимости всех товаров"""
    total_price = 0
    for col in carts:
        if not col.get("deleted"): # Расчет полной стоимости идет в том случае если товар из сессии не был удален
            price, discount, quantity = col.get('price'), col.get('discount'), col.get('quantity')
            if discount:
                p = round((price - price * discount[0].percent / 100) * col['quantity'], 2)
            else:
                p = price * quantity
            total_price += p
    return total_price


def prepare_data(request, carts) -> list[dict]:
    """Дополнительная функция для подготовки данных о корзинах пользователя для header"""
    if request.user.is_authenticated:
        prepare = [
            {
                "price": col.sellerprice.price,
                "discount": col.sellerprice.product.one_discount,
                "quantity": col.quantity
            }
            for col in carts
        ]
    else:
        prepare = [
            {
                "price": col.price,
                "discount": col.product.one_discount,
                "quantity": request.session['cart'][str(col.id)].get('quantity'),
                "deleted": request.session['cart'][str(col.id)].get('deleted') # Флаг отвечающий за удаленный товар в сессии
            }
            for col in carts
        ]
    return prepare
