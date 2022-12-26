# generic class for thread for all forums
class Thread():
	def __init__(self, url, title='sample title', content='', views=0, comments=0, username='sample user', user_id = '000',
		user_url = '', date='00-00-00',forum='', thread_id=000):
		self.title = title
		self.content = content
		self.views = views
		self.date = date
		self.url = url
		self.username = username
		self.user_id = user_id
		self.user_url = user_url
		self.comments = comments
		self.thread_id = thread_id
		self.forum = forum

	def to_dict(self):
		return {
		'thread_id' : self.thread_id,
		'forum' : self.forum,
		'title' : self.title,
		'content' : self.content,
		'views' : self.views,
		'comments' : self.comments,
		'url' : self.url,
		'username' : self.username,
		'user_id' : self.user_id,
		'user_url' : self.user_url,
		'date' : self.date
		}

# generic class for comments of all forums
class Comment():
	def __init__(self, content='', comment_id=000, username='sample user', user_url='', user_id = '000', date='00-00-00', forum='',
		thread_id=000, thread_url=''):
		self.content = content
		self.date = date
		self.thread_url = thread_url
		self.thread_id = thread_id
		self.username = username
		self.user_id = user_id
		self.user_url = user_url
		self.comment_id = comment_id
		self.forum = forum

	def to_dict(self):
		return{
		'date' : self.date,
		'thread_url' : self.thread_url,
		'thread_id' : self.thread_id,
		'content' : self.content,
		'username' : self.username,
		'user_id' : self.user_id,
		'user_url' : self.user_url,
		'comment_id' : self.comment_id,
		'forum' : self.forum
		}