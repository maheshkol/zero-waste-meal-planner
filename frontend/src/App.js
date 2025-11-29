import React from 'react';
import Pantry from './pages/Pantry';
import Plan from './pages/Plan';

function App(){
  return (
    <div style={{padding:20}}>
      <h1>Zero-Waste Meal Planner (Prototype)</h1>
      <Pantry />
      <hr/>
      <Plan />
    </div>
  );
}

export default App;
