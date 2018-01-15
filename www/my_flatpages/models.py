from django.db import models
from django.contrib.sites.models import Site
from tinymce import models as TinymceField
from django.utils.translation import ugettext_lazy as _

#######################################################################################################################
#######################################################################################################################

class FlatPage(models.Model):
	url = models.CharField(_('URL'), max_length=100, db_index=True)
	title = models.CharField(_('title'), max_length=500)
	content = TinymceField.HTMLField(_('content'), blank=True)
	enable_comments = models.BooleanField(_('enable comments'))
	template_name = models.CharField(_('template name'), max_length=70, blank=True,
		help_text=_("Example: 'flatpages/contact_page.html'. If this isn't provided, the system will use 'flatpages/default.html'."))
	registration_required = models.BooleanField(_('registration required'), help_text=_("If this is checked, only logged-in users will be able to view the page."))
	sites = models.ManyToManyField(Site, verbose_name=_('sites'))

	description = models.TextField(_('description'), blank=True)
	keywords = models.TextField(_('keywords'), blank=True)

	class Meta:
		db_table = 'django_flatpage'
		verbose_name = _('flat page')
		verbose_name_plural = _('flat pages')
		ordering = ('title',)
		
	def get_title(self): return self.title
	def get_content(self): return self.content
	def get_description(self): return self.description
	def get_keywords(self): return self.keywords

	def __unicode__(self):
		return u"%s -- %s" % (self.url, self.get_title())

	def get_absolute_url(self):
		return self.url
		
#######################################################################################################################
#######################################################################################################################