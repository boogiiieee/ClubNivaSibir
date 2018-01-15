INSTALLED_APPS = (
	...
	'news',
	...
)

url(r'^news/', include('news.urls')),

CACHE_BACKEND = 'dummy:///'