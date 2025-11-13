FROM python:3.12.12-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r data_clean_requirements.txt
ENTRYPOINT [ "python", "data_clean.py", "Customer" "/Input/03_Library SystemCustomers.csv" "/Ouput/03_Library SystemCustomers.csv" ]