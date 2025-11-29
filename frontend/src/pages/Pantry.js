import React, {useState} from 'react';

export default function Pantry(){
  const [file,setFile] = useState(null);
  const [userId] = useState("test_user");
  const [pantry, setPantry] = useState([]);

  async function upload(){
    if(!file) return;
    const form = new FormData();
    form.append('file', file);
    form.append('user_id', userId);
    const resp = await fetch('http://localhost:8000/api/pantry/upload-photo?user_id='+userId, {method:'POST', body: form});
    const data = await resp.json();
    setPantry(prev => prev.concat(data.parsed_items));
  }

  return (
    <div>
      <h2>Pantry</h2>
      <input type="file" accept="image/*" onChange={e=>setFile(e.target.files[0])} />
      <button onClick={upload}>Upload</button>
      <ul>
        {pantry.map((p,i)=><li key={i}>{p.name || JSON.stringify(p)}</li>)}
      </ul>
    </div>
  )
}
