FROM node:24-alpine3.21

# 作業ディレクトリを設定
WORKDIR /app

COPY app/package.json app/package-lock.json ./

RUN npm install

# プロジェクト初期でReactをダウンロードするとき
# RUN npm create vite@latest

# CMD ["sh"]
# CMD ["npm", "run", "dev", "--host", "0.0.0.0", "--port", "5173"]
CMD ["npm","run","dev"]