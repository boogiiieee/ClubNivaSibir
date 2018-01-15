Добавляет в админку модуль конфигурации сайта.

1) settings - 'configuration',
2) url - url(r'^configuration', include('configuration.urls')),
3) syncdb
4) dushboard.py - 
	from configuration.views import ConfigModule
	self.children.append(ConfigModule())
5) 'configuration.context_processors.custom_proc',