const $ = id => document.getElementById(id);
let selectedImage, previewUrl;
document.querySelectorAll('[data-tab]').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('[data-tab]').forEach(b => { const active=b===button; b.setAttribute('aria-pressed',active); $(b.dataset.tab).hidden=!active; });
}));
$('upload').addEventListener('change', async () => {
  selectedImage=null; $('result').textContent=''; $('download').hidden=true; $('preview').hidden=true; $('empty').hidden=false;
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  const file=$('upload').files[0];
  if (!file) return;
  if (!['image/jpeg','image/png','image/webp'].includes(file.type) || file.size>2500000) { $('status').textContent='Choose a supported image under 2.5 MB.'; return; }
  try { const bitmap=await createImageBitmap(file); bitmap.close(); } catch { $('status').textContent='This file is not a readable image.'; return; }
  selectedImage=file; previewUrl=URL.createObjectURL(file); $('preview').src=previewUrl; $('preview').hidden=false; $('empty').hidden=true; $('status').textContent='Image ready.';
});
const download = (text,name) => { const url=URL.createObjectURL(new Blob([text],{type:'text/plain'})); const a=document.createElement('a'); a.href=url; a.download=name; a.click(); setTimeout(()=>URL.revokeObjectURL(url),1000); };
$('analyze').addEventListener('click', async () => {
  if (!selectedImage) { $('status').textContent='Upload a radiograph first.'; return; }
  $('analyze').disabled=true; $('upload').disabled=true; $('status').textContent='Analyzing…'; $('result').textContent=''; $('download').hidden=true;
  try {
    const image=await new Promise((resolve,reject)=>{const reader=new FileReader(); reader.onload=()=>resolve(reader.result.split(',')[1]); reader.onerror=reject; reader.readAsDataURL(selectedImage);});
    const response=await fetch('/api/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image,mimeType:selectedImage.type,mode:$('mode').value,history:$('history').value})});
    const data=await response.json(); if (!response.ok) throw new Error(data.error || 'Analysis unavailable.');
    $('result').textContent=data.result; $('status').textContent='Draft complete — clinician review required.'; $('download').hidden=false;
  } catch(error) { $('status').textContent=error.message; } finally { $('analyze').disabled=false; $('upload').disabled=false; }
});
$('download').onclick=()=>download($('result').textContent,'cxr-analysis.txt');
const headings=['Examination','Comparison','Clinical indication','Technical factors','Support devices','Chest wall','Mediastinum and hila','Lungs','Pleura and diaphragm','Impression'];
headings.forEach((heading,i)=>{const label=document.createElement('label');label.htmlFor=`field${i}`;label.textContent=heading;const field=document.createElement('textarea');field.id=label.htmlFor;$('fields').append(label,field);});
$('export').onclick=()=>download('EDUCATIONAL DRAFT — REQUIRES CLINICIAN REVIEW\n\n'+headings.map((h,i)=>`${h.toUpperCase()}\n${$('field'+i).value || 'Not specified'}`).join('\n\n'),'cxr-manual-report.txt');
try {
  const response=await fetch('/knowledge-base.json'); if (!response.ok) throw new Error(); const knowledge=await response.json();
  const render=()=>{ $('references').replaceChildren(); Object.entries(knowledge).forEach(([key,value])=>{if (!JSON.stringify({key,value}).toLowerCase().includes($('search').value.toLowerCase())) return;const details=document.createElement('details');const summary=document.createElement('summary');summary.textContent=key.replaceAll('_',' ');const content=document.createElement('pre');content.textContent=JSON.stringify(value,null,2);details.append(summary,content);$('references').append(details);}); };
  $('search').addEventListener('input',render);render();
} catch { $('references').textContent='Learning references could not load. Please refresh.'; }
