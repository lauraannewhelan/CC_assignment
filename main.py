# Importing Flask framework and necessary modules
from flask import Flask, render_template, request

# Importing Paramiko for SSH functionality
import paramiko

# Importing MySQL connector for database operations
import mysql.connector

# Importing Error module for error handling
from mysql.connector import Error

# Creating a Flask application instance
app = Flask(__name__)

# MySQL database details
mysql_host = "127.0.0.1"  # Use localhost or the IP of your host machine
mysql_port = "7703"  # Use the host port mapped to the MySQL container
mysql_database = "search_cache"  # Your MySQL database name
mysql_user = "student"  # Your MySQL username
mysql_password = "mypassword"  # Your MySQL password

# EC2 instance details
instance_ip = "16.170.247.48"  # CHANGE THIS to your EC2 instance's public IP address
security_key_file = "/Users/laurawhelan/Downloads/CT5170.pem"  # CHANGE THIS to the path of your private key file
cmd = "python3 ~/assignment/wiki.py"  # CHANGE THIS to the command to execute wiki.py on the EC2 instance

# Function to establish connection to the MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host=mysql_host,
            port=mysql_port,
            database=mysql_database,
            user=mysql_user,
            password=mysql_password
        )
        return connection
    except Error as e:
        print("Error connecting to database:", e)
        return None

# Function to save query results to the MySQL database
def save_to_database(query, result):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            myquery = "INSERT INTO query_results (query, result) VALUES (%s, %s)"
            data = (query, result)
            cursor.execute(myquery, data)
            connection.commit()
            cursor.close()
            connection.close()
            print("Successfully saved to database")
        except Error as e:
            print("Error saving to database:", e)

# Function to search for query results in the MySQL database
def search_from_database(query):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            myquery = "SELECT result FROM query_results WHERE query = %s"
            cursor.execute(myquery, (query,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return result[0] if result else None
        except Error as e:
            print("Error searching from database:", e)
    return None

# Function to execute remote commands on the EC2 instance
def execute_remote_command(command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key = paramiko.RSAKey.from_private_key_file(security_key_file)
        client.connect(hostname=instance_ip, username="ubuntu", pkey=key)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('utf-8').strip()
        client.close()
        return output
    except Exception as e:
        print("Error executing remote command:", e)
        return None

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for search functionality with POST method
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']  # Getting the search query from the form data
    cached_result = search_from_database(query)  # Searching for cached result in the database
    if cached_result:  # If cached result found
        return render_template('search_results.html', query=query, result=cached_result)  # Rendering template with cached result
    else:  # If cached result not found
        output = execute_remote_command(f"{cmd} '{query}'")  # Executing remote command to fetch search result
        if output:  # If search result fetched successfully
            save_to_database(query, output)  # Saving search result to the database
        else:  # If search result not found
            output = f"No result found for '{query}'"  # Generating message for no result found
        return render_template('search_results.html', query=query, result=output)  # Rendering template with search result

# Running the Flask app if this script is executed directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)  # Running the Flask app on host 0.0.0.0 and port 8888
