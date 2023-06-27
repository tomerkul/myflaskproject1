import docker

# Create a Docker client
client = docker.from_env()

# Define the image name
image_name = "tomerkul/myflask"

# List all available tags for the image on Docker Hub
tags = client.images.list(name=image_name)

# Sort the tags in descending order and get the latest version
latest_tag = sorted(tags, key=lambda x: x.attrs['Created'], reverse=True)[0].tags[0]

# Pull the latest version of the image
client.images.pull(repository=image_name, tag=latest_tag)

print(f"Successfully pulled {image_name}:{latest_tag}")
