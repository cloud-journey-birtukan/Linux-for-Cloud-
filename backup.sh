#!/bin/bash
#these are enviromental variables for the sake of security
USER = "${REMOTE_USER:-ubuntu}"
IP ="${REMOTE_IP:-1.2.3.4}"
DIR="${REMOTE_DIR:-/var/www/html/}"
DEST ="$HOME/backups/cloudsync"
LOG_FILE="$(dirname "$0")/../logs/backup.log"
TIMESTAMP=$(date "+%Y-%m-%d  %H:%M:%S")

echo "$TIMESTAMP starting to sync from  $IP..." >> "$LOG_FILE"

#check if destination exists
mkdir -p "$DEST"

rsync -avz "$USER@IP:DIR" "$DEST" >> "$LOG_FILE" 2>&1

if [$? -eq 0]; then
	echo "$TIMESTAMP SUCCESS:file synched to $DEST" >>"$LOG_FILE"
else
	echo "$TIMESTAMP ERROR:file synch failed" >>"$LOG_FILE"
fi

