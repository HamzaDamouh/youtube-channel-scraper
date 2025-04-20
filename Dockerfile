# Use the official Airflow image as the base image
FROM apache/airflow:2.6.1

# Copy the requirements file into the image
COPY requirements.txt /requirements.txt

# Install the extra Python dependencies defined in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /requirements.txt

# Optionally, copy the rest of your project if needed (e.g., your scraper, dags, etc.)
# Here we're assuming you want the entire project available in /opt/airflow
COPY . /opt/airflow

# Set the working directory (this is optional if the base image already sets it)
WORKDIR /opt/airflow
