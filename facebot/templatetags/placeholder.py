from django import template
register = template.Library()

@register.filter(name='placeholder')
def placeholder(field, holder):
   return field.as_widget(attrs={"placeholder":holder})
