FROM python:3.11.1-slim-buster

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create dir and assign the folder as the main
WORKDIR /api

# copy project
COPY ./backend/api .

# copy and install requirments
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
