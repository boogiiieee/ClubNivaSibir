# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.template import Template, Context

from partners.models import Partner

class PartnerTest(TestCase):
	def setUp(self):
		self.client = Client()
		
	def test1(self):
		username = 'test_user'
		pwd = 'secret'

		self.u = User.objects.create_user(username, '', pwd)
		self.u.is_staff = True
		self.u.is_superuser = True
		self.u.save()

		self.assertTrue(self.client.login(username=username, password=pwd), "Logging in user %s, pwd %s failed." % (username, pwd))
			
		##########################################################################
		##########################################################################
		
		c = 0
		for i in range(2):
			self.assertTrue(Partner.objects.create(title="test %d" % c), "Can not create new row in Partner table.")
			c += 1
			
		out = Template(
			"{% load partners_tags %}"
			"{% get_partners_list %}"
			"{% for p in partners_list %}"
			"{{ p.title }},"
			"{% endfor %}"
		).render(Context())
		self.assertEqual(out, "test 1,test 0,")
			
		##########################################################################
		##########################################################################
		
		self.client.logout()