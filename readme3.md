Self-healing web-server
Overview
-Auto-monitoring: checks the health of the server every 60 sec
-Auto recovery: attempts automatic restart incase of server failure
-Alerting: notify's the admin if server failure cannot be recovered automatically

Project components
watcher: a script file for the core monitoring
web-watcher.service : systemd unit for daemon running of script
myserver.log: dedicated file that saves attempts and status

Demonstration
 ensure to make the script executable and move it to /usr/local/bin
   chmod +x watcher
   mv watcher.sh /usr/local/bin/watcher
make sure to create a service file in 
  /etc/systemd/system 
  and the ExecStart pointing to /usr/loca/bin/watcher
  enable and start it sudo systemctl enable web-watcher.service
            sudo systemctl start web-watcher.service
create a log file in /var/log 
To simulate simple failure
   sudo systemctl stop nginx
check the auto recovery:-
   sudo journalctl -u web-watcher.service -f
   cat myserver.log 
To simulate severe failure
   nano /etc/nginx/nginx.conf  and an extra garbage to and save
  sudo systemctl stop nginx 
 check the log file it will be alerting and sending an email  

Note
 use absolute path to commands
eg; /usr/bin/curl
    /bin/systemctl
