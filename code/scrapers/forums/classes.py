# generic class for thread for all forums
class Thread():
	def __init__(self, url, title='sample title', content='', views=0, comments=0, created_by='sample user', date='00-00-00'):
		self.title = title
		self.content = content
		self.views = views
		self.date = date
		self.url = url
		self.created_by = created_by
		self.comments = comments

	def to_dict(self):
		return {
		'url' : self.url,
		'title' : self.title,
		'content' : self.content,
		'views' : self.views,
		'comments' : self.comments,
		'created_by' : self.created_by,
		'date' : self.date
		}