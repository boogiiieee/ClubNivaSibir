Чистит лишние файлы, сессии, кэш, каптчи, превьюшки, водяные знаки

INSTALLED_APPS = (
	...
	'cleaner',
	...
)

CLEANER_APPS = (
	'banners',
	'news',
	'gallery',
)

manage.py cleaner_start