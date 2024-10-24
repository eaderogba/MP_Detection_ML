# Use official TensorFlow runtime image
FROM tensorflow/tensorflow:2.6.0

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . /app

# Expose ports for FastAPI and Chainlit
EXPOSE 8000 8501

# Create a script to run both services
RUN echo '#!/bin/bash\n\
uvicorn inference:app --host 0.0.0.0 --port 8000 &\n\
chainlit run Chainlit.py --host 0.0.0.0 --port 8501\n\
' > /app/start_services.sh && chmod +x /app/start_services.sh

# Command to run both services
CMD ["/app/start_services.sh"]