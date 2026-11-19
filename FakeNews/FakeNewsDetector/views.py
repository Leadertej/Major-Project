from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from textblob import TextBlob
import re
import nltk


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
        return render(request, 'Login.html', {})

def UploadNews(request):
    if request.method == 'GET':
        return render(request, 'UploadNews.html', {})

def AdminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('t1', '')
        password = request.POST.get('t2', '')
        if username == 'admin' and password == 'admin':
            context = {'data': 'Welcome ' + username}
            return render(request, 'AdminScreen.html', context)
        else:
            context = {'data': 'Login failed'}
            return render(request, 'Login.html', context)

def UploadNewsDocument(request):
    if request.method == 'POST' and request.FILES.get('t1'):
        myfile = request.FILES['t1']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        request.session['uploaded_file_name'] = fs.path(filename)
        context = {'data': myfile.name + ' news document loaded'}
        return render(request, 'UploadNews.html', context)
    else:
        return render(request, 'UploadNews.html', {'data': 'No file uploaded.'})


def getQuotes(paragraph):
    score = 0
    matches = re.findall(r'(?:"(.*?)")', paragraph)
    if matches:
        score = len(matches)
    return score

def checkVerb(paragraph):
    score = 0
    b = TextBlob(paragraph)
    for word, tag in b.tags:
        if tag in ['VBG', 'VBN', 'VBP', 'VBD']:
            score += 1
    return score

def nameEntities(paragraph):
    score = 0
    for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(paragraph))):
        if hasattr(chunk, 'label'):
            score += 1
    return score

def naiveBayes(quotes_score, verb_score, entity_score, paragraph):
    total_words = len(nltk.word_tokenize(paragraph))
    if total_words == 0:
        return 0
    return (quotes_score + verb_score + entity_score) / total_words * 10

def DetectorAlgorithm(request):
    file_path = request.session.get('uploaded_file_name', None)
    if not file_path:
        return render(request, 'UploadNews.html', {'data': 'No file has been uploaded yet.'})

    strdata = '<table border=1 align=center width=100%><tr><th>News Text</th><th>Classifier Detection Result</th><th>Fake Rank Score</th></tr>'
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                quotes_score = getQuotes(line)
                verb_score = checkVerb(line)
                entity_score = nameEntities(line)
                score = naiveBayes(quotes_score, verb_score, entity_score, line)
                label = 'Real News' if score > 0.90 else 'Fake News'
                strdata += f'<tr><td>{line}</td><td>{label}</td><td>{score:.2f}</td></tr>'
        strdata += '</table>'
        return render(request, 'ViewFakeNewsDetector.html', {'data': strdata})
    except FileNotFoundError:
        return render(request, 'UploadNews.html', {'data': 'Uploaded file not found. Please re-upload.'})
