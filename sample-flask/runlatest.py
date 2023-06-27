import docker

client = docker.from_env()

images = client.images.list()
existing_versions = [float(image.tags[0].split(":")[1]) for image in images if image.tags and image.tags[0].startswith("tomerkul/myflask:")]

if existing_versions:
    latest_version = max(existing_versions)
    image_name = f"tomerkul/myflask:{latest_version}"
    print(f"Using existing image: {image_name}")

    # Run the container with port mapping
    container = client.containers.run(image_name, detach=True, ports={'5000/tcp': 5000})
    print(f"Successfully started container: {container.id}")
else:
    print("No existing images found. Please build the image first.")


