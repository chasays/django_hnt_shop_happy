
## bt setup 

- select PHP project, and delete the whole the files
- go to setting, and config SSL ,apply ssl-license and confirm
- config nginx profile, copy nginx.ini's content to nginx, then restart nginx

please enjoy it ~
thanks qingbc~

## 1. start 
uwsgi --ini deploy/uwsgi.pid 
service nginx start

## 2. reload 
uwsgi --reload deploy/uwsgi.pid 
service nginx restart