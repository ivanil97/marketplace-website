

def solve_total_price(carts) -> dict:
    """Дополнительная функция для подсчета полной стоимости всех товаров"""
    total_price = 0
    total_quantity = 0
    for col in carts:
        if not col.get("deleted"): # Расчет полной стоимости идет в том случае если товар из сессии не был удален
            price, discount, quantity = col.get('price'), col.get('discount'), col.get('quantity')
            if discount:
                p = round((price - price * discount[0].percent / 100) * col['quantity'], 2)
            else:
                p = price * quantity

            total_quantity += quantity
            total_price += p

    total_price = float(total_price)
    if total_quantity > 5 and total_price > 500:
        return {"total_price": round(total_price - (total_price * 0.1), 2), "total_quantity": total_quantity}
    elif total_price > 500:
        return {"total_price": round(total_price - (total_price * 0.05), 2), "total_quantity": total_quantity}
    elif total_quantity > 5:
        return {"total_price": round(total_price - (total_price * 0.05), 2), "total_quantity": total_quantity}

    return {"total_price": total_price, "total_quantity": total_quantity}


def prepare_data(request, carts) -> list[dict]:
    """Дополнительная функция для подготовки данных о корзинах пользователя для header"""
    if request.user.is_authenticated:
        prepare = [
            {
                "price": col.sellerprice.price,
                "discount": col.sellerprice.product.one_discount if col.sellerprice.product else 0,
                "quantity": col.quantity
            }
            for col in carts
        ]
    else:
        prepare = [
            {
                "price": col.price,
                "discount": col.product.one_discount if col.product else 0,
                "quantity": request.session['cart'][str(col.id)].get('quantity'),
                "deleted": request.session['cart'][str(col.id)].get('deleted') # Флаг отвечающий за удаленный товар в сессии
            }
            for col in carts
        ]
    return prepare
