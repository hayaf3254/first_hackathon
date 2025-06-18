import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Transition1.css';

type Category = {
  id: number;
  name: string;
  parent_id: number | null;
};

const Transition1 = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const selectedName = location.state?.selectedName as string | undefined;

  const [allCategories, setAllCategories] = useState<Category[]>([]);
  const [childCategories, setChildCategories] = useState<Category[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/food-categories/`);
        if (!res.ok) throw new Error('親カテゴリ取得に失敗しました');
        const data: Category[] = await res.json();
        setAllCategories(data);

        const parent = data.find((cat) => cat.name === selectedName);
        if (!parent) throw new Error('選択されたカテゴリが見つかりません');

        const childRes = await fetch(`${import.meta.env.VITE_API_BASE_URL}/food-categories/?parent_id=${parent.id}`);
        if (!childRes.ok) throw new Error('子カテゴリ取得に失敗しました');
        const children: Category[] = await childRes.json();
        setChildCategories(children);
      } catch (err: any) {
        setError(err.message);
      }
    };

    if (selectedName) {
      fetchAll();
    }
  }, [selectedName]);

  const handleSubcategoryClick = (subcategory: string) => {
    navigate('/transition2', { state: { selectedSubcategory: subcategory } });
  };

  return (
    <div className="center-container">
      <h1 className="category-h1">{selectedName} の選択</h1>
      {error && <p>{error}</p>}
      {childCategories.length > 0 ? (
        <div>
          {childCategories.map((subcategory) => (
            <button
              className="category-button"
              key={subcategory.id}
              onClick={() => handleSubcategoryClick(subcategory.name)}
            >
              {subcategory.name}
            </button>
          ))}
        </div>
      ) : (
        <p>子カテゴリが見つかりません。</p>
      )}
    </div>
  );
};

export default Transition1;
