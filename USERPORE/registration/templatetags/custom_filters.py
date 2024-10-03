from django import template

register = template.Library()

@register.filter
def product_type(num):
    if num == 1:
        product_type = "휘낭시에"
    elif num == 2:
        product_type = "조각케이크"
    elif num == 3:
        product_type = "스콘"
    elif num == 4:
        product_type = "특별메뉴"
    
    return product_type