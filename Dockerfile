FROM python:3.9-slim

WORKDIR /kws-pmd

COPY . /kws-pmd

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]