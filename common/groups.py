import requests
url = "http://172.20.171.232:5001"

@app.route('/group/info')
def register():
    return render_template("form-validation.html")


@app.route('/group/add', methods=["POST", "GET"])
def groupAdd():
    if request.method == "POST":
        result = request.form
        groupname = result["groupname"]
        api = parse.urljoin(url, '/api/v1/groups/%s' % groupname)
        req = requests.post(api)
        print(req.text)
        return render_template("/test/result.html", result=result)

# @app.route('/result',methods=["POST","GET"])
# def result():
#     if request.method == "POST":
#         result = request.form
#         print(result)
#         return render_template("/test/result.html",result=result)