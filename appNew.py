from flask import Flask,request,make_response,redirect,url_for
from flask import send_file,send_from_directory,render_template,session,flash
from datetime import timedelta
from file_explorer import files
from valid_user import validate_user
import json
import os
import getpass
from valid_user import validate_user
from logger import logger
from werkzeug.utils import secure_filename
from flask_cors import CORS

app=Flask(__name__)
CORS(app,resources={r"/*":{"origins":"*"}})
app.config["SECRET_KEY"]=os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=7)
#session.permanent=True
app.config['upload']=os.getcwd()
logger=logger()
print(os.getcwd())
root=r"C:\Users\%s\Desktop" % getpass.getuser()


@app.route("/")
#@login_required
def hello():
    logger.info("/")
    #session["user"]="liwe"
    files_list=files(root)
    #res=make_response(json.dumps(files_list))
    #res.set_cookie("user",request.form['name'])
    #return json.dumps(files_list)
    return render_template('home.html',path=root,files_list=files_list)

@app.route("/login",methods=['POST'])
def login():
    logger.info("login")
    if(request.method=="GET"):
        return render_template("login.html")

    user=request.form['name']
    pwd=request.form['pwd']
    if(validate_user(user,pwd)):
        msg="Success"
        flash(msg) #消息闪现 falsh message to next request
        #res.set_cookie("username",user)
        return redirect(url_for("hello"))
    else:
        error='Invalid username or password. Please try again.'
        flash(error,category=error)
        return render_template("login.html")



# Get 请求中获取参数方法：folder=request.args.get('folder') 
# POST                  folder=request.form['folder']
@app.route("/nav") 
def navigate():
    logger.info("/nav")
    path=request.args.get('path')
    if(path is None):
        path=root
    if(os.path.isfile(path)):
        #return redirect(url_for('download',file=path)) # 重定向
        return redirect(url_for("view",file=path))
    files_list=files(path)
    #return json.dumps(files_list)
    return render_template("home.html",path=path,files_list=files_list)


@app.route("/download")
def download():
    logger.info("/download")
    fp=request.args.get('file')
    directory=os.path.dirname(fp)
    file=str(fp).split("\\")
    file=file[-1]
    return send_from_directory(directory,file,as_attachment=True)

@app.route("/view")
def view():
    file=request.args.get('file')
    #return send_file(file)
    with open(file,"r",encoding='utf-8') as fs:
        txt=fs.read()
        return render_template("viewcontent.html",file=file,content=txt)
"""
back to parent folder
"""
@app.route("/nav/back",methods=['GET'])
def back():
    parent=os.path.dirname(request.args.get('path'))
    return redirect(url_for("navigate",path=parent))
    

def after_requests(resp):
    resp.headers['Access-Control-Allow-Origin']='*'
    resp.headers['Access-Control-Allow-Methods']='POST,DELETE,PUT,GET'
    """     if(request.method=="OPTIONS"):
        resp. """
   
    return resp
"""
view file content
"""
@app.route("/file",methods=["POST","OPTIONS"])
def file():
    path=request.args['file']
    try:
        fp=open(path,"r")
        content=fp.read()
        fp.close()
        print("reve")
        print(content)
    except IOError:
        return (IOError.strerror)
    return content
   
    
@app.route("/upload",methods=['GET','POST'])
def upload():
    if(request.method=='GET'):
        return render_template("upload.html")
    else:
        f=request.files['file']
        """
        Strange thing:path os.getcwd() points to E: 
        """
        #f.save(os.path.join(os.getcwd(),'/upload/'+secure_filename(f.filename)))
        f.save(os.path.join("E:\\Programming",secure_filename(f.filename)))

@app.route("/set_cookie")
def set_cookie():
    res=make_response("success")
    res.set_cookie("user","li")
    return res

@app.route("/get_cookie")
def get_cookie():
    return make_response(request.cookies.get("li"))

@app.route("/get_session")
def get_session():
    return session.get("li")

#app.after_request(after_requests)
if __name__=="__main__":
    
    #app.run(debug=True,host='0.0.0.0',port=5000)
    app.run(debug=True,host='127.0.0.1',port=5000)