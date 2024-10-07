"""
    Функции serializer_data_user() и serializer_data_session()
    подготавливают одинаковую структуру данных словаря для шаблона cart.html
    в не зависимости авторизован пользователь или нет
"""

from .pydentic_models import CartModel, SellerPriceModel


def serializer_data_user(carts) -> list[dict]:
    """Функция для обработки данных о корзине пользователя если он был аутентифицирован"""
    if_authenticated = [CartModel.model_validate(book, from_attributes=True).dict() for book in carts]
    for id_col, col in enumerate(if_authenticated):
        col['sellerprice']['id'] = col['id']
        col['image'] = carts[id_col].sellerprice.product.one_image
    return if_authenticated


def serializer_data_session(carts) -> list[dict]:
    """Функция для обработки данных о корзине пользователя если он не был аутентифицирован"""
    not_authenticated = [SellerPriceModel.model_validate(book, from_attributes=True).dict() for book in carts]
    f = []
    for id_col, col in enumerate(not_authenticated):
        new, new["id"] = {}, col['id']
        new['sellerprice'] = col
        new['image'] = carts[id_col].product.one_image
        f.append(new)
    return f
