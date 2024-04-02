
# Flask Wiki Search Engine README

This Flask web application is a simple search engine that allows users to search for information in Wikipedia via a script hosted in an EC2 instance. Once a search is completed, the query and result are cached in a mysql database within a Docker container hosted from a VM on the host machine. The database is searched for a previous query prior to the execution of the Wikipedia search on the EC2 instance to speed up results. 


# Flask Search Engine README

This Flask web application serves as a simple search engine that allows users to search for information stored remotely on an EC2 instance or fetch cached results from a MySQL database.

## Prerequisites
You will need to set up and Amazon EC2 instance and an Ubuntu Virtual Machine (VM) on your host machine.
Some useful resources:
- https://www.youtube.com/watch?v=osqZnijkhtE (EC2)
- https://www.youtube.com/watch?v=O19mv1pe76M (Ubuntu VM)

Within the VM, you will need to set up a docker container with mysql installs. See:
- https://www.youtube.com/watch?v=U0paw01g_KU (docker on Ubuntu)


Before running the application, make sure you have the following installed on your host, on the EC2 instance and on the Ubuntu VM. 

- Python 3
- Flask
- Paramiko
- mysql-connector-python

## Installation

1. Clone this repository to your local machine:

    ```
    git clone https://github.com/your-repo/flask-search-engine.git
    ```

2. Install dependencies using pip:

    ```
    pip install -r requirements.txt
    ```

## Configuration

1. Modify the `main.py` file to include your MySQL database details and EC2 instance details.
   
2. Ensure that you have the private key file (.pem) to access your EC2 instance and update the `security_key_file` variable in `main.py` with the correct path.

## Running the Application

1. Navigate to the project directory:

    ```
    cd assignment
    ```

2. Run the Flask application:

    ```
    python3 main.py
    ```

3. Access the application in your web browser at `http://localhost:8888`.

You can view my version at 
- http://192.168.0.236:8888/

## Usage

1. Enter a search query in the provided input field on the home page and click the "Search" button.

2. If the result is cached in the MySQL database, it will be displayed. Otherwise, the application will execute a remote command on the specified EC2 instance to fetch the search result.

3. After executing the search, the result will be displayed on a new page.

4. You can navigate back to the home page to perform another search.

## Troubleshooting

- If you encounter any issues with connecting to the MySQL database or executing remote commands, ensure that your database and EC2 instance are properly configured and accessible.

- Double-check your MySQL database details and EC2 instance IP address in the `config.py` file and `app.py` respectively.

