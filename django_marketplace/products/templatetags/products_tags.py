from django import template

register = template.Library()


@register.simple_tag()
def get_discount(discounts):
    discount = max(discounts, key=lambda obj: obj.percent)
    discount.from_date = str(discount.from_date)[5:11] + str(discount.to_date)[5:11]
    return discount


@register.simple_tag()
def solve_price(price, discount):
    price_old = price
    p = int(price)
    price_dis = round((p - p * discount.percent / 100), 2)
    return {"old_price": price, "dis": price_dis}
