FROM python:3.11.1-slim-buster

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create dir and assign the folder as the main
WORKDIR /test

# copy project and test
COPY ./backend/api ./
COPY ./backend/test/api ./test

# install requirments
RUN pip install -r requirements.txt
RUN pip install -r test/requirements.txt

CMD ["python","-m","pytest", "test/"]
