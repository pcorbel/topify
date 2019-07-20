# First stage: Frontend
FROM node:11.7.0-alpine AS front_builder

# Install dependencies
WORKDIR /app
COPY topify/templates/topify/package.json \
     topify/templates/topify/package-lock.json \
     /app/
RUN npm install

# Build
COPY topify/templates/topify /app
RUN npm run build

# Final stage
FROM python:3.7-alpine

WORKDIR /app
ENV REFRESH_INTERVAL 3000
RUN apk add --no-cache --virtual .build_deps \
  linux-headers \
  gcc \
  musl-dev
COPY requirements.txt /app
COPY setup.py /app
RUN pip install -r requirements.txt
RUN apk del .build_deps
RUN apk add --no-cache curl
COPY topify /app/topify
COPY --from=front_builder /app/dist /app/topify/templates/topify
RUN python setup.py install
HEALTHCHECK CMD curl -X GET "http://0.0.0.0:5000/" || exit 1
CMD ["topify"]
