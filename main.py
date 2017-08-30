import jinja2
import os
import webapp2
import sys

sys.path.append('source/')
from blogpost import BlogPost
from blogpost import blog_list

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'))

# This function creates the table of contents
# It makes:
# <ol>
#   <li><a href="view-post?page_id=(i)">{{ title }}</a></li>
# </ol>
def constructBlogListHTML():
    html_string = '<ol>\n'
    for i in range(0, len(blog_list)):
        blog_post = blog_list[i]
        html_string += '<li>' + blog_post.listString(i) + '</li>'
    html_string += '</ol>'
    return html_string

# The class for viewing the home page (the table of contents)
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('index.html')
        template_variables = {'table_of_contents': constructBlogListHTML()}
        self.response.out.write(template.render(template_variables))

# The class for viewing blog posts
class ViewPostHandler(webapp2.RequestHandler):
    def get(self):
        page_id = int(self.request.get('page_id'))
        self.sendResponse(page_id, None)

    def post(self):
        page_id = int(self.request.get('page_id'))
        self.sendResponse(page_id, self.request.get('comment'))

    def sendResponse(self, page_id, new_comment):
        template = env.get_template('blogpost.html')
        blog_post = blog_list[page_id]
        commentHTML = blog_post.commentsAsHTML(page_id, new_comment)
        template_variables = {
            'title': blog_post.title,
            'content': blog_post.content,
            'image': blog_post.image,
            'comments': commentHTML
        }
        self.response.out.write(template.render(template_variables))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/view-post', ViewPostHandler)
], debug=True)
