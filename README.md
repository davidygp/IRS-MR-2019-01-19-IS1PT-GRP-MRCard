# SECTION 1 : PROJECT TITLE
### MRCard Recommender System

# SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT
With the income of working adults in singapore steadily rising over the years, many people are gaining access to credit cards, especially young working adults. The majority of adults nowadays own at least one or more credit cards, with many others planning to start using credit cards as well. Banks have also been actively coming up with more credit cards and trying and to get consumers to take them up. 

There can be many advantages in having a credit card. One advantage is that credit card users can earn benefits in terms of rebates, air miles, and rewards. This is usually the main draw for people to use credit cards. However, not every card is suitable for everyone. Each card has its own requirements and rates, and whether the user can earn the benefits from the card largely depends on their lifestyle and spending habits. With many credit cards available from the banks in Singapore, it can be a time-consuming task to pick up a suitable credit card, and many people simply get cards where their potential benefits are not maximised.

As a group of 5 young working professionals, we felt that this was a very relevant issue. Hence, we came up with the idea of designing a recommendation system to recommend the most suitable credit card or saving account based on the applicant's personal background, spending habits and personal preferences.

For this project, we first set out to perform knowledge acquisition by interviewing a subject matter expert, and also conducting a survey. To build the system, we decided to utilise the Django web framework, for its ease of integration with the front-end user interface (done with HTML), and the back-end rules engine (PyKnow) that we used to perform rule-based reasoning.

Our team learned a lot in the process of working on this project. We got the chance to apply techniques (like knowledge acquisition and rule-based reasoning) that we learned in our lectures and workshops in a viable business application scenario, and also picked up technical skills which would surely prove useful in the future course of our work.

# SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name | Student ID (MTech Applicable)| Work Items (Who Did What) | Email (Optional) |
| :---: | :---: | :---: | :---: |
| LI DUO  | A0195364W | asdfasdfa | e0384995@u.nus.edu |
| LIM CHONG SENG HERMANN | A0195392U | asfasf | e0385023@u.nus.edu |
| LU JIAHAO | A0091835Y | asdfasf | e0384293@u.nus.edu |
| YAM GUI PENG DAVID | A0195315A | asfasf | e0384946@u.nus.edu |
| ZHAO YAZHI | A0195305E | ASDFASD | e0384936@u.nus.edu |

# SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO
Sudoku AI Solver

Note: It is not mandatory for every project member to appear in video presentation; Presentation by one project member is acceptable. More reference video presentations here

# SECTION 5 : USER GUIDE
<Github File Link> : https://github.com/telescopeuser/Workshop-Project-Submission-Template/blob/master/UserGuide/User%20Guide%20HDB-BTO.pdf

[ 1 ] To run the system using iss-vm
download pre-built virtual machine from http://bit.ly/iss-vm

start iss-vm

open terminal in iss-vm

$ git clone https://github.com/telescopeuser/Workshop-Project-Submission-Template.git

$ source activate iss-env-py2

(iss-env-py2) $ cd Workshop-Project-Submission-Template/SystemCode/clips

(iss-env-py2) $ python app.py

Go to URL using web browser http://0.0.0.0:5000 or http://127.0.0.1:5000

[ 2 ] To run the system in other/local machine:
Install additional necessary libraries. This application works in python 2 only.
$ sudo apt-get install python-clips clips build-essential libssl-dev libffi-dev python-dev python-pip

$ pip install pyclips flask flask-socketio eventlet simplejson pandas

# SECTION 6 : PROJECT REPORT / PAPER
<Github File Link>  https://github.com/telescopeuser/Workshop-Project-Submission-Template/blob/master/ProjectReport/Project%20Report%20HDB-BTO.pdf

Recommended Sections for Project Report / Paper:

+ Executive Summary / Paper Abstract
+ Business Problem Background
+ Project Objectives & Success Measurements
+ Project Solution (To detail domain modelling & system design.)
+ Project Implementation (To detail system development & testing approach.)
+ Project Performance & Validation (To prove project objectives are met.)
+ Project Conclusions: Findings & Recommendation
+ List of Abbreviations (if applicable)
+ References (if applicable)

# SECTION 7 : MISCELLANEOUS
HDB_BTO_SURVEY.xlsx
Results of survey
Insights derived, which were subsequently used in our system
