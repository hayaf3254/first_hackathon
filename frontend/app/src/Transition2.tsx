import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Transition2.css'; 

const Transition2 = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const selectedSubcategory = location.state?.selectedSubcategory as string | undefined;
  const [timeLeft, setTimeLeft] = useState(10); // 10秒カウントダウン
  const [selected, setSelected] = useState<string | null>(null);

  const options = ['ラーメン', 'コンビニ', 'お惣菜', '松屋']; // 仮データ

  useEffect(() => {
    if (timeLeft > 0 && !selected) {
      const timer = setTimeout(() => setTimeLeft(prev => prev - 1), 1000);
      return () => clearTimeout(timer);
    }

    if (timeLeft === 0 && !selected && options.length > 0) {
      const randomIndex = Math.floor(Math.random() * options.length);
      const randomChoice = options[randomIndex];
      setSelected(randomChoice);
      alert(`${randomChoice} を自動で選びました！`);
    }
  }, [timeLeft, selected, options]);

  const handleSelect = (option: string) => {
    if (selected) return;
    setSelected(option);
    alert(`${option} を選びました！`);
  };

  return (
    <div className="center-container">
      <h1 className="category-h1">チョイス！！！</h1>
      <p>{selectedSubcategory ? `${selectedSubcategory}の中から選んでください` : '中華料理の中から選んでください'}</p>
      <p className="countdown-text">残り時間: <span className="countdown-number">{timeLeft}</span> 秒</p>


      <div className="button-container">
        {options.map(option => (
          <button
            key={option}
            onClick={() => handleSelect(option)}
            className="category-button"
          >
            {option}
          </button>
        ))}
      </div>

      {selected && (
        <>
        <p className="selected-result">
        選んだ料理：<span className="selected-name">{selected}</span>
        </p>
        <button className="home-button"
          onClick={() => navigate('/')}>
          ホームに戻る
        </button>
      </>
      )}

    </div>
  );
};

export default Transition2;
