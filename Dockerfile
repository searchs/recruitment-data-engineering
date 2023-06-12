FROM python:3.8
WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev netcat  # Added netcat here
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY load-data.py .
COPY wait-for.sh .     
RUN chmod +x wait-for.sh   
CMD ["./wait-for.sh", "pgdb:5432", "--", "python", "./load-data.py"]