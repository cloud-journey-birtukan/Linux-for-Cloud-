# This is the "Base" image
# Use the official AWS Lambda image
FROM public.ecr.aws/lambda/python:3.12

# Set the working directory inside the container
WORKDIR /var/task

# Install the libraries your code needs directly
RUN pip install boto3 Pillow

# Copy only your python script
COPY processor.py .

# Set the handler (matches the function in your code)
CMD [ "processor.lambda_handler" ]