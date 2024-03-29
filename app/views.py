import os, sys, subprocess
import hashlib, time
sys.path.append('/home/shihab/schistotarget/app')
from django.shortcuts import render_to_response, redirect
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext

from app.tasks import run_immuno, run_features_predict



def home(request):
   return render_to_response('index.html')

def manual(request):
    return render_to_response('help.html')

def forum(request):
    return render_to_response('forum.html')

def contact(request):
   return render_to_response('contact.html', context_instance=RequestContext(request))

def thanks(request):
   name=request.POST['name']
   email=request.POST['email']
   message=request.POST['message']
   command = "echo 'Name: '"+name+"'\nEmail: '"+email+"'\nMessage: '"+message+" | mutt -s 'SchistoTarget Prediction Query' -- pharm.shihab@gmail.com"
   subprocess.call(command, shell=(sys.platform!="Linux"))
   return render_to_response('thanks.html', { 'name': name })

#-----------IMMUNOREACTIVITY PREDICTION-----------------------------

def immuno_app(request):
   return render_to_response('immuno_app.html', context_instance=RequestContext(request))
	
def immuno_predict(request):
   if str(request.POST.get('input_sequences')).replace(" ", "") == "" and str(
           request.POST.get('input_file')).replace(" ", "") == "":
      message = "Enter either fasta sequences in text area or upload fasta file!!!"
      return render_to_response('immuno_app.html', {'message': message}, context_instance=RequestContext(request))

   feature_mode = request.POST.getlist('featureMode')
   if len(feature_mode) > 0:
      feature_mode = 'moreConservative'
   else:
      feature_mode = 'lessConservative'

   input_email=request.POST['input_email'].replace(" ","")
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
   task=run_immuno.delay(filename, input_email, feature_mode)
   task_id=task.id
   return HttpResponseRedirect('/immuno_progress/'+task_id, { 'task_id': task_id })

def immuno_progress(request, task_id):
   result = run_immuno.AsyncResult(task_id)
   while not  result.ready():
      return render_to_response('immuno_progress.html', { 'task_id': task_id })
   return HttpResponseRedirect('/immuno_results/'+task_id, { 'task_id': task_id })
   
def immuno_results(request, task_id):
   result = run_immuno.AsyncResult(task_id)
   result_data=result.get()
   prediction_lines, header, lines, x1, x2, x3, fh, fd, feature_mode, json_ids, feature_cutoff = result_data
   return render_to_response('immuno_result.html',
                             {'immuno_result': prediction_lines, 'header': header, 'all_predictions': lines, 'x1': x1,
                              'x2': x2, 'x3': x3, 'fh': fh, 'fd': fd, 'feature_mode': feature_mode,
                              'json_ids': json_ids, 'feature_cutoff': feature_cutoff})


#-----------FEATURES PREDICTION-----------------------------

def feature_app(request):
   return render_to_response('feature_app.html', context_instance=RequestContext(request))


def feature_predict(request):
   if str(request.POST.get('feature_sequences')).replace(" ", "") == "" and str(
           request.POST.get('feature_file')).replace(" ", "") == "":
      message = "Enter either fasta sequences in text area or upload fasta file!!!"
      return render_to_response('feature_app.html', {'message': message}, context_instance=RequestContext(request))
   features_list = request.POST.getlist('featuresBox')
   feature_email = request.POST['feature_email'].replace(" ", "")
   if request.POST['feature_sequences'].replace(" ", "") != "":
      filename = "test_" + hashlib.md5(time.asctime()).hexdigest()
      file_in = open(filename, 'w')
      file_in.write(request.POST['feature_sequences'].replace(" >", ">"))
      file_in.close()
   else:
      file = request.FILES['feature_file']
      filename = file.name + "_" + hashlib.md5(time.asctime()).hexdigest()
      destination = open(filename, 'wb+')
      for chunk in file.chunks():
         destination.write(chunk)
   task = run_features_predict.delay(filename, feature_email, features_list)
   task_id = task.id
   return HttpResponseRedirect('/feature_progress/' + task_id, {'task_id': task_id})


def feature_progress(request, task_id):
   result = run_features_predict.AsyncResult(task_id)
   while not result.ready():
      return render_to_response('feature_progress.html', {'task_id': task_id})
   return HttpResponseRedirect('/feature_results/' + task_id, {'task_id': task_id})


def feature_results(request, task_id):
   result = run_features_predict.AsyncResult(task_id)
   result_data = result.get()
   fh, fd = result_data
   return render_to_response('feature_result.html', {'fh': fh, 'fd': fd})


#-----------ERROR HANDLER-----------------------------

def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


















