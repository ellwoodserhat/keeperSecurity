# Python API Testing Framework with Encryption

## Overview
This is a modular and reusable API testing framework built using Python. It is designed for testing public APIs like ReqRes using:

- **requests** — for making HTTP requests
- **pytest** — for writing test cases
- **pytest-html** — for generating HTML reports
- **pycryptodome** — for AES encryption of request and response bodies
- **GitHub Actions** — for CI/CD automation

## Features
- Reusable CRUD operation method supporting GET, POST, PUT, DELETE
- Parameterized test cases for flexibility and coverage
- AES encryption for request/response payloads to align with cybersecurity best practices
- CI pipeline with GitHub Actions for automated testing
- HTML test report generation with detailed results

## Project Structure
project_root/
├── api_testing/
│ ├── data_provider.py # Parameterized test data for CRUD operations
│ └── test_users.py # Parameterized test cases covering all scenarios
├── configuration/ # configuration directory
│ └── config.py # Configuration (base URL and encryption key)
├── utilities/ # utilities directory
│ ├── httpReq.py # Generic, reusable CRUD request method
│ └── utils.py # AES encrypt/decrypt helpers
├── reports/ # HTML test report output directory
├── .github/
│ └── workflows/
│ └── ci.yml # CI pipeline configuration for GitHub Actions
├── requirements.txt # Python dependencies
├── run_tests.py # Test runner script
└── README.md


## Setup Instructions
1. **Clone the Repository:**
```bash
git clone <your-repo-url>
cd project_root

Install Dependencies:
pip install -r requirements.txt

Run Tests Locally:
run run_tests.py

View Test Report:
Open reports/index.html in your browser.



How It Works
Each test uses the request() method in client.py to avoid duplication.

Test methods like test_create_user() and test_update_user() use pytest.mark.parametrize to inject dynamic test values from data_provider.py.

All request and response payloads can be optionally encrypted using encrypt_data() and decrypt_data() in utils.py.

The framework covers all CRUD operations, negative tests, data validation, response time assertions, and performance testing via concurrency.

How to Run Your Tests on GitHub Actions and Check Results
1. Push Your Code to GitHub
Make sure your full project—including your test files and the GitHub Actions workflow file .github/workflows/ci.yml—is committed and pushed to your repository’s master branch:
git add .
git commit -m "Add tests and CI workflow"
git push origin main

2. Trigger the GitHub Actions Workflow
Once you push to the branch monitored by your workflow (master), GitHub automatically triggers the workflow defined in .github/workflows/ci.yml. This will:
Checkout your code
Setup Python environment
Install dependencies
Run your tests
Generate test reports
Upload artifacts 

3. Check the Workflow Run
Go to your GitHub repository page in a web browser
Click the Actions tab at the top
You will see a list of recent workflow runs triggered by pushes or pull requests
Click the most recent run to see details

4. View Step Logs
Inside the workflow run page, each job and step is shown
Click on the Test to view the logs for the test execution
Here you can see which tests passed, failed, or errored, and detailed error messages if any

5. Download and View Test Reports
Workflow uploads a test report as an artifact (like an HTML report):
On the workflow run page, scroll down to the Artifacts section
Click on the artifact (test-report) to download it
Open the downloaded index.html in your browser to view a detailed, nicely formatted report of your test results

