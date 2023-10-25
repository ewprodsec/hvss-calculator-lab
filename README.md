# hvss-calculator-lab
This is the Healthcare Vulnerability Scoring System Calculator (HVSS) Machine Learning Training Lab

## Introduction
The HVSS Calculator is using AI/ML models trained to predict the risk score for each of the four impact types independintly.

There are five different models get created by the lab, on separate files:

- **XCIA Model (xcia_model.pkl)**: Predicts the risk score for the XCIA (original CIA) impact type
- **XPS Model (xps_model.pkl)**: Predicts the risk score for the XPS (parient safety) impact type
- **XSD Model (xsd_model.pkl)**: Predicts the risk score for the XSD (sensitive data breach) impact type
- **XHB Model (xhb_model.pkl)**: Predicts the risk score for the XHB (hospital breach) impact type
- **Expolitability Model (exploitability_model.pkl)**: Predicts the risk score only for the Expolitability ingredient

### Notice
The score prediction for each impact type is considering the values of the exploitability values & specific impact values as a single value set. However, for learning purposes we are also producing an individual model only for the expolitability part, so you can learn how the expolitabilty part affects the overall scoring.

## How to use the lab
The lab is based on Jupyter Notebook for running the python code. Should you be new to Jupyter Notebook, please consider reading the formal intro documentation to get you in quickly. There are also plenty of tutorials around the internet which you may find useful.

- Jupyter Notebook can be installed from here: https://jupyter.org/install
- Intro docs for Jupyter Notebook can be found here: https://docs.jupyter.org/en/latest

There are two labs available, and you can select each of them according to your preferences:

- ```HVSS Score Lab (full training data without test set).ipynb```: This lab is skipping the usage of test sets (i.e., no MSE validation is available), and instead uses the full training data available to train the models.
- ```HVSS Score Lab (with test set).ipynb```: This lab includes a test step of the models' accuracy (MSE) using test sets, which are taken out of the training data.

### What lab should I choose?
Great question. It is a common practice on AI/ML model engineering to use test sets for the evaluation of model accuracy using Mean Squared Error (MSE). However, the test sets are taken out of the training set, leaving relativley small-sized training data for the HVSS models - which in turn affects the model accuracy, becuase we are missing data which the algorithm can learn from. In observation we made, we discovered that using the ```HVSS Score Lab (full training data without test set).ipynb``` lab produces higher quality models. But if you want to go traditional, or in case you are largely extending your training set, then for sure consider using the ```HVSS Score Lab (with test set).ipynb``` file.

### What python version should I use?
We successfully ran the labs with python 3.11, however it is possible that earlier versions will work as well.

### Preparing the lab environment
Beside of Jupyter Notebook installation, you should also install the external python libraries which the labs are using (pandas, scikit-learn, and others). To do so, please run the following command from the root folder: 

```pip install -r requirements.txt```

### Testing the models
Congratulations! You successfully created the models, and they are now located under the ```models``` folder. But, how can you test it?
For this we also created ```hvss-cli.py```, a simple python CLI applciation which you can find under the ```test``` folder. Just run the file and play with the various options to get risk scores. ***Remember to install the requirements.txt file before running the CLI app!***

## Acknowledgments
This project was originally created by the HVSS Working Group, founded by the Product Security Team of [Edwards Lifesciences](https://www.edwards.com):
- Oleg Yusim
- Roman Ivanenko
- Tejas Bharambe
- Jacob Barkai
- Samuel Takachicha
- Aleksey Haytman
- Isaias Rivera
- Maddy Tamilthurai
- Vinitha Mathiyazhagan

## Good luck and happy modeling!
