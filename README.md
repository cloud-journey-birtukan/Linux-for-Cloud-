# cloud Backup project
This project contains a script to automate  from cloud server to local machine
##Features
-incremental sync:uses rsync to only transfer changes(delta algorighm)
-Automated(tracks every attempt log with Timestamp)
Headless Execution: designed to run via Crontab for automation
## Prerequsites on both machines
-remote linux server
-ssh key-based authentication
-rsync autonticated on both machines
##Usage
-clone the repo
make script executable using 'chmod +x scripts/backup.sh'
Add to crontab for daily uses using   ex: 0 2 * * * /path/to/scripts/backup.sh  
!!!Donot forget to use the path to the file as  direct access is not possible in crontab!
