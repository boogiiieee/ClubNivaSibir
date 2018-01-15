Позволяет в шаблоне загружать список баннеров в контекстную переменную banners_list

INSTALLED_APPS = (
	...
	'banners',
	...
)

{% load banners_tags %}
{% get_banners_list %}