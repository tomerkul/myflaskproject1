FROM python:3.8

# Set a directory for the app
WORKDIR /usr/src/app

# Copy all the files from the host directory to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Tell the port number the container should expose
EXPOSE 5000

# Run the command
CMD ["python", "app.py"]
