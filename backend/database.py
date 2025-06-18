from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv  # ← 追加
import os

# .envファイル読み込み
load_dotenv()

# 環境変数からDB情報を取得
DB_HOST = os.getenv("MYSQLHOST")
DB_PORT = os.getenv("MYSQLPORT")
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_NAME = os.getenv("MYSQLDATABASE")


# 接続URL構築
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

print("MYSQLHOST:", os.environ.get("MYSQLHOST"))
print("MYSQLPORT:", os.environ.get("MYSQLPORT"))
print("MYSQLUSER:", os.environ.get("MYSQLUSER"))
print("MYSQLPASSWORD:", os.environ.get("MYSQLPASSWORD"))
print("MYSQLDATABASE:", os.environ.get("MYSQLDATABASE"))