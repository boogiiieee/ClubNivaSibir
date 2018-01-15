from forum.models import Thread, Post
from django.utils.translation import ugettext as _
from django.template import Library, Node, TemplateSyntaxError, Variable, resolve_variable
import re
register = Library()

def bbcode(value):
	bbdata = [
		(r'\[url\](.+?)\[/url\]', r'<a href="\1">\1</a>'),
		(r'\[url=(.+?)\](.+?)\[/url\]', r'<a href="\1">\2</a>'),
		(r'\[email\](.+?)\[/email\]', r'<a href="mailto:\1">\1</a>'),
		(r'\[email=(.+?)\](.+?)\[/email\]', r'<a href="mailto:\1">\2</a>'),
		(r'\[img\](.+?)\[/img\]', r'<img src="\1">'),
		(r'\[img=(.+?)\](.+?)\[/img\]', r'<img src="\1" alt="\2">'),
		(r'\[b\](.+?)\[/b\]', r'<b>\1</b>'),
		(r'\[i\](.+?)\[/i\]', r'<i>\1</i>'),
		(r'\[u\](.+?)\[/u\]', r'<u>\1</u>'),
		(r'\[quote\](.+?)\[/quote\]', r'<div style="margin-left: 1cm">\1</div>'),
		(r'\[center\](.+?)\[/center\]', r'<div align="center">\1</div>'),
		(r'\[code\](.+?)\[/code\]', r'<tt>\1</tt>'),
		(r'\[big\](.+?)\[/big\]', r'<big>\1</big>'),
		(r'\[small\](.+?)\[/small\]', r'<small>\1</small>'),
		(r'\[br\]', r'<br/>'),
		]

	for bbset in bbdata:
		p = re.compile(bbset[0], re.DOTALL)
		value = p.sub(bbset[1], value)

	#The following two code parts handle the more complex list statements
	temp = ''
	p = re.compile(r'\[list\](.+?)\[/list\]', re.DOTALL)
	m = p.search(value)
	if m:
		items = re.split(re.escape('[*]'), m.group(1))
		for i in items[1:]:
			temp = temp + '<li>' + i + '</li>'
		value = p.sub(r'<ul>'+temp+'</ul>', value)

	temp = ''
	p = re.compile(r'\[list=(.)\](.+?)\[/list\]', re.DOTALL)
	m = p.search(value)
	if m:
		items = re.split(re.escape('[*]'), m.group(2))
		for i in items[1:]:
			temp = temp + '<li>' + i + '</li>'
		value = p.sub(r'<ol type=\1>'+temp+'</ol>', value)

	return value
register.filter(bbcode)

def forum_latest_thread_activity(parser, token):
    """
    {% forum_latest_thread_activity [number] as [context_var] %}
    """
    bits = token.contents.split()
    if len(bits) not in (1, 2, 4):
        raise TemplateSyntaxError('%s tag requires none, one or three arguments' % bits[0])
    if bits[2] != 'as':
        raise TemplateSyntaxError("Second argument to %s tag must be 'as'" % bits[0])
    if not bits[1]:
        bits[1] = 5 # Default number of items
    if not bits[3]:
        bits[3] = 'latest_thread_activity'
    return ForumLatestThreadsNode(bits[1], bits[3])

class ForumLatestThreadsNode(Node):
    def __init__(self, number, context_var):
        self.number = int(number) - 1
        self.context_var = context_var
    
    def render(self, context):
        context[self.context_var] = Thread.objects.select_related().order_by('-latest_post_time')[:self.number]
        return ''

def forum_latest_posts(parser, token):
    """
    {% forum_latest_posts [number] as [context_var] %}
    """
    bits = token.contents.split()
    if len(bits) not in (1, 2, 4):
        raise TemplateSyntaxError('%s tag requires none, one or three arguments' % bits[0])
    if bits[2] != 'as':
        raise TemplateSyntaxError("Second argument to %s tag must be 'as'" % bits[0])
    if not bits[1]:
        bits[1] = 5 # Default number of items
    if not bits[3]:
        bits[3] = 'latest_posts'
    return ForumLatestPostsNode(bits[1], bits[3])

class ForumLatestPostsNode(Node):
    def __init__(self, number, context_var):
        self.number = int(number) - 1
        self.context_var = context_var
    
    def render(self, context):
        context[self.context_var] = Post.objects.select_related().order_by('-time')[:self.number]
        return ''


def forum_latest_user_posts(parser, token):
    """
    {% forum_latest_user_posts user [number] as [context_var] %}
    """
    bits = token.contents.split()
    if len(bits) not in (2, 3, 5):
        raise TemplateSyntaxError('%s tag requires one, two or four arguments' % bits[0])
    if bits[3] != 'as':
        raise TemplateSyntaxError("Second argument to %s tag must be 'as'" % bits[0])
    if not bits[2]:
        bits[2] = 5 # Default number of items
    if not bits[3]:
        bits[4] = 'latest_user_posts'
    return ForumLatestUserPostsNode(bits[1], bits[2], bits[4])

class ForumLatestUserPostsNode(Node):
    def __init__(self, user, number, context_var):
        self.user = Variable(user)
        self.number = int(number) - 1
        self.context_var = context_var
    
    def render(self, context):
        user = self.user.resolve(context)
        context[self.context_var] = Post.objects.select_related().filter(author=user).order_by('-time')[:self.number]
        return ''

register.tag('forum_latest_posts', forum_latest_posts)
register.tag('forum_latest_thread_activity', forum_latest_thread_activity)
register.tag('forum_latest_user_posts', forum_latest_user_posts)



