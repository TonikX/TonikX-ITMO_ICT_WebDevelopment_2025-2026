FROM node:24-alpine

WORKDIR /app

COPY package.json ./

RUN npm install

RUN npm install vue-router@4 axios vuetify @mdi/font

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
