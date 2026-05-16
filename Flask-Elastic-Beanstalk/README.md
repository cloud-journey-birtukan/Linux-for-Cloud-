☁️ What is PaaS (Platform as a Service)?
Platform as a Service (PaaS) is a cloud computing model that provides developers with a complete platform — hardware, software, and infrastructure — to build, run, and manage applications without dealing with the complexity of the underlying infrastructure.

┌────────────────────────────────────────────┐
│              SaaS (Software)               │  ← You use the app
│         Gmail, Salesforce, Slack           │
├────────────────────────────────────────────┤
│             PaaS (Platform)  ← YOU ARE HERE│  ← You write & deploy code
│    AWS Elastic Beanstalk, Heroku, GCP      │
│    App Engine, Azure App Service           │
├────────────────────────────────────────────┤
│         IaaS (Infrastructure)              │  ← You manage servers
│    AWS EC2, Azure VMs, Google Compute      │
├────────────────────────────────────────────┤
│     On-Premises (Traditional)              │  ← You own everything
│    Your own data center & hardware         │
└────────────────────────────────────────────┘

AWS Elastic Beanstalk — PaaS in Practice
Elastic Beanstalk is AWS's PaaS offering. Under the hood, it automatically provisions and manages:

Developer Machine
      │
      │  git push / eb deploy
      ▼
┌─────────────────┐        ┌──────────────────────────┐
│  AWS CodeBuild  │───────▶│   AWS Elastic Beanstalk  │
│  (CI Pipeline)  │  build │                          │
│  buildspec.yml  │ & test │  ┌──────────────────────┐│
└─────────────────┘        │  │   EC2 Instance(s)    ││
                           │  │   └── Flask App      ││
                           │  └──────────────────────┘│
                           │         ▲                 │
                           │  Load Balancer            │
                           │         │                 │
                           └─────────┼─────────────────┘
                                     │
                               End Users 🌐




✅ Prerequisites
Before you begin, ensure you have the following installed and configured:

 Python 3.8+
 AWS CLI — Install guide
 AWS EB CLI — installed via requirements.txt in this project
 AWS Account with IAM permissions for Elastic Beanstalk and CodeBuild
 Git

Configure your AWS credentials before proceeding:
aws configure
# Enter: AWS Access Key ID, Secret Access Key, region (us-east-1), output format (json)

flask-continuous-delivery/
├── application.py          # Main Flask application (EB expects this name)
├── requirements.txt        # Python dependencies (includes awsebcli)
├── Makefile                # Build automation: install, lint, test
├── buildspec.yml           # AWS CodeBuild pipeline definition
├── .elasticbeanstalk/
│   └── config.yml          # EB CLI configuration (auto-generated)
├── tests/
│   └── test_app.py         # Unit tests
└── README.md               # This file
# Create a virtual environment in your home directory
python3 -m venv ~/.eb

# Activate it (Linux/macOS)
source ~/.eb/bin/activate

# Your prompt should now show (.eb) indicating the venv is active
# (.eb) $
B. Install Dependencies
With your virtual environment active, use make to install all dependencies defined in requirements.txt:
make all
install:
    pip install --upgrade pip && pip install -r requirements.txt

lint:
    pylint --disable=R,C application.py

test:
    python -m pytest tests/ -v

all: install lint test
C. Initialize EB Application
Initialize a new Elastic Beanstalk application in the current directory:
eb init -p python-3.8 flask-continuous-delivery --region us-east-1
Optional — Set up SSH key pair for instance access:
eb init
# Follow the prompts and select "Yes" when asked to set up SSH
D. Create Remote EB Instance
Provision and launch your cloud environment:
   eb create flask-continuous-delivery-env
This single command will:

Create an EC2 instance running Amazon Linux with Python 3.7
Set up an Elastic Load Balancer
Configure an Auto Scaling Group
Deploy your Flask application
Return a public URL for your app


⏳ This typically takes 3–5 minutes on first run.

Once complete, open your app in the browser:
   eb open
   eb status
   eb health

🔧 Troubleshooting
eb command not found after make all

Make sure your virtual environment is active: source ~/.eb/bin/activate

Deployment fails with "application not found"

Elastic Beanstalk expects your Flask app object to be named application. Check your entry point file: application = Flask(__name__)

CodeBuild can't deploy to EB

Ensure your CodeBuild IAM role has the AWSElasticBeanstalkFullAccess policy attached.

Environment health is "Degraded"

Run eb logs to inspect application errors. The most common cause is a missing dependency in requirements.txt
