
# bt 配置

php项目，然后删除目录的所有文件
启动ssl 访问
1. start 
uwsgi --ini deploy/uwsgi.pid 
service nginx start

2. reload 
uwsgi --reload deploy/uwsgi.pid 
service nginx restart