import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SelectionTop.css'; 

type Category = {
  id: number;
  name: string;
};

const SelectionTop = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await fetch('http://localhost:8000/food-categories/');
        if (!response.ok) {
          throw new Error('カテゴリの取得に失敗しました');
        }
        const data: Category[] = await response.json();
        setCategories(data);
      } catch (err: any) {
        setError(err.message);
      }
    };

    fetchCategories();
  }, []);

  const handleClick = (name: string) => {
    navigate('/transition1', { state: { selectedName: name } });
  };

  return (
    <div className="center-container">
      <h1 className="category-h1">さっさと決めちゃおう！</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div className="button-container">
      {categories.map((category) => (
        <button
          className="category-button"
          key={category.id}
          onClick={() => handleClick(category.name)}
          style={{ margin: '10px', padding: '10px', fontSize: '16px' }}
        >
          {category.name}
        </button>
      ))}
      </div>
    </div>
  );
};

export default SelectionTop;
