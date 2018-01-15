Позволяет в шаблоне загружать список партнеров в контекстную переменную partners_list

INSTALLED_APPS = (
	...
	'partners',
	...
)

{% load partners_tags %}
{% get_partners_list %}