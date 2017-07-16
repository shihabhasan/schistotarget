# SchistoTarget: A Highly-Accurate Web Server for Prediction of schistosome immunoreactive proteins

SchistoTarget is implemented in Python and the web-server is freely accessible at http://schistotarget.bioapps.org. Currently local installation is not available. Source code and documentation are available from [GitHub](https://github.com/shihabhasan/SchistoTarget).

SchistoTarget is a supervised machine learning based tool which uses 2 supervised machine learning techniques using Scikit-Learn to discriminate between immunoreactive and non-immunoreactive proteins. These 2 techniques are: 

1. [Gaussian Naive Bayes (GNB)](http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html#sklearn.naive_bayes.GaussianNB)
2. [Passive aggressive](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.PassiveAggressiveClassifier.html#sklearn.linear_model.PassiveAggressiveClassifier)

Generated predictions are stored in a database, which facilitates the rapid reuse of predictions without rerunning the time-consuming machine learning classifications. This saves considerabe runtime if the same sequences are uploaded multiple times, e.g. by different users. SchistoTarget predictions are highly valuable for identifying genes important for host-parasite interaction and the discovery of novel drug and vaccine targets.

## Data & Source Code
The data set can be downloded from [here](http://schistotarget.bioapps.org/static/data.zip) and the source codes of SchistoTarget can be found on [GitHub](https://github.com/shihabhasan/SchistoTarget).

## Input options
SchistoTarget takes the fasta formatted text or file. File extension can be any type (eg. .txt, .fas, .fasta etc.). File extension does not have any effect on SchistoTarget. SchistoTarget can not predict the protein class if the protein sequence is less than 20 amino acids. 

## Output
After completing the task, a result page with a prediction table is appeared. The result is also sent by email if a valid email address is provided during data submission. The prediction table is a list of Sequence ID of test protein sequence, category prediction, score. The methods table is a list of Sequence ID of test protein sequence, name of the machine learning technique, category prediction, decision score and probability. Plots and Charts can be drawn from 'Draw Charts' section. Click on a row of the Prediction table, then click any of the buttons from 'Draw Charts' section to draw plot. 