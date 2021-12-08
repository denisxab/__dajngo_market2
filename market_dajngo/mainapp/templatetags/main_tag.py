from django import template

from market_dajngo.settings import MEDIA_URL

register = template.Library()


@register.simple_tag()
def UrlMedia(path):
	"""
	{% UrlMedia 'url_фото.png'%}
	"""
	return f"{MEDIA_URL}{path}"
