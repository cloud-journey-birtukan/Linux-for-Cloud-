       AWS S3 Automated Data pipeline
A robust, fault-tolerant Python utility designed to synchronize local directory assets with S3. it is designed to be cost and time efficient by checking and only uploading the new files, using the concept of multithreading.


 #core features
Parallel Execution: uses ThreadPoolExecutor for concurrent upload, reducing time latency
StateTracking: Implements JSON based tracker to ensure only new or modified files are uploaded saving AWS costs.
Industrial Automation: integrated with systemd services and timers for reliable scheduled execution.
Fault Tolerance:Comprehensive error handling for network interruptions (ClientError) and authentication failures (NoCredentialsError).
Validation Layer: Post-upload verification using S3 Object metadata loading to confirm data integrity.

   Architecture Overview

The pipeline follows a Scan-Filter-Upload-Verify lifecycle:

    1.Scan: Detects all files in a targeted local directory.

    2.Filter: Compares files against the uploaded_metadata.json ledger.

    3.Upload: Distributes new files across worker threads.

    4.Verify: Confirms object existence in S3 before updating the local state.
  
  Tech Stack

    Language: Python 3.12

    Cloud SDK: Boto3 (AWS SDK for Python)

    Environment: Ubuntu 24.04 LTS

    Automation: Systemd (Service & Timer units)

    Libraries: python-dotenv, concurrent.futures, logging
  Installation & Setup
 
 1.Clone & Environment
 2.Configuration (.env)
  Create a .env file in the root directory:to safely include AWS credentilals
 3.Deployment (Systemd)
   To enable daily automation at 2:00 AM:
   Copy s3-uploader.service and s3-uploader.timer to /etc/systemd/system/.
   Reload and enable:
 
 Monitoring

Logs are persisted to /home/birtukan/data_pipeline.log. You can monitor the live ingestion via:
  
 Future Enhancements

    [ ] Add Log Rotation to manage disk space for long-term deployments.

    [ ] Implement MD5 Checksum comparison for deeper file integrity.

    [ ] Add Slack/Discord notifications for failed upload alerts.

 The Launch Checklist

    Permissions: Ensure your user birtukan has access to the directory where the uploaded_metadata.json will be created.

    AWS Policies: Double-check that your IAM user has s3:PutObject, s3:ListBucket, and s3:GetObject permissions for your specific bucket.

    Path Verification: Confirm that /home/birtukan/files_upload actually exists before the first run.

    Dry Run: Run the script manually one time using python3 my1boto3.py just to watch the logs and make sure the first batch uploads correctly.
   GOOD LUCK!!!
