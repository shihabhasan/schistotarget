import os, sys, subprocess
import hashlib, time
sys.path.append('/home/shihab/schistotarget/app')
from django.shortcuts import render_to_response, redirect
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext

from app.immuno_tasks import run_immuno



def index(request):
   return render_to_response('index.html')

def home(request):
   return render_to_response('index.html')

def help(request):
   return render_to_response('help.html')

def contact(request):
   return render_to_response('contact.html', context_instance=RequestContext(request))

def thanks(request):
   name=request.POST['name']
   email=request.POST['email']
   message=request.POST['message']
   command = "echo 'Name: '"+name+"'\nEmail: '"+email+"'\nMessage: '"+message+" | mutt -s 'schistotarget Prediction Query' -- pharm.shihab@gmail.com"
   subprocess.call(command, shell=(sys.platform!="Linux"))
   return render_to_response('thanks.html', { 'name': name })

#-----------IMMUNOREACTIVITY PREDICTION-----------------------------

def immuno_app(request):
   return render_to_response('immuno_app.html', context_instance=RequestContext(request))
	
def immuno_predict(request):
   immuno_email=request.POST['input_email'].replace(" ","")
   if request.POST['input_sequences'].replace(" ","")!="":
      filename="test_"+hashlib.md5(time.asctime()).hexdigest()
      file_in=open(filename, 'w')
      file_in.write(request.POST['input_sequences'].replace(" >",">"))
      file_in.close()
   else:
      file = request.FILES['input_file']
      filename = file.name+"_"+hashlib.md5(time.asctime()).hexdigest()
      destination=open(filename,'wb+')
      for chunk in file.chunks():
         destination.write(chunk)
   task=run_surface.delay(filename, immuno_email)
   task_id=task.id
   return HttpResponseRedirect('/immuno_progress/'+task_id, { 'task_id': task_id })

def immuno_progress(request, task_id):
   result = run_surface.AsyncResult(task_id)
   while not  result.ready():
      return render_to_response('progress.html', { 'task_id': task_id })
   return HttpResponseRedirect('/immuno_results/'+task_id, { 'task_id': task_id })
   
def immuno_results(request, task_id):
   result = run_surface.AsyncResult(task_id)
   result_data=result.get()
   prediction_lines, header, lines, x1, x2, x3, fh, fd = result_data
   return render_to_response('result.html', { 'predict_result': prediction_lines, 'header':header, 'all_predictions': lines, 'x1': x1, 'x2': x2, 'x3': x3, 'fh':fh, 'fd':fd })


#-----------IgE PREDICTION-----------------------------

def IgE_app(request):
   return render_to_response('IgE_app.html', context_instance=RequestContext(request))
	
def IgE_predict(request):
   IgE_email=request.POST['input_email'].replace(" ","")
   if request.POST['input_sequences'].replace(" ","")!="":
      filename="test_"+hashlib.md5(time.asctime()).hexdigest()
      file_in=open(filename, 'w')
      file_in.write(request.POST['input_sequences'].replace(" >",">"))
      file_in.close()
   else:
      file = request.FILES['input_file']
      filename = file.name+"_"+hashlib.md5(time.asctime()).hexdigest()
      destination=open(filename,'wb+')
      for chunk in file.chunks():
         destination.write(chunk)
   task=run_surface.delay(filename, IgE_email)
   task_id=task.id
   return HttpResponseRedirect('/IgE_progress/'+task_id, { 'task_id': task_id })

def IgE_progress(request, task_id):
   result = run_surface.AsyncResult(task_id)
   while not  result.ready():
      return render_to_response('progress.html', { 'task_id': task_id })
   return HttpResponseRedirect('/IgE_results/'+task_id, { 'task_id': task_id })
   
def IgE_results(request, task_id):
   result = run_surface.AsyncResult(task_id)
   result_data=result.get()
   prediction_lines, header, lines, x1, x2, x3, fh, fd = result_data
   return render_to_response('result.html', { 'predict_result': prediction_lines, 'header':header, 'all_predictions': lines, 'x1': x1, 'x2': x2, 'x3': x3, 'fh':fh, 'fd':fd })

#-----------IgG1 PREDICTION-----------------------------

def IgG1_app(request):
   return render_to_response('IgG1_app.html', context_instance=RequestContext(request))
	
def IgG1_predict(request):
   IgG1_email=request.POST['input_email'].replace(" ","")
   if request.POST['input_sequences'].replace(" ","")!="":
      filename="test_"+hashlib.md5(time.asctime()).hexdigest()
      file_in=open(filename, 'w')
      file_in.write(request.POST['input_sequences'].replace(" >",">"))
      file_in.close()
   else:
      file = request.FILES['input_file']
      filename = file.name+"_"+hashlib.md5(time.asctime()).hexdigest()
      destination=open(filename,'wb+')
      for chunk in file.chunks():
         destination.write(chunk)
   task=run_surface.delay(filename, IgG1_email)
   task_id=task.id
   return HttpResponseRedirect('/IgG1_progress/'+task_id, { 'task_id': task_id })

def IgG1_progress(request, task_id):
   result = run_surface.AsyncResult(task_id)
   while not  result.ready():
      return render_to_response('progress.html', { 'task_id': task_id })
   return HttpResponseRedirect('/IgG1_results/'+task_id, { 'task_id': task_id })
   
def IgG1_results(request, task_id):
   result = run_surface.AsyncResult(task_id)
   result_data=result.get()
   prediction_lines, header, lines, x1, x2, x3, fh, fd = result_data
   return render_to_response('result.html', { 'predict_result': prediction_lines, 'header':header, 'all_predictions': lines, 'x1': x1, 'x2': x2, 'x3': x3, 'fh':fh, 'fd':fd })



#-----------IgG3 PREDICTION-----------------------------

def IgG3_app(request):
   return render_to_response('IgG3_app.html', context_instance=RequestContext(request))
	
def IgG3_predict(request):
   IgG3_email=request.POST['input_email'].replace(" ","")
   if request.POST['input_sequences'].replace(" ","")!="":
      filename="test_"+hashlib.md5(time.asctime()).hexdigest()
      file_in=open(filename, 'w')
      file_in.write(request.POST['input_sequences'].replace(" >",">"))
      file_in.close()
   else:
      file = request.FILES['input_file']
      filename = file.name+"_"+hashlib.md5(time.asctime()).hexdigest()
      destination=open(filename,'wb+')
      for chunk in file.chunks():
         destination.write(chunk)
   task=run_surface.delay(filename, IgG3_email)
   task_id=task.id
   return HttpResponseRedirect('/IgG3_progress/'+task_id, { 'task_id': task_id })

def IgG3_progress(request, task_id):
   result = run_surface.AsyncResult(task_id)
   while not  result.ready():
      return render_to_response('progress.html', { 'task_id': task_id })
   return HttpResponseRedirect('/IgG3_results/'+task_id, { 'task_id': task_id })
   
def IgG3_results(request, task_id):
   result = run_surface.AsyncResult(task_id)
   result_data=result.get()
   prediction_lines, header, lines, x1, x2, x3, fh, fd = result_data
   return render_to_response('result.html', { 'predict_result': prediction_lines, 'header':header, 'all_predictions': lines, 'x1': x1, 'x2': x2, 'x3': x3, 'fh':fh, 'fd':fd })


#-----------IgG4 PREDICTION-----------------------------

def IgG4_app(request):
   return render_to_response('IgG4_app.html', context_instance=RequestContext(request))
	
def IgG4_predict(request):
   IgG4_email=request.POST['input_email'].replace(" ","")
   if request.POST['input_sequences'].replace(" ","")!="":
      filename="test_"+hashlib.md5(time.asctime()).hexdigest()
      file_in=open(filename, 'w')
      file_in.write(request.POST['input_sequences'].replace(" >",">"))
      file_in.close()
   else:
      file = request.FILES['input_file']
      filename = file.name+"_"+hashlib.md5(time.asctime()).hexdigest()
      destination=open(filename,'wb+')
      for chunk in file.chunks():
         destination.write(chunk)
   task=run_surface.delay(filename, IgG4_email)
   task_id=task.id
   return HttpResponseRedirect('/IgG4_progress/'+task_id, { 'task_id': task_id })

def IgG4_progress(request, task_id):
   result = run_surface.AsyncResult(task_id)
   while not  result.ready():
      return render_to_response('progress.html', { 'task_id': task_id })
   return HttpResponseRedirect('/IgG4_results/'+task_id, { 'task_id': task_id })
   
def IgG4_results(request, task_id):
   result = run_surface.AsyncResult(task_id)
   result_data=result.get()
   prediction_lines, header, lines, x1, x2, x3, fh, fd = result_data
   return render_to_response('result.html', { 'predict_result': prediction_lines, 'header':header, 'all_predictions': lines, 'x1': x1, 'x2': x2, 'x3': x3, 'fh':fh, 'fd':fd })


#-----------ERROR HANDLER-----------------------------

def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


















