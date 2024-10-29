from django import template

register = template.Library()


@register.simple_tag()
def get_discount(discounts):
    discount = max(discounts, key=lambda obj: obj.percent)
    mount = discount.to_date.strftime("%B")[:3]
    discount.from_date = str(discount.to_date)[8:11] + mount
    return discount


@register.simple_tag()
def solve_price(price, discount):
    price_old = int(price)
    price_dis = round((price_old - price_old * discount.percent / 100), 2)
    return {"old_price": price, "dis": price_dis}
