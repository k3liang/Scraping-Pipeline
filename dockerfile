FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# need to change current directory to this folder for scrapy cmd
WORKDIR /app/jobs_project

CMD ["scrapy", "crawl", "job_spider"]