from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models, schemas, database, data
import traceback

from fastapi import FastAPI

app = FastAPI(trust_forwarded_headers=True)

origins = [
    "https://first-hackathon-q475.vercel.app",
    "http://localhost",
    "http://localhost:5173",  # フロントエンドのURLとポートを許可
]



# ★ここで CORS を追加！
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 許可するオリジンのリスト
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# データベースセッションを取得する関数
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# アプリケーション起動時にDBテーブル作成と初期データ投入
@app.on_event("startup")
def create_db_tables_and_initial_data():
    models.Base.metadata.create_all(bind=database.engine)
    print("Database tables created or already exist.")

    db = next(get_db()) # DBセッションを取得
    try:

        category_id_map = {} # カテゴリ名とIDを紐付ける辞書
        for category_data in data.INITIAL_FOOD_CATEGORIES_LEVEL1:
            category_name = category_data["name"]
            existing_category = db.query(models.FoodCategory).filter(models.FoodCategory.name == category_name).first()
            if not existing_category:
                new_category = models.FoodCategory(name=category_name, parent_id=None)
                db.add(new_category)
                db.flush() # IDを確定させるためにflush
                category_id_map[category_name] = new_category.id
            else:
                category_id_map[category_name] = existing_category.id
        db.commit() # ここで最初のコミット

        # Step 2: 中間カテゴリを投入（親IDを紐付け）
        for child_name, parent_name in data.INITIAL_FOOD_CATEGORIES_LEVEL2.items():
            existing_category = db.query(models.FoodCategory).filter(models.FoodCategory.name == child_name).first()
            if not existing_category:
                parent_id = category_id_map.get(parent_name) # 親カテゴリのIDを取得
                if parent_id is None: # 親カテゴリが見つからない場合はエラー
                    print(f"Warning: Parent category '{parent_name}' not found for '{child_name}'")
                    continue
                new_category = models.FoodCategory(name=child_name, parent_id=parent_id)
                db.add(new_category)
                db.flush()
                category_id_map[child_name] = new_category.id # 新しいカテゴリのIDをマップに追加
            else:
                category_id_map[child_name] = existing_category.id
        db.commit() # ここで2回目のコミット

        # Step 3: 具体的な料理を投入（親IDを紐付け）
        for dish_name, parent_name in data.INITIAL_FOOD_CATEGORIES_LEVEL3.items():
            existing_category = db.query(models.FoodCategory).filter(models.FoodCategory.name == dish_name).first()
            if not existing_category:
                parent_id = category_id_map.get(parent_name) # 親カテゴリのIDを取得
                if parent_id is None: # 親カテゴリが見つからない場合はエラー
                    print(f"Warning: Parent category '{parent_name}' not found for '{dish_name}'")
                    continue
                new_category = models.FoodCategory(name=dish_name, parent_id=parent_id)
                db.add(new_category)
                db.flush()
            else:
                pass # 既に存在する場合は何もしない
        db.commit() # ここで最終コミット
        print("Initial food categories loaded.")

    except Exception as e:
        db.rollback()
        print("❌ Error loading initial food categories")
        print(e)  # エラー内容を表示
        traceback.print_exc()  # ← これでトレースバックを表示！
    finally:
        db.close() # セッションを閉じる


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI Backend!"}

# ★食べ物絞り込みAPIエンドポイント★
@app.get("/food-categories/", response_model=List[schemas.FoodCategory])
def get_food_categories(parent_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    指定された親カテゴリIDの子カテゴリのリスト、
    または親カテゴリIDが指定されていない場合は最上位カテゴリのリストを返す。
    """
    # parent_id が None なら、一番上の階層のカテゴリを取得
    if parent_id is None:
        categories = db.query(models.FoodCategory).filter(models.FoodCategory.parent_id == None).all()
    else:
        # 指定された parent_id を持つ子カテゴリを取得
        categories = db.query(models.FoodCategory).filter(models.FoodCategory.parent_id == parent_id).all()
        # 親カテゴリが存在するかどうかのチェック（おまけ）
        parent_category = db.query(models.FoodCategory).filter(models.FoodCategory.id == parent_id).first()
        if not parent_category:
             raise HTTPException(status_code=404, detail="Parent category not found")

    return categories # 取得したカテゴリのリストを返す

# 特定のカテゴリIDの詳細情報を取得するAPI
@app.get("/food-categories/{category_id}", response_model=schemas.FoodCategory)
def get_food_category_by_id(category_id: int, db: Session = Depends(get_db)):
    """
    特定のカテゴリIDの情報を返す。
    """
    category = db.query(models.FoodCategory).filter(models.FoodCategory.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, proxy_headers=True)
