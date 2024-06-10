from django import template

register = template.Library()

register.filter("currency", lambda x: '{:.2f} NOK'.format(x).replace(".", ","))
register.filter("minor_currency", lambda x: '{:.2f} NOK'.format(x/100).replace(".", ","))
