import React, {useState} from 'react';

export default function Plan(){
  const [plan, setPlan] = useState(null);
  const userId = "test_user";
  async function generate(){
    const resp = await fetch('http://localhost:8000/api/plan/generate', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({user_id: userId})
    });
    const data = await resp.json();
    setPlan(data.plan);
  }
  return (
    <div>
      <h2>Plan</h2>
      <button onClick={generate}>Generate Weekly Plan</button>
      {plan && <div>
        <h3>Grocery List:</h3>
        <ul>{plan.grocery_list.map((g,i)=><li key={i}>{g.item} x{g.qty}</li>)}</ul>
        <h3>Week:</h3>
        <ol>{plan.week.map((d,i)=><li key={i}>{d.recipe.title}</li>)}</ol>
      </div>}
    </div>
  )
}
