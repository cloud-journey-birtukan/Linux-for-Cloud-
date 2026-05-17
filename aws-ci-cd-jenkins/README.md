# AWS EC2 Jenkins CI/CD Pipeline (No-Docker)

This repository contains a basic Python application that monitors log files, paired with a lightweight Jenkins CI/CD pipeline. The goal of this project is to run an automated deployment on a single AWS EC2 instance without using containers (Docker/Kubernetes).
┌─────────────────┐         Webhook         ┌─────────────────┐
│   GitHub Repo   ├────────────────────────►│   Jenkins EC2   │
└─────────────────┘                         └───────┬─────────┘
                                                    │ Deploys
                                                    ▼
                                            ┌─────────────────┐
                                            │ Native Host App │
                                            └─────────────────┘
┌──────────────────────────────────────────────────────────────────────────┐
│                      AWS EC2 NATIVE WORKSPACE RUNTIME                    │
│                                                                          │
│  1. Pull Source ──► 2. Compile Check ──► 3. Fetch Secret ──► 4. Deploy   │
│                                                          │
└──────────────────────────────────────────────┼───────────────────────────┘

                                  Injects Keys │
                               ┌───────────────┴────────────┐
                               │ Jenkins Credentials Plugin  │
                               │ (Masked Secure Vault Store) │
                               └─────────────────────────────┘

## How It Works

The architecture relies on a standard Git-triggered workflow. Instead of shipping container images, Jenkins pulls raw code updates directly into a working directory on the host machine and handles process switching natively.



### Steps in the Process:
1. **Developer Push:** You push code changes to the GitHub repository.
2. **Webhook Trigger:** GitHub sends an automated HTTP POST request to your Jenkins EC2 server port `8080`.
3. **Workspace Preparation:** Jenkins wakes up, pulls down the latest commit, and spins up an isolated local Python virtual environment (`venv`).
4. **Environment Swapping:** Using your secure AWS keys, Jenkins targets the local server runtime, terminates the outdated background execution processes, and starts the new code immediately using `nohup` background tasks.

---

## Secure Credential Handling (No Leaks)

To interact with AWS services without exposing critical account keys to the public, this pipeline abstracts secrets away from the codebase entirely.



* **The Vault:** Raw `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` details are input directly into the Jenkins Web UI under **Manage Jenkins -> Credentials**. They are encrypted and stored inside the private system files of the EC2 instance.
* **The Token Alias:** The `Jenkinsfile` in the repository only references an alias string (like `aws-global-credentials`). 
* **Runtime Injection:** When a build kicks off, the Jenkins AWS Steps plugin temporarily injects the keys into that specific execution pipeline. If the console log tries to print these keys, Jenkins instantly catches them and covers them up as `****`.

---

## Troubleshooting Guide

When setting up a raw, non-containerized pipeline on an EC2 instance, you will likely hit a few common environment bottlenecks. Here is how to fix them:

### 1. Webhook Fails to Trigger Jenkins (Timeout Error)
* **The Symptom:** You push code to GitHub, but Jenkins does absolutely nothing, and GitHub shows a red warning icon next to your webhook.
* **The Cause:** Your AWS EC2 Security Group is blocking incoming traffic from GitHub's IP addresses.
* **The Fix:** Go to your AWS EC2 Console -> Security Groups -> Edit Inbound Rules. Ensure you have opened **Custom TCP Port 8080** to either the general public (`0.0.0.0/0`) or specifically to GitHub's official Webhook IP ranges.

### 2. "pkill: Operation not permitted" or App Fails to Restart
* **The Symptom:** The pipeline script crashes during the deployment stage when trying to kill the old app processes.
* **The Cause:** The `jenkins` system user on Linux doesn't have the permissions required to modify or stop processes started by other system accounts (like `ubuntu` or `root`).
* **The Fix:** Ensure that whatever account originally started the application matches the user running the Jenkins automation agent. If permissions are completely blocked, you may need to grant limited `sudo` access to the `jenkins` user inside the server's `/etc/sudoers` configuration file.

### 3. Port 8000 Already in Use (Address Already Bound)
* **The Symptom:** The pipeline says it completed successfully, but your new app changes aren't showing up, and your logs say `Process already in use`.
* **The Cause:** The previous background application process didn't close properly, meaning it is still sitting on network Port 8000.
* **The Fix:** SSH directly into your EC2 server and find out exactly what process ID (PID) is locking the port by running:
  ```bash
  sudo lsof -i :8000
Once you get the PID number, force it to close manually using:
    sudo kill -9 <PID_NUMBER>
4. "python3: command not found" in Jenkins Console Logs

    The Symptom: The build stage fails instantly with a command missing error.

    The Cause: Jenkins runs as its own isolated system user (jenkins), which often does not share the same system path shortcuts or environment tools as your main login user.

    The Fix: SSH into the machine and make sure Python is installed globally across the whole machine, not just your local account:
     sudo apt install -y python3 python3-venv python3-pip
                          
                                                    













                                                    ▼
                                   
                 
                                         
