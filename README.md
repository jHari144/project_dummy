# project_dummy
## usage

use the following steps to create the database\
`psql -d postgres`\
once in the `postgres` database\
`CREATE DATABASE dummy;`\
`CREATE USER myuser WITH PASSWORD 'mypass';`\
`ALTER USER myuser WITH SUPERUSER;`\
use the following steps to run the server\
assuming that you've installes django  
p.s. be in the root directory i.e., `project_dummy` not `project_dummy/project_dummy`  
  
`python3 manage.py makemigrations  
python3 manage.py migrate  
python3 manage.py runserver`  

you can use only the last step to runserver from the second time. this is for the first time only.
