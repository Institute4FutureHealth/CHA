# Use the official Python 3.11 image as base
FROM python:3.11

ENV GRADIO_SERVER_NAME="0.0.0.0"


# Set the working directory in the container
WORKDIR /code

# Copy the dependencies file to the working directory
#COPY ./requirements.txt /code/requirements.txt

# this will work too
#COPY requirements.txt .

# Install any dependencies
#RUN pip install --no-cache-dir -r /code/requirements.txt

COPY setup.py /code/setup.py

RUN pip install --no-cache-dir '.[all]'

#this one will work too
#RUN pip install --no-cache-dir -r requirements.txt

# Install rsync
#RUN apt-get update && apt-get install -y rsync

# Copy all files except the specified directory
#COPY . .
#RUN rsync -a --exclude='openChavenv/' ./ /CHACode/

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user . $HOME/app

EXPOSE 7860

# Command to run the application
#following works and gradio url works but not able to access local url on 127.0.0.1:7860
CMD ["python", "main.py"]

#following works and gradio url works but not able to access local url on 127.0.0.1:7860
# CMD ["python", "main.py", "--address", "0.0.0.0", "--port", "7860", "--allow-websocket-origin", "nirmits-openCHA.hf.space"]
