import os

SECRET_KEY = "test"

base_dir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, "app.db")

# custom variables
data_files_folder_name = "data_files"
data_files_path = os.path.join(base_dir, data_files_folder_name)
