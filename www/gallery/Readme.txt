INSTALLED_APPS = (
	...
	'gallery',
	...
)

url(r'^gallery/', include('gallery.urls')),