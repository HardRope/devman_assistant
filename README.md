# Devman assistant bot  
This bot helps to group students according with their develop level and temporary opportunities in group projects.  

1. First of all administrator of the project enter all current students, curator and project info in Django admin panel.
2. Every student should choose comfortable timecodes in the bot - time when he would able to take an online meeting with collabours and mentor. 
3. When all students sent their timecodes, curator tap the button to group students with some rules (seniors work only with seniors, highest priority have students who choose only one timecode, group can be from 2 to 3 students).
4. If script think that extra timecodes can make sorting better, it send a request to unsorted students.
5. Curator see preliminary result of sorting students and if averything is okay, tap the "save" button and groups are saved. (after this action there is no way to change groups in telegram, only in django admin panel).
6. Every student can request a call back which (request) will sent to curator.

## install app
clone repo, activate env, make migrations and create superuser:
```
git clone https://github.com/ilyashirko/devman_assistant
cd devman_assistant
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate && python3 manage.py createsuperuser
```
create .env file and write there all necessary data: