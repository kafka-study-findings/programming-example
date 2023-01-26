FROM python:3.12.0a4-alpine3.17
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# ARG hosts
# ENV hosts=$hosts
COPY topic_list.txt topic_list.txt
COPY main.py main.py
RUN ls -al
CMD ["python","main.py"]