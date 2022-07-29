import demjson
from flask import Flask, render_template, request,redirect

import requests
from urllib import parse
import json
app = Flask(__name__)

url = "http://localhost:5001"

@app.route('/group/info')
def register():
    return render_template("group-info.html")


@app.route('/group/list')
def groupList():
    api=parse.urljoin(url, '/api/v1/groups')
    req=requests.get(api)
    groupInfo=demjson.decode(req.text)
    if groupInfo['status']=='OK':
        groups=groupInfo['data']['groups']
    return render_template("group-list.html",result=groups)

@app.route('/group/add', methods=["POST", "GET"])
def groupAdd():
    if request.method == "POST":
        result = request.form
        print(result)
        groupname = result["groupname"]
        api = parse.urljoin(url, '/api/v1/groups/%s' % groupname)
        req = requests.post(api)
        print(req.text)
        return redirect('/group/list')

@app.route('/group/control', methods=["POST"])
def groupControl():
    result = request.form
    if result.get('delete'):
        groupname = result["delete"]
        api = parse.urljoin(url, '/api/v1/groups/%s' % groupname)
        req = requests.delete(api)
        print(req.text)
        return redirect('/group/list')
    elif result.get('edit'):
        groupname = result["edit"]
        api = parse.urljoin(url, '/api/v1/groups/%s' % groupname)
        req = requests.get(api)
        result=demjson.decode(req.text)
        members=result['data']['members']
        if len(members)==0:
            hostList=''
        else:
            hostList=','.join(members).replace(',','\n')
        context={'groupname':groupname,'hostList':hostList} 
        print(context)
        return render_template("host-info.html",**context)

@app.route('/host/info', methods=["POST", "GET"])
def hostInfo():
    if request.method == "POST":
        result = request.form
        print(result)
        hosts = result["hosts"]
        groupname=result['groupname']
        groupVars={"ansible_ssh_user":result["ansible_ssh_user"],"ansible_ssh_pass":result["ansible_ssh_pass"]}
        api = parse.urljoin(url, '/api/v1/groupvars/%s' % groupname)
        headers = {"Content-Type": "application/json"}
        req=requests.post(api,data=json.dumps(groupVars),headers=headers)
        print(req.text)
        api = parse.urljoin(url, '/api/v1/groups/%s' % groupname)
        req = requests.delete(api)
        api = parse.urljoin(url, '/api/v1/groups/%s' % groupname)
        req = requests.post(api)
        for i in hosts.split('\n'):
            host=i
            api = parse.urljoin(url, '/api/v1/hosts/%s/groups/%s' % (host,groupname))
            req = requests.post(api)
        return redirect('/group/list')
@app.route('/task/mysql', methods=["POST", "GET"])
def taskMysql():
    return render_template("task-mysql.html")


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=8080, debug=True)
