from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, Response, flash, redirect, url_for
import json
from .auth.auth import AuthError, requires_auth
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lornaolum:abc@localhost/blog'
db = SQLAlchemy(app)
CORS(app)
#setting up model
class Blog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    feature = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    thumbnail = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'Blog: (self.description)'

    def __init__(self, description, title, feature, image, thumbnail):
        self.description = description
        self.title = title
        self.feature = feature
        self.image = image
        self.thumbnail = thumbnail



#members API route



def format_blog(blog):
    return{
       " description": blog.description,
       "id": blog.id,
       "title": blog.title,
       "feature": blog.feature,
       "image": blog.image,
       "thumbnail": blog.thumbnail

    }


@app.route('/blogs', methods=['GET'])
def blogs():
    contents = Blog.query.all()
    content_list= []
    for content in contents:
        content_list.append(formated_blog(content))
    token = get_token_auth_header()
    payload = verify_decode_jwt(token)
    check_permissions(permission, payload)
    return{ "contents": content_list}


@app.route('/blogs/<id>', methods=['GET'])
def get_one(id):
    content = Blog.query.filter_by(id=id).one
    formatted_blog = format_blog(content)
    
    return {"content": formatted_blog}



@app.route('/blogs', methods=['POST'])
def create_blog():
    try:
        new_blog = blogs(new_description=request.json('description'),
                         new_title=request.json('title'),
                         new_feature=request.json('feature'),
                         new_image=request.json('image'),
                         new_thumbnail=request.json('thumbnail'))
        
        db.session.add(new_blog)
        db.session.commit()
        token = get_token_auth_header()
        payload = verify_decode_jwt(token)
        check_permissions(permission, payload)
    except:
        db.session.rollback()
        flash('An error occurred. blog ' + new_description + ' could not be listed.')
            
    finally:
        db.session.close()
        flash('Blog ' + request.json['blog_id'] + ' was successfully listed!')
        return format_blog(new_blog)
  
# takes values from the json submitted, and update existing
@app.route('/blogs/<int:blog_id>/edit', methods=['POST'])
def edit_blog(blog_id):
    try:   
        blog = request.json.get()
        new_blog_id = request.json('blog_id')
        db.session.add(new_blog_id)
        db.session.commit()
    except:
           db.session.rollback()
    finally:
           db.session.close()
  
    return format_blog(new_blog_id)



@app.route('/blogs/<blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    
    try:
       Blog.query.filter_by(id=blog_id).delete()

       token = get_token_auth_header()
       payload = verify_decode_jwt(token)
       check_permissions(permission, payload)
       db.session.commit()
       
    except Exception as e:
        print('error')
  
    finally:
         db.session.close()
       
         return { 'success': True }

@app.route('/blogs/<int:blog_id>', methods=['UPDATE'])
def update_blog(blog_id):
    content = Blog.query.filter_by(id=id)
    new_blog = blog(new_blog_id=request.json('blog_id'), 
                        new_description=request.json('description'),
                        new_title=request.json('title'),
                        new_feature=request.json('feature'),
                        new_image=request.json('image'),
                        new_thumbnail=request.json('thumbnail'))

    content.update(dict(new_blog = blog))

    token = get_token_auth_header()
    payload = verify_decode_jwt(token)
    check_permissions(permission, payload)
    db.session.commit()
    return {"content": formatted_blog(content.one)}


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')




@app.route("/blog")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}



if __name__=="__main__":
    app.run(debug=True)