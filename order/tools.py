from order.models import Coupon, OrderCalcModel


def get_total_price(user, token=None, coupon=None):
    coupon = Coupon.objects.filter(name=coupon, number_of_uses__gte=1).exclude(user=user).first()
    order_calc = OrderCalcModel.objects.last()
    if not token and not coupon:
        return order_calc.total
    total_cents = float(order_calc.total.replace("$", "")) * 100
    if token and total_cents > user.dms_tokens * 100:
        total_cents -= user.dms_tokens * 100

    if coupon:
        total_cents *= coupon.get_discount_modifier()
    total_cents = total_cents / 100
    return f"{round(total_cents , 2)}$"



