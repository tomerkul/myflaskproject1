import subprocess
import docker

# Define the image name and tag
image_name = "tomerkul/myflask"
image_tag = "1.1"

# Create a Docker client
client = docker.from_env()

# Reload the Docker images by listing them again
client.images.list()

# Find the image with the specified name and tag
image = None
for img in client.images.list():
    if f"{image_name}:{image_tag}" in img.tags:
        image = img
        break

if image is None:
    print(f"No image found for {image_name}:{image_tag}")
    exit()

# Save the Docker image as a tar file
tar_file = f"{image_name.replace('/', '-')}-{image_tag}.tar"
subprocess.run(["docker", "save", "-o", tar_file, f"{image.id}"])

# Define the EC2 instance details
ec2_user = "ec2-user"
ec2_instance = "44.202.126.178"
key_file = "/home/tomer/.ssh/mykeyVir.pem"
remote_path = "/home/ec2-user"

# Transfer the Docker image to the EC2 instance using SCP
subprocess.run(["scp", "-i", key_file, "-o", "StrictHostKeyChecking=no", tar_file, f"{ec2_user}@{ec2_instance}:{remote_path}"])

# Run the Docker image on the EC2 instance
subprocess.run(["ssh", "-i", key_file, "-o", "StrictHostKeyChecking=no", f"{ec2_user}@{ec2_instance}", f"docker load -i {remote_path}/{tar_file}"])
subprocess.run(["ssh", "-i", key_file, "-o", "StrictHostKeyChecking=no", f"{ec2_user}@{ec2_instance}", f"docker run -d -p 5000:5000 {image_name}:{image_tag}"])

