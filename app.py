from flask import Flask,request,make_response
from file_explorer import files
import json
import os
import getpass


app=Flask(__name__)

root=r"C:\Users\%s\Desktop" % getpass.getuser()

@app.route("/")
def hello():
    print("home")
    files_list=files(root)
    return json.dumps(files_list)

@app.route("/nav")
def navigate():
    path=request.args['path']
    
    files_list=files(path)
    return json.dumps(files_list)

@app.route("/nav/back",methods=['POST','OPTIONS'])
def back():
    parent=os.path.dirname(request.args['path'])
    files_list=files(parent)
    return json.dumps(files_list)

def after_requests(resp):
    resp.headers['Access-Control-Allow-Origin']='*'
    resp.headers['Access-Control-Allow-Methods']='POST,DELETE,PUT,GET'
    """     if(request.method=="OPTIONS"):
        resp. """
   
    return resp

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
   
    


app.after_request(after_requests)
if __name__=="__main__":
    app.run(debug=False,port=5000)
   