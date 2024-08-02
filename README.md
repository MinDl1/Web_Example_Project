# Web Example Project

# Will be done

- [ ] CI/CD (Jenkins)
- [ ] Documentation
- [ ] Frontend on React
- [ ] Endpoints in res_forgot_passwd (with redis)
- [ ] And other things

---

- [x] Automatic deployment
- [x] Unit auto tests
- [x] Error codes
- [x] Monitoring (Grafana, Prometheus, Cadvisor, Node exporter)

# How to start

## First step

### Create .env file in code directory using example.env.txt

```bash
cp example.env.txt .env
```

### Default admin user in PostgreSQL for application:

Login: admin  
Password: 12345

## BUILD and RUN docker-compose

```bash
docker-compose up --build -d
```

# After building and running containers you can check:

- [FastAPI](https://fastapi.tiangolo.com/) [Swagger](https://swagger.io/) - http://127.0.0.1:8001/docs
- [PostgreSQL](https://www.postgresql.org/) - http://127.0.0.1:5432
- [MongoDB](https://www.mongodb.com/) - http://127.0.0.1:27017
- [Cadvisor](https://github.com/google/cadvisor) - http://127.0.0.1:8002
- [Node exporter](https://github.com/prometheus/node_exporter) - http://127.0.0.1:8003
- [Prometheus](https://prometheus.io/) - http://127.0.0.1:8004
- [Grafana](https://grafana.com/) - http://127.0.0.1:8005
