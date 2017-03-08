from flask import Flask
from flask import request
from sklearn.svm import SVC

app = Flask(__name__)
data = []
results = []


# page for interaction
@app.route('/')
def index():
    return app.send_static_file('index.html')


# gathers data from forms
@app.route('/getData', methods=['POST'])
def getData():
    roadID = request.form['roadID']
    direction = request.form['direction']
    dayOfWeek = request.form['dayOfWeek']
    timeOfDay = request.form['timeOfDay']
    trafficStatus = request.form['trafficStatus']
    data.append([str(roadID), str(direction), str(dayOfWeek), str(timeOfDay)])
    results.append(int(trafficStatus))
    return app.send_static_file('index.html')


# generates a traffic status that is to be expected
@app.route('/status', methods=['POST'])
def status():
    if (len(data) < 2):
        return ("Error. Need to input more predictions.", 400)

    model = SVC(gamma=0.001, C=100.)
    model.fit(data, results)
    roadID = request.form['roadID']
    direction = request.form['direction']
    dayOfWeek = request.form['dayOfWeek']
    timeOfDay = request.form['timeOfDay']
    trafficStatus = model.predict([[str(roadID), str(direction), str(dayOfWeek), str(timeOfDay)]])
    return ("Your Estimated Traffic Status: " + str(trafficStatus), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
