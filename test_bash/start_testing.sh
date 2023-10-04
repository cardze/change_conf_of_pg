sleepTime=120
user=root
user_passwd="rNTUTstudent1!"
server_ip=192.168.78.161

sshpass -p ${user_passwd} ssh ${user}@${server_ip} "sudo reboot"
echo Server rebooted
echo
    sleep ${sleepTime}
echo Setting started
./change_pg12_conf.sh
# sshpass -p ${user_passwd} ssh ${user}@${server_ip} "sudo systemctl stop munin.timer & sudo service munin-node stop & sudo service munin stop & sudo service munin-asyncd stop"
# nohup sshpass -p ${user_passwd} ssh ${user}@${server_ip} "firewall-cmd --add-port=4444/tcp & ./ServerAgent-2.2.3/startAgent.sh > /dev/null"