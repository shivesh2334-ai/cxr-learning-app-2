import {localReport} from './reporting.js';
const $ = id => document.getElementById(id);
let selectedImage, previewUrl, annotations=[], loadedImage, generation=0;
document.querySelectorAll('[data-tab]').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('[data-tab]').forEach(b => { const active=b===button; b.setAttribute('aria-pressed',active); $(b.dataset.tab).hidden=!active; });
}));
$('upload').addEventListener('change', async () => {
  const current=++generation; selectedImage=null; loadedImage=null; annotations=[]; $('film').hidden=true; $('saveFilm').disabled=true; $('markers').replaceChildren(); $('result').value=''; $('download').hidden=true; $('preview').hidden=true; $('empty').hidden=false;
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  const file=$('upload').files[0];
  if (!file) return;
  if (!['image/jpeg','image/png','image/webp'].includes(file.type) || file.size>2500000) { $('status').textContent='Choose a supported image under 2.5 MB.'; return; }
  try { const bitmap=await createImageBitmap(file); bitmap.close(); } catch { $('status').textContent='This file is not a readable image.'; return; }
  if(current!==generation)return; selectedImage=file; previewUrl=URL.createObjectURL(file); $('preview').src=previewUrl; $('preview').hidden=false; $('empty').hidden=true; $('status').textContent='Image ready.'; const img=new Image(); img.onload=()=>{if(current!==generation)return; loadedImage=img; $('preview').hidden=true; $('film').hidden=false; $('saveFilm').disabled=false; drawFilm();}; img.src=previewUrl;
});
const download = (text,name) => { const url=URL.createObjectURL(new Blob([text],{type:'text/plain'})); const a=document.createElement('a'); a.href=url; a.download=name; a.click(); setTimeout(()=>URL.revokeObjectURL(url),1000); };
$('analyze').addEventListener('click', async () => {
  if (!selectedImage) { $('status').textContent='Upload a radiograph first.'; return; }
  $('analyze').disabled=true; $('upload').disabled=true; $('status').textContent='Analyzing…'; $('result').value=''; $('download').hidden=true;
  try {
    let data;
    if($('localOnly').checked) data=localReport($('observations').value,$('history').value);
    else {
    const image=await new Promise((resolve,reject)=>{const reader=new FileReader(); reader.onload=()=>resolve(reader.result.split(',')[1]); reader.onerror=reject; reader.readAsDataURL(selectedImage);});
    const response=await fetch('/api/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({image,mimeType:selectedImage.type,mode:$('mode').value,history:$('history').value,observations:$('observations').value})});
    data=await response.json(); if (!response.ok) throw new Error(data.error || 'Analysis unavailable.');
    }
    if(data.source==='ai') annotations=data.annotations || []; drawFilm();
    $('result').value=data.result; $('status').textContent=data.source==='local' ? `${data.fallbackReason || 'Local mode.'} Image not automatically interpreted; draft uses your observations.` : 'AI draft complete — verify report and marker positions.'; $('download').hidden=false;
  } catch(error) { const fallback=localReport($('observations').value,$('history').value); $('result').value=fallback.result; annotations=[];drawFilm();$('download').hidden=false;$('status').textContent='Network/API unavailable. Local draft uses your observations only; image not interpreted.'; } finally { $('analyze').disabled=false; $('upload').disabled=false; }
});
$('download').onclick=()=>download($('result').value,'cxr-analysis.txt');
const headings=['Examination','Comparison','Clinical indication','Technical factors','Support devices','Chest wall','Mediastinum and hila','Lungs','Pleura and diaphragm','Impression'];
headings.forEach((heading,i)=>{const label=document.createElement('label');label.htmlFor=`field${i}`;label.textContent=heading;const field=document.createElement('textarea');field.id=label.htmlFor;$('fields').append(label,field);});
$('export').onclick=()=>download('EDUCATIONAL DRAFT — REQUIRES CLINICIAN REVIEW\n\n'+headings.map((h,i)=>`${h.toUpperCase()}\n${$('field'+i).value || 'Not specified'}`).join('\n\n'),'cxr-manual-report.txt');
try {
  const response=await fetch('/knowledge-base.json'); if (!response.ok) throw new Error(); const knowledge=await response.json();
  const render=()=>{ $('references').replaceChildren(); Object.entries(knowledge).forEach(([key,value])=>{if (!JSON.stringify({key,value}).toLowerCase().includes($('search').value.toLowerCase())) return;const details=document.createElement('details');const summary=document.createElement('summary');summary.textContent=key.replaceAll('_',' ');const content=document.createElement('pre');content.textContent=JSON.stringify(value,null,2);details.append(summary,content);$('references').append(details);}); };
  $('search').addEventListener('input',render);render();
} catch { $('references').textContent='Learning references could not load. Please refresh.'; }

function drawFilm(){
 if(!loadedImage)return;
 const canvas=$('film'),ctx=canvas.getContext('2d');
 const scale=Math.min(1,1800/Math.max(loadedImage.naturalWidth,loadedImage.naturalHeight));
 const w=Math.round(loadedImage.naturalWidth*scale),h=Math.round(loadedImage.naturalHeight*scale),row=52;
 canvas.width=w;canvas.height=h+100+annotations.length*row;
 ctx.fillStyle='#091017';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.drawImage(loadedImage,0,0,w,h);
 const radius=Math.max(12,w/65);ctx.font=`bold ${radius}px sans-serif`;
 annotations.forEach((a,i)=>{const x=a.x*w,y=a.y*h;ctx.strokeStyle='#ffe459';ctx.lineWidth=3;ctx.beginPath();ctx.arc(x,y,radius,0,Math.PI*2);ctx.stroke();ctx.fillStyle='#ffe459';ctx.fillText(String(i+1),x+radius+3,y);});
 ctx.font=`${Math.max(12,Math.min(20,w/38))}px sans-serif`;ctx.fillStyle='white';
 ctx.fillText('PRELIMINARY — clinician review required',12,h+28);
 ctx.fillText('Markers are approximate. Original pixels are not diagnostically enhanced.',12,h+55);
 annotations.forEach((a,i)=>{const text=`${i+1}. ${a.label}`; const max=Math.max(20,Math.floor(w/12));ctx.fillStyle='#ffe459';ctx.fillText(text.slice(0,max),12,h+90+i*row);if(text.length>max)ctx.fillText(text.slice(max,max*2),12,h+112+i*row);});
 $('markers').replaceChildren();annotations.forEach((a,i)=>{const li=document.createElement('li');li.textContent=a.label;const remove=document.createElement('button');remove.textContent='Remove';remove.onclick=()=>{annotations.splice(i,1);drawFilm();};li.append(remove);$('markers').append(li);});
}
$('film').onclick=event=>{
 if(!loadedImage || annotations.length>=12)return;
 const label=$('markerLabel').value.trim();if(!label){$('status').textContent='Enter a finding label before placing a marker.';return;}
 const c=$('film'),r=c.getBoundingClientRect(),h=Math.round(loadedImage.naturalHeight*Math.min(1,1800/Math.max(loadedImage.naturalWidth,loadedImage.naturalHeight)));
 const x=(event.clientX-r.left)/r.width,y=(event.clientY-r.top)/r.height*c.height/h;
 if(y>1)return;annotations.push({label,x,y});drawFilm();
};
$('undoMarker').onclick=()=>{annotations.pop();drawFilm();};
$('saveFilm').onclick=()=>{$('film').toBlob(blob=>{if(!blob)return;const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='cxr-annotated-draft.png';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);},'image/png');};
