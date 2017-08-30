from google.appengine.ext import ndb

class CommentsData(ndb.Model):
    comment_string = ndb.StringProperty(repeated=True)
    comment_page_id = ndb.IntegerProperty()

# The blog post class
class BlogPost:
    def __init__ (self, title, content, image):
        self.title = title
        self.content = content
        self.image = image

    def listString(self, page_id):
        return '<a href="view-post?page_id=' + str(page_id) + '">' + self.title + '</a>'

    def commentsAsHTML(self, page_id, new_comment):
        comments_query = CommentsData.query(CommentsData.comment_page_id == page_id)
        comments_data = comments_query.get()
        if comments_data == None:
            if new_comment == None:
                return '<p>No comments yet.</p>'
            else:
                comment_list = [ new_comment ]
                comments_data = CommentsData(comment_page_id = page_id,
                                            comment_string = comment_list)
                comments_data.put()
                return '<p>' + new_comment + '</p>'
        else:
            if new_comment != None:
                comments_data.comment_string.append(new_comment)
            html_string = ''
            for comment in comments_data.comment_string:
                html_string += '<p>' + comment + '</p>'
            if new_comment != None:
                comments_data.put()
            return html_string

blog_list = [
    BlogPost(
    'About Me',
    'Hello! My name is Aljon Pineda. ' +
    'I am 17 years old, turning 18 in August. ' +
    'I recently graduated from Meadowcreek High School, ' +
    'and I will be attending Georgia Tech and majoring in Computer Science. ' +
    'I have one younger sister who is 16 right now.',
    'aljon.PNG'
    ),
    BlogPost(
    'What I Do in My Free Time',
    'In my free time, my favorite thing to do is play ' +
    'video games with my friends. Whenever I have the chance, ' +
    'I would play my favorite game, Overwatch. What I also ' +
    'love to do is read books, especially the detective ' +
    'fiction genre. Recently, I got into the interest ' +
    'of writing my own detective fiction book.',
    'overwatch.jpg'
    )
]
