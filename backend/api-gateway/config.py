import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Function to get an environment variable or return a default value
def get_env_variable(var_name, default=None):
    """
    Retrieve an environment variable and provide a default if it doesn't exist.
    
    Parameters:
        var_name (str): The name of the environment variable to retrieve.
        default (any): The default value to return if the variable isn't found (default is None).
    
    Returns:
        any: The value of the environment variable or the default value.
    """
    return os.getenv(var_name, default)

# Example configuration variables
# Replace 'VAR_NAME' with the actual environment variable names you need
# Replace 'default_value' with the actual default values you need for each variable

API_URL = get_env_variable("API_URL", "default_api_url")
DATABASE_URL = get_env_variable('DATABASE_URL', "default_database_url")
PORT = get_env_variable('PORT', '8000')

# Main function to test the configuration output
if __name__ == "__main__":
    print(f"API URL: {API_URL}")
    print(f"Database URL: {DATABASE_URL}")
    print(f"Port: {PORT}")
