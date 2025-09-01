FROM node:20-slim

WORKDIR /app
COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./ 2>/dev/null || true
RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000
CMD ["npm", "run", "start"]