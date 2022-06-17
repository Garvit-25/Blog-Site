from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user,current_user,logout_user,login_required
from blogSite import db
from blogSite.models import User,BlogPost
from blogSite.users.forms import SignupForm,LoginForm,UpdateUserForm
from blogSite.users.picture_handler import add_profile_pic

users = Blueprint('users',__name__)

@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('core.index'))

@users.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
	    return redirect(url_for('core.index'))

	form = LoginForm()
	if request.method == 'POST':
		if request.form.get('user') == 'user_login':
			user = User.query.filter_by(email=form.email.data).first()
			if user is not None and user.check_password(form.password.data):
				login_user(user)

				next = request.args.get('next')
				if next==None or not next[0]=='/':
					next = url_for('core.index')

				return redirect(next)
	return render_template('login.html',form=form)

@users.route('/signup',methods=['GET','POST'])
def signup():
	form = SignupForm()

	if request.method == 'POST':
		if request.form.get('action') == 'value':
			user = User(email=form.email.data,
			username = form.username.data,
			password = form.password.data)

		db.session.add(user)
		db.session.commit()
		return redirect(url_for('users.login'))
	return render_template('signup.html',form=form)

@users.route('/account',methods=['GET','POST'])
@login_required
def account():
	form = UpdateUserForm()

	if request.method=='POST':
		if request.form.get('update_value') == 'update':
			pic = current_user.profile_image
			
			if form.picture.data:
				username = current_user.username
				pic = add_profile_pic(form.picture.data,username)
				current_user.profile_image = pic

			current_user.username = form.username.data
			current_user.email = form.email.data
			
			#num = User.query.filter_by(id=current_user.id).update(dict(username=form.username.data,email=form.email.data,profile_image=pic))
			
			db.session.commit()
			return redirect(url_for('users.account'))

	elif request.method =='GET':
		form.username.data = current_user.username
		form.email.data = current_user.email

	profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
	return render_template('account.html',profile_image=profile_image,form=form)

@users.route("/<username>")
def user_posts(username):
	page = request.args.get('page',1,type=int)
	user = User.query.filter_by(username=username).first_or_404()
	blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
	return render_template('user_blog_posts.html',blog_posts=blog_posts,user=user)	
