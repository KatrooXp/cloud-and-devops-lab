## Gitlab task

### Using the curl utility, write REST API requests

- creating a new project in a group

![Alt text](<pictures/Screenshot from 2023-08-09 20-27-03.png>)    

- project deletion/migration

![Alt text](<pictures/Screenshot from 2023-08-09 22-57-09.png>)

![Alt text](<pictures/Screenshot from 2023-08-09 23-10-08.png>)

- adding users to a project/group with different roles

![Alt text](<pictures/Screenshot from 2023-08-21 11-11-14.png>)

- getting a branch list

![Alt text](<pictures/Screenshot from 2023-08-21 11-35-44.png>)

- getting list of merged branches

![Alt text](<pictures/Screenshot from 2023-08-21 11-41-32.png>)

- get a list of tags

![Alt text](<pictures/Screenshot from 2023-08-21 11-50-47.png>)

- create an issue and assign it to a specific user

![Alt text](<pictures/Screenshot from 2023-08-21 12-05-45.png>)

- branch creation with issue identifier

    first, get the issue id, than create a branch, name starting with this iid

![Alt text](<pictures/Screenshot from 2023-08-21 15-08-46.png>)
![Alt text](<pictures/Screenshot from 2023-08-21 14-53-54.png>)

- creating a branch merge request

![Alt text](<pictures/Screenshot from 2023-08-21 16-11-44.png>)

- request for confirmation of branch merge with/without branch deletion

![Alt text](<pictures/Screenshot from 2023-08-21 16-37-53.png>)

- tag on commit after merge

![Alt text](<pictures/Screenshot from 2023-08-21 16-50-32.png>)

- user list retrieval
    - the whole

![Alt text](<pictures/Screenshot from 2023-08-21 17-16-44.png>)

    - з певними правами
    
![Alt text](<pictures/Screenshot from 2023-08-22 11-24-16.png>)

- commit handling
    - get a list of all commit comments in the merge request

![Alt text](<pictures/Screenshot from 2023-08-22 12-15-15.png>)

    - вставити коментар у commit у певний рядок від імені користувача

![Alt text](<pictures/Screenshot from 2023-08-22 13-11-19.png>)

### Написати скрипти на bash і *Python, параметри повинні передаватися з командного рядка (name_of_project, email_of_member, role, name_of_issue, content_of_issue and etc.):

    please, see the file gitlab_task.sh

a) створити новий проект із заданим ім'ям у певній групі;

![Alt text](<pictures/Screenshot from 2023-08-25 16-59-27.png>)

b) додати/видалити/змінити роль користувача на проекті;

![Alt text](<pictures/Screenshot from 2023-08-25 17-02-00.png>)

c) створити/видалити/змінити набір лейблів (bug, DEV_env, DEV_env, QA_env, PROD_env, task) для певного проєкту;

![Alt text](<pictures/Screenshot from 2023-08-25 17-06-01.png>)

d) створити issue (опис, label) для певного користувача, до певної дати і призначити тег (див.). Якщо label не існує, то створити. If milestone does not exist, then it should be created.

![Alt text](<pictures/Screenshot from 2023-08-25 17-07-36.png>)

e) Find all actually marge request and create list of problem line. One record of list must consist from: date_time, name_file, number_line, author, description. Proposed use the Linux command printf

![Alt text](<pictures/Screenshot from 2023-08-25 16-57-46.png>)



