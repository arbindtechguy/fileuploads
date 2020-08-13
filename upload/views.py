from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
import os
import glob
import shutil


# Create your views here.
def index(request):
    return render(request, 'upload/index.html')

def handleUpload(request):
    print(request.GET)
    file = request.FILES['file']
    parts = request.POST.get('parts')
    if parts == '':
        parts = 10
    parts = int(parts)
    try:
        handle_uploaded_file(file, parts)
        messages.add_message(request, messages.SUCCESS, 'ファイルが正常にアップロードされました。')
    except:
        messages.add_message(request, messages.WARNING, 'ファイルのアップロード中に問題が発生しました。もう一度お試しください。')
    return redirect('index')

def handle_uploaded_file(f, parts):
    parts = parts -1
    projDir = os.path.dirname(__file__)
    tmpDir = projDir + '/videos/' + "tmp." + f.name
    size = int(f.size / parts)

    if (os.path.isdir(tmpDir)):
        os.stat(tmpDir)
        continue_upload(tmpDir, size, parts, f);
    else:
        os.mkdir(tmpDir)
        n = 1
        for chunk in f.chunks(size):
            dest = tmpDir + "/" + str(n)
            with open(dest, 'wb+') as dest: 
                dest.write(chunk)
            n = n + 1
    mergeFiles(tmpDir, f.name)

def continue_upload(tmpDir, size, parts, f):
    n = 1
    oldFiles = glob.glob(tmpDir + "/*" );

    for uploadChunk in f.chunks(size):
        dest = tmpDir + "/" + str(n)

        # ファイルが存在し、有効な場合はスキップします
        if(os.path.isfile(dest) and os.path.getsize(dest) == size):
            print("==============*** skip:" + oldFiles[n-1] + "***====================")
            n = n + 1
            continue
        
        # 古い破損したファイル削除する
        if(os.path.isfile(dest)):
            os.remove(dest)

        # 残りのファイルの追加
        with open(dest, 'wb+') as dest:
            dest.write(uploadChunk)
            n = n + 1

def mergeFiles(oldDir, fileName):
    print(oldDir, fileName)
    projDir = os.path.dirname(__file__)
    saveDir = projDir + '/videos/' + fileName
    datas = sorted(glob.glob(oldDir + "/*"), key=os.path.getmtime)
    with open(saveDir , 'wb+') as destination:
        for chunk in datas:
            with open(chunk, 'rb') as f:
                destination.write(f.read())

def gallery(request):
    folder = os.path.dirname(__file__) + '/videos/' 
    files = glob.glob(folder + "*.*")
    return render(request, 'upload/gallery.html', {'files': files});

def clearGallery(request):
    folder = os.path.dirname(__file__) + '/videos/'
    datas = glob.glob(folder + "/*")
    for file_path in datas:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    messages.add_message(request, messages.SUCCESS, 'すべてのファイルが正常に削除されました。')
    return redirect('index')