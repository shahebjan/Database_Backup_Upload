# <<<-------------------------Importing all Important modules & Packages--------------------------------->>>
import os
import time
import datetime
import pymysql
import paramiko
# <<<------------------------Making a class with constructer----------------------------->>>
class backup_upload:

    def __init__(self, remote_file_path, hostname, username, password):
        self.remote_file_path = remote_file_path
        self.hostname = hostname
        self.username = username
        self.password = password
# <<<---------------------Assigning a Backup Path where my Backup Files will be stored-------------------->>>
        self.backup_directory = 'D:\Backup\Files'
#<<<---------------------Making a Function that creates a Backup and will upload on server------------------->>> 
    def create_backup(self):
        conn = pymysql.connect(host = 'localhost', user = 'root')
        with conn.cursor() as cur:
            sql = 'SHOW DATABASES'
            cur.execute(sql)
            data = cur.fetchall()
            for row in data:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                backup_filename = f"{row[0]}-{timestamp}.sql"
                backup_path = os.path.join(self.backup_directory, backup_filename)
                command = f'mysqldump -u root --skip-column-statistics --databases {row[0]} > "{backup_path}"'
                os.system(command)
                print("Backup Successfully")

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                try:
                    ssh.connect(hostname=self.hostname, username=self.username, password=self.password)
                    sftp = ssh.open_sftp()
                    sftp.put(backup_path, self.remote_file_path+backup_filename)
                    print("Backup uploaded successfully.")
# <<<--------------------Deleting those Backup Files from local system----------------------------->>>
                    os.unlink(backup_path)
                    print("Backup deleted=====>>> {}".format(backup_path))
# <<<--------------------Handeling errors and exceptions---------------------->>>
                except Exception as e:
                    print(f"Error: {str(e)}")
# <<<-------------------Closing all connections finally---------------------->>> 
                finally:
                    sftp.close()
                    ssh.close()

# <<<---------------------Credentials-------------------------------->>>

hostname = '202.176.1.189'
username = 'techpath-user1'
password = 'pyarmedhokha1'
remote_file_path = '/var/www/html/'
# <<<------------------------Making Object of that class------------------------------->>>
backup_uploader = backup_upload(remote_file_path, hostname, username, password)
# <<<----------------------Calling Backup creation function by Object of class-------------------->>>
backup_uploader.create_backup()

        

        