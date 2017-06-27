from __future__ import absolute_import
from celery import task
import sys
sys.path.append('/home/shihab/schistotarget/scripts/moreConservative')
sys.path.append('/home/shihab/schistotarget/scripts/lessConservative')
sys.path.append('/home/shihab/schistotarget/scripts/featuresPrediction')
from .immunoMoreConservativeTasks import run_immuno_more_conservative
from .immunoLessConservativeTasks import run_immuno_less_conservative
from .featureTasks import run_features


#---------------------IMMUNO BACKGROUND TASK------------------
@task
def run_immuno(filename, immuno_email, feature_mode):
    task_id = run_immuno.request.id
    if feature_mode=="lessConservative":
        result = run_immuno_less_conservative(filename, immuno_email, feature_mode, task_id)
    if feature_mode=="moreConservative":
        result = run_immuno_more_conservative(filename, immuno_email, feature_mode, task_id)
    return result


#---------------------FEATURES PREDICTION BACKGROUND TASK------------------
@task
def run_features_predict(filename, feature_email, features_list):
    task_id = run_features.request.id
    result = run_features(filename, feature_email, features_list, task_id)
    return result