import docker
import subprocess

# SSH connection details
ssh_key_path = "/home/tomer/.ssh/mykeyVir.pem"
ssh_user = "ec2-user"
ec2_instance_ip = "3.87.44.92"

# Find and kill the process running on port 5000
command = f"ssh -i {ssh_key_path} {ssh_user}@{ec2_instance_ip} 'sudo lsof -t -i :5000 -sTCP:LISTEN -P -n'"
process = subprocess.run(command, shell=True, capture_output=True, text=True)
if process.returncode == 0:
    process_id = process.stdout.strip()
    # Kill the process
    command = f"ssh -i {ssh_key_path} {ssh_user}@{ec2_instance_ip} 'sudo kill -9 {process_id}'"
    subprocess.run(command, shell=True, check=True)

# Find the latest version of the image
client = docker.from_env()
images = client.images.list()

existing_versions = [float(image.tags[0].split(":")[1]) for image in images if image.tags and image.tags[0].startswith("tomerkul/myflask:")]

if existing_versions:
    latest_version = max(existing_versions)
    next_version = latest_version + 0.1
else:
    next_version = 1.0

# Format the version number to one decimal place
next_version = f"{next_version:.1f}"

image_name = f"tomerkul/myflask:{latest_version}"

# Save the image as a tar file
subprocess.run(["docker", "save", "-o", "latest_image.tar", image_name], check=True)

# Transfer the tar file to the EC2 instance
subprocess.run(["scp", "-i", ssh_key_path, "-o", "StrictHostKeyChecking=no", "latest_image.tar", f"{ssh_user}@{ec2_instance_ip}:/home/ec2-user"], check=True)

# Remove the local tar file
subprocess.run(["rm", "latest_image.tar"], check=True)

# Run the downloaded image on the EC2 instance
command = f"ssh -i {ssh_key_path} {ssh_user}@{ec2_instance_ip} 'docker load -i latest_image.tar -t {image_name}'"
subprocess.run(command, shell=True, check=True)

command = f"ssh -i {ssh_key_path} {ssh_user}@{ec2_instance_ip} 'docker run -d -p 5000:5000 {image_name}'"
subprocess.run(command, shell=True, check=True)

