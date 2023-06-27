import docker

# Create a Docker client
client = docker.from_env()

# Image details
repo_name = 'tomerkul/myflask'

# Get the available images
images = client.images.list()

# Get the available image tags
tags = []
for image in images:
    for tag in image.tags:
        if repo_name in tag:
            tags.append(tag.split(':')[1])

# Filter out any non-numeric tags
numeric_tags = [tag for tag in tags if tag.replace('.', '').isdigit()]

# Sort the numeric tags in descending order
sorted_tags = sorted(numeric_tags, key=lambda x: tuple(map(int, x.split('.'))), reverse=True)

if sorted_tags:
    # Get the latest tag
    latest_tag = sorted_tags[0]

    # Pull the latest image
    image_name = f"{repo_name}:{latest_tag}"
    print(f"Pulling image: {image_name}")
    client.images.pull(repository=repo_name, tag=latest_tag)
else:
    print("No image found with version tags.")
