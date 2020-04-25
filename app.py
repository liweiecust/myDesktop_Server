from flask import Flask,request,make_response,redirect,url_for,send_file,render_template
from file_explorer import files
import json
import os
import getpass
from valid_user import validate_user
from logger import logger

app=Flask(__name__)
logger=logger()

root=r"C:\Users\%s\Desktop" % getpass.getuser()

@app.route("/")
def hello():
    logger.info("/")
    files_list=files(root)
    return json.dumps(files_list)

@app.route("/login",methods=['POST','GET'])
def login():
    logger.info("login")
    if(request.method=="GET"):
        return render_template("login.html")

    user=request.form['name']
    pwd=request.form['pwd']
    if(validate_user(user,pwd)):
        return redirect(url_for("hello"))
    else:
        return render_template("login.html")


# Get 请求中获取参数方法：folder=request.args.get('folder') 
# POST                  folder=request.form['folder']
@app.route("/nav") 
def navigate():
    logger.info("/nav")
    path=request.args.get('path')
    
    if(os.path.isfile(path)):
        return redirect(url_for('download',file=path)) # 重定向
    files_list=files(path)
    return json.dumps(files_list)
"""
@app.route("/nav/<folder>") 
def navigate2(folder):
    path=request.args.get('folder')
    print(path)
    if(os.path.isfile(folder)):
        return redirect(url_for('download')) # 重定向
    files_list=files(folder)
    return json.dumps(files_list)
"""

@app.route("/download")
def download():
    logger.info("/download")
    return send_file(request.args.get('file'))
"""
back to parent folder
"""
@app.route("/nav/back",methods=['POST'])
def back():
    parent=os.path.dirname(request.form['path'])
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
   
    
@app.route("/upload")
def upload():
    return render_template("upload.html")

#app.after_request(after_requests)
if __name__=="__main__":
    app.run(debug=True,port=5000)
   