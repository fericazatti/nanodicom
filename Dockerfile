# Base Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first for caching purposes
COPY requirements.txt .

# Install dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the client code into the container
COPY dicom_listener/ dicom_listener/
#COPY .env .  # Optional: this can be mounted as a volume at runtime

# Default command to run the application
CMD ["python3", "-m", "dicom_listener"]
