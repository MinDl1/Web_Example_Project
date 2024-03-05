# Web Example Project

# Will be done

- Error codes
- Documentation
- Frontend on React
- Endpoints in res_forgot_passwd (with redis)
- And other things

# How to start

## First step

Create .env file in code directory using example.env.txt  
```bash
cp example.env.txt .env
```

## BUILD and RUN docker-compose

```bash
cd code && docker-compose up --build -d
```

After building and running containers you can check:
FastAPI Swagger - http://127.0.0.1:8001/docs