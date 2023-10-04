nohup sshpass -p "rNTUTstudent1!" scp cybertec_V3_pg_12.conf root@192.168.78.161:postgresql.conf 
nohup sshpass -p "rNTUTstudent1!" ssh root@192.168.78.161 "cp ~/postgresql.conf /var/lib/pgsql/data/postgresql.conf" 
nohup sshpass -p "rNTUTstudent1!" ssh root@192.168.78.161 "systemctl restart postgresql.service"
sleep 10
echo change complete!
