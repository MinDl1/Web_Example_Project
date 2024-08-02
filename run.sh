#!/bin/bash

if [[ "$1" = "--start" && $# -eq 1 ]]; then
  echo "The starting of docker containers has begun" &&
  sudo docker compose -f docker-compose.yml up --build -d &&
  echo "Docker containers have been created"
elif [[ "$1" = "--stop" && $# -eq 1 ]]; then
  echo "The stopping of docker containers has begun" &&
  sudo docker stop backend_api &&
  echo "The Docker container 'backend_api' has been stopped" &&
  sudo docker stop backend_database_postgres &&
  echo "The Docker container 'backend_database_postgres' has been stopped" &&
  sudo docker stop backend_database_mongo &&
  echo "The Docker container 'backend_database_mongo' has been stopped" &&
  sudo docker stop cadvisor &&
  echo "The Docker container 'cadvisor' has been stopped" &&
  sudo docker stop nodeexporter &&
  echo "The Docker container 'nodeexporter' has been stopped" &&
  sudo docker stop prometheus &&
  echo "The Docker container 'prometheus' has been stopped" &&
  sudo docker stop grafana &&
  echo "The Docker container 'grafana' has been stopped" &&
  sudo docker stop test_backend_api &&
  echo "The Docker container 'test_backend_api' has been stopped" &&
  echo "All web_example_project containers with images and volumes have been stopped"
elif [[ "$1" = "--remove" && $# -eq 1 ]]; then
  echo "The removing of Docker containers has begun" &&
  sudo docker container rm backend_api &&
  sudo docker image rm web_example_project-api &&
  sudo docker volume rm web_example_project_backend_api &&
  echo "The Docker container 'backend_api' with image and volume has been removed" &&
  sudo docker container rm backend_database_postgres &&
  sudo docker image rm web_example_project-postgres_database &&
  sudo docker volume rm web_example_project_backend_database_postgres &&
  echo "The Docker container 'backend_database_postgres' with image and volume has been removed" &&
  sudo docker container rm backend_database_mongo &&
  sudo docker image rm web_example_project-mongo_database &&
  sudo docker volume rm web_example_project_backend_database_mongo_data &&
  sudo docker volume rm web_example_project_backend_database_mongo_config &&
  echo "The Docker container 'backend_database_mongo' with image and volumes has been removed" &&
  sudo docker container rm cadvisor &&
  sudo docker image rm gcr.io/cadvisor/cadvisor:v0.49.1 &&
  echo "The Docker container 'cadvisor' with image has been removed" &&
  sudo docker container rm nodeexporter &&
  sudo docker image rm prom/node-exporter:v1.8.2 &&
  echo "The Docker container 'nodeexporter' with image has been removed" &&
  sudo docker container rm prometheus &&
  sudo docker image rm prom/prometheus:v2.46.0 &&
  sudo docker volume rm web_example_project_prometheus_data &&
  echo "The Docker container 'prometheus' with image and volume has been removed" &&
  sudo docker container rm grafana &&
  sudo docker image rm grafana/grafana:8.3.4 &&
  sudo docker volume rm web_example_project_grafana_data &&
  echo "The Docker container 'grafana' with image and volume has been removed" &&
  sudo docker container rm test_backend_api &&
  sudo docker image rm web_example_project-test_api &&
  sudo docker volume rm web_example_project_test_backend_api &&
  echo "The Docker container 'test_backend_api' with image and volume has been removed" &&
  echo "All web_example_project containers with images and volumes have been removed"
elif [[ "$1" = "--stop" && $# -eq 2 ]]; then
  if [ "$2" = "--remove" ]; then
    echo "The stopping of docker containers has begun" &&
    sudo docker stop backend_api &&
    echo "The Docker container 'backend_api' has been stopped" &&
    sudo docker stop backend_database_postgres &&
    echo "The Docker container 'backend_database_postgres' has been stopped" &&
    sudo docker stop backend_database_mongo &&
    echo "The Docker container 'backend_database_mongo' has been stopped" &&
    sudo docker stop cadvisor &&
    echo "The Docker container 'cadvisor' has been stopped" &&
    sudo docker stop nodeexporter &&
    echo "The Docker container 'nodeexporter' has been stopped" &&
    sudo docker stop prometheus &&
    echo "The Docker container 'prometheus' has been stopped" &&
    sudo docker stop grafana &&
    echo "The Docker container 'grafana' has been stopped" &&
    sudo docker stop test_backend_api &&
    echo "The Docker container 'test_backend_api' has been stopped" &&
    echo "All web_example_project containers with images and volumes have been stopped" &&
    echo "The removing of Docker containers has begun" &&
    sudo docker container rm backend_api &&
    sudo docker image rm web_example_project-api &&
    sudo docker volume rm web_example_project_backend_api &&
    echo "The Docker container 'backend_api' with image and volume has been removed" &&
    sudo docker container rm backend_database_postgres &&
    sudo docker image rm web_example_project-postgres_database &&
    sudo docker volume rm web_example_project_backend_database_postgres &&
    echo "The Docker container 'backend_database_postgres' with image and volume has been removed" &&
    sudo docker container rm backend_database_mongo &&
    sudo docker image rm web_example_project-mongo_database &&
    sudo docker volume rm web_example_project_backend_database_mongo_data &&
    sudo docker volume rm web_example_project_backend_database_mongo_config &&
    echo "The Docker container 'backend_database_mongo' with image and volumes has been removed" &&
    sudo docker container rm cadvisor &&
    sudo docker image rm gcr.io/cadvisor/cadvisor:v0.49.1 &&
    echo "The Docker container 'cadvisor' with image has been removed" &&
    sudo docker container rm nodeexporter &&
    sudo docker image rm prom/node-exporter:v1.8.2 &&
    echo "The Docker container 'nodeexporter' with image has been removed" &&
    sudo docker container rm prometheus &&
    sudo docker image rm prom/prometheus:v2.46.0 &&
    sudo docker volume rm web_example_project_prometheus_data &&
    echo "The Docker container 'prometheus' with image and volume has been removed" &&
    sudo docker container rm grafana &&
    sudo docker image rm grafana/grafana:8.3.4 &&
    sudo docker volume rm web_example_project_grafana_data &&
    echo "The Docker container 'grafana' with image and volume has been removed" &&
    sudo docker container rm test_backend_api &&
    sudo docker image rm web_example_project-test_api &&
    sudo docker volume rm web_example_project_test_backend_api &&
    echo "The Docker container 'test_backend_api' with image and volume has been removed" &&
    echo "All web_example_project containers with images and volumes have been removed"
  else
    echo "Invalid arguments.
For help: ./run.sh -h"
    exit 1
  fi
elif [[ "$1" = "-h" || "$1" = "--help" ]] && [[ $# -eq 1 ]]; then
  echo "
      --start     start application
      --stop      stop application
      --remove    remove application

      Example:    ./run.sh --start
                  ./run.sh --stop
  "
else
  echo "Invalid arguments.
For help: ./run.sh -h"
  exit 1
fi
