from django import template
import base64

register = template.Library()

@register.filter
def get_item(list_objm, index):
    try:
        return list_objm[int(index)]
    except (IndexError, TypeError):
        return None
    
@register.filter
def get_item_image(list_objm, index):
    try:
        model = list_objm[int(index)]
        return model.get_image
    except (IndexError, TypeError):
        return None
    
@register.filter
def custom_encrypt(value):
    encoded = base64.urlsafe_b64encode(str(value).encode()).decode()
    return encoded