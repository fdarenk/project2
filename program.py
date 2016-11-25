from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
import json

def create_datafile():
        datafile = open('data.txt', 'w', encoding = 'UTF-8')
        fieldsfile = open('fields.txt', 'r', encoding = 'UTF-8')
        datafile.write('name\tgender\tage')
        for l in fieldsfile.readlines():
                units = l.strip('\n').split('\t')
                datafile.write('\t' + units[1])
        datafile.write('\n')
        fieldsfile.close()
        datafile.close()

def get_data():
        datafile = open('data.txt', 'r', encoding = 'UTF-8')
        data = []
        i=0
        for l in datafile.readlines():
                i += 1
                if i > 1:
                        line = l.strip('\n').split('\t')
                        data.append(line)
        datafile.close()
        return data

def get_fields():
        fieldsfile = open('fields.txt', 'r', encoding = 'UTF-8')
        fields = []
        for l in fieldsfile.readlines():
                line = l.strip('\n').split('\t')
                fields.append(line[1])
        fieldsfile.close()
        return fields

app = Flask(__name__)
@app.route('/')
def page():
        if request.args:
                datafile = open('data.txt', 'a', encoding = 'UTF-8')
                datafile.write(request.args['name'] + '\t' + request.args['gender'] + '\t' + request.args['age'])
                for f in get_fields():
                        datafile.write('\t' + request.args[f])
                datafile.write('\n')
                datafile.close()
        fieldsfile = open('fields.txt', encoding = 'UTF-8')
        fields = {}
        for l in fieldsfile.readlines():
                units = l.strip('\n').split('\t')
                fields[units[0]]=units[1]
        fieldsfile.close()
        return render_template('form.html', fields = fields)

@app.route('/stats')
def stats():
        data = get_data()
        if data:
                average = get_average(data)
                genders = get_genders(data)
                answers = get_answers(data)
                return render_template('stats.html', average = average, genders = genders, answers = answers)
        else:
                return render_template('nostats.html')

@app.route('/search')
def search():
        return render_template('search.html')

@app.route('/results')
def resultspage():
        name = request.args['name']
        fields = get_fields()
        data = get_data()
        length = len(data[0])
        found = []
        appear = 0
        for resp in data:
                if resp[0] == name:
                        appear = 1
                        found.append(resp)
        if appear == 1:
                return render_template('results.html', found = found, name = name, fields = fields, length = length)
        if appear == 0:
                return render_template('noresults.html', name = name)

@app.route('/json')
def jsonpage():
        datafile = open('data.txt', 'r', encoding = 'UTF-8')
        data = []
        for l in datafile.readlines():
                line = l.strip('\n').split('\t')
                data.append(line)
        datafile.close()
        jsonstr = json.dumps(data, Ensure_ascii=False)
        return render_template('json.html', jsonstr = jsonstr)

def get_answers(data):
        answers = []
        for numquest in range(3, (len(data[0]))):
                quest_n = []
                for resp in data:
                        appear = 0
                        for ans in quest_n:
                                if ans[1] == resp[numquest]:
                                        ans[0] += 1
                                        appear = 1
                        if appear == 0:
                               quest_n.append([1, resp[numquest]])
                question = [get_fields()[numquest - 3], sorted(quest_n)]
                answers.append(question)
        return answers

def get_average(data):
        summ = 0
        for resp in data:
                summ += int(resp[2])
        summ = summ/(len(data))
        return summ

def get_genders(data):
        men = 0
        women = 0
        for resp in data:
                if resp[1] == 'м':
                        men += 1
                else:
                        women +=1
        genders = str(men) + ' : ' + str(women)
        return genders

def main():
        create_datafile()

if __name__ == '__main__':
        main()
        app.run()
