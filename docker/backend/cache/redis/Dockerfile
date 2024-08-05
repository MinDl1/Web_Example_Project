FROM redis:7.4.0-alpine

# Download sed
RUN apk add --no-cache sed

COPY /backend/cache/redis/redis.conf.template /usr/local/etc/redis/redis.conf.template

ARG REDIS_PASSWORD
ARG REDIS_USER
ARG REDIS_USER_PASSWORD
ARG TEST_REDIS_USER
ARG TEST_REDIS_USER_PASSWORD

#Generating a conf file based on conf.template
RUN sed -e "s/{REDIS_PASSWORD}/$REDIS_PASSWORD/g" \
         -e "s/{REDIS_USER}/$REDIS_USER/g" \
         -e "s/{REDIS_USER_PASSWORD}/$REDIS_USER_PASSWORD/g" \
         -e "s/{TEST_REDIS_USER}/$TEST_REDIS_USER/g" \
         -e "s/{TEST_REDIS_USER_PASSWORD}/$TEST_REDIS_USER_PASSWORD/g" \
         /usr/local/etc/redis/redis.conf.template > /usr/local/etc/redis/redis.conf

CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
