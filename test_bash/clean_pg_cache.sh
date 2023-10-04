systemctl stop postgresql.service
sync
echo '3' | sudo /usr/bin/tee -a /proc/sys/vm/drop_caches
systemctl start postgresql.service
service tomcat9 restart