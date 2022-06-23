from flask import render_template,url_for,request,redirect,Blueprint,abort
from flask_login import current_user,login_required
from blogSite import db
from blogSite.models import BlogPost
from blogSite.blog_posts.forms import BlogPostForms

blog_posts = Blueprint('blog_posts',__name__)

#for creating blogs
@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
	form = BlogPostForms()

	if request.method == 'POST':
		if request.form.get('action') == 'value':
			blog_post = BlogPost(title = form.title.data,
				text = form.text.data,
				user_id = current_user.id)
			db.session.add(blog_post)
			db.session.commit()
			return redirect(url_for('core.index'))
	return render_template('create_post.html',form=form)

#for viewing blogs
@blog_posts.route('/<int:blog_post_id>',methods=['GET','POST'])
def blog_post(blog_post_id):
	blog_post = BlogPost.query.get_or_404(blog_post_id)

	form = BlogPostForms()
	if request.method == 'POST':
		if request.form.get('action') == 'value':
			blog_post.title = form.title.data
			blog_post.text = form.text.data
			db.session.commit()
			return redirect(url_for('blog_posts.blog_post',blog_post_id=blog_post_id))

	elif request.method == 'GET':
		form.title.data = blog_post.title
		form.text.data = blog_post.text

	
	return render_template('blog_post.html',form=form,title=blog_post.title,date = blog_post.date,post = blog_post)	

@blog_posts.route('/<int:blog_post_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(blog_post_id):
	blog_post = BlogPost.query.get_or_404(blog_post_id)
	if blog_post.author != current_user:
		abort(403)

	db.session.delete(blog_post)
	db.session.commit()
	return redirect(url_for('core.index'))