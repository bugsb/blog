from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =     db.Column(db.String(100),nullable=False)
    content =   db.Column(db.Text,nullable=False)
    author =    db.Column(db.String(20),nullable=False,default='N/A')

    def __repr__(self):
        return 'Blog Post' + str(self.id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts',methods=['POST','GET'])
def posts():
    if request.method=='POST':
        postTitle = request.form['title']
        postContent = request.form['content']
        newPost = Blog(title=postTitle, content=postContent,author='Mani')
        db.session.add(newPost)
        db.session.commit()
        return redirect('/posts')
    else:
        allPost = Blog.query.order_by('title').all()
        return render_template('posts.html',posts=allPost)

@app.route('/posts/update/<int:id>',methods=['GET','POST'])
def update(id):
    allPost = Blog.query.get_or_404(id)
    if request.method=='POST':
        allPost.title = request.form['title']
        allPost.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('update.html',post=allPost)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = Blog.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/new',methods=['POST','GET'])
def newPost():
    if request.method=='POST':
        postTitle = request.form['title']
        postContent = request.form['content']
        newPost = Blog(title=postTitle, content=postContent,author='Mani')
        db.session.add(newPost)
        db.session.commit()
        return redirect('/posts')
    else:
        allPost = Blog.query.order_by('title').all()
        return render_template('newPost.html',posts=allPost)



if __name__ == "__main__":
    app.run(debug=True)
