from django import template
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
    res = css.split(',')
    return field.as_widget(attrs={"class":res[0],"placeholder":res[1]})

