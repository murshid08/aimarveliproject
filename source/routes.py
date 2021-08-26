from source.models import Post, User
from flask import redirect,render_template,url_for,request
from source import app,bcrypt,db
from source.forms import RegisterForm,LoginForm,PostForm
from flask_login import current_user,login_user,logout_user,login_required



@app.route('/home')
def home():
    page=request.args.get('page',1,type=int)
    posts=Post.query.order_by(Post.category.desc()).paginate(page=page,per_page=5)
    return render_template('home.html',posts=posts)

@app.route('/',methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('post'))
    form=RegisterForm()
    if form.validate_on_submit():
        hashed=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(email=form.email.data,password=hashed)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("register.html",form=form,title="Register")


@app.route('/login',methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('post'))
    form=LoginForm()
    user=User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password,form.password.data):
        login_user(user)
        return redirect(url_for('post'))

    
    return render_template('login.html',form=form,title="login")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/post/new',methods=["GET","POST"])
@login_required
def post():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(category=form.category.data,cat_fields=form.cat_fields.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('post.html',form=form,title='new post',legend='new post')


@app.route('/post/<int:post_id>/')
def user (post_id):
    posts=Post.query.get_or_404(post_id)
    return render_template('postint.html', title=post.title, posts=posts)

@app.route('/post/int:post_id/update')
def update(post_id):
    posts=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.category=form.category.data
        post.cat_fields-form.cat_fields.data
        return redirect(url_for('user',post_id=post.id))
    elif request.method == 'GET':
        form.category.data = post.category
        form.cat_fields.data = post.cat_fields
    return render_template('updatepost.html', title='Update Post',
                           form=form) 


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))   
