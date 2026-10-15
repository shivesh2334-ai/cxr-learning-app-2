// Local retrieval and deterministic report composition; no image inference or API required.
export const sources = [
 {id:'glossary',title:'Fleischner Society glossary (2024)',url:'https://pubs.rsna.org/doi/10.1148/radiol.232558'},
 {id:'air',title:'Thoracic abnormal air collections: radiograph–CT correlation (2020)',url:'https://pmc.ncbi.nlm.nih.gov/articles/PMC7066360/'},
 {id:'bullae',title:'Giant bulla or pneumothorax: How to distinguish (2019)',url:'https://pmc.ncbi.nlm.nih.gov/articles/PMC6702430/'}
];
export const chunks = [
 ['bullae','bullous emphysema bulla bullae hyperlucency lucent curvilinear wall reduced vascular markings','Thin-walled lucent airspaces may represent bullae. Large peripheral bullae can resemble pneumothorax. CT can resolve uncertainty in a clinically stable patient.','bullae'],
 ['pneumothorax','pneumothorax pleural line absent peripheral markings deep sulcus','A visible visceral pleural edge with absent peripheral vascular markings raises concern for pneumothorax. Mimics include bullae and skin folds. Urgent clinical assessment is needed for acute symptoms; instability requires emergency management without waiting for CT.','air'],
 ['consolidation','consolidation opacity air bronchogram airspace pneumonia','Airspace opacity is a descriptive finding and is not specific for infection. Interpret with symptoms, distribution and prior imaging.','glossary'],
 ['atelectasis','atelectasis collapse linear bands volume loss scarring','Atelectasis reflects reduced lung aeration and volume. Linear opacities alone do not establish the cause or chronicity.','glossary'],
 ['effusion','pleural effusion meniscus blunted costophrenic angle','Pleural fluid can produce basal opacity or costophrenic blunting. Radiograph appearance varies with patient position; ultrasound may clarify suspected fluid.','glossary'],
 ['interstitial','interstitial reticular reticulation fibrosis nodular','Reticular or nodular opacities require description of distribution. A radiograph alone may not establish the underlying interstitial disorder.','glossary'],
 ['nodule','nodule mass rounded focal lesion','A focal rounded opacity needs comparison with prior studies and assessment for superimposed structures; CT may be needed for characterization.','glossary']
].map(([id,terms,text,source])=>({id,terms,text,source}));
const tokens=s=>new Set(s.toLowerCase().match(/[a-z]{3,}/g)||[]);
export function retrieve(query) {
 const q=tokens(query);
 return chunks.map(c=>({...c,score:[...tokens(c.terms)].filter(t=>q.has(t)).length})).filter(c=>c.score>0).sort((a,b)=>b.score-a.score).slice(0,3);
}
export function localReport(observations='',history='') {
 const refs=retrieve(observations);
 const result=['PRELIMINARY CXR REPORT — CLINICIAN REVIEW REQUIRED','Mode: local knowledge-base assisted draft. The uploaded image has NOT been interpreted by a model.',`Clinical context (user supplied): ${history || 'Not provided'}`,'Findings (clinician supplied):',observations.trim() || 'No observations supplied. Image findings, normality, laterality and image quality are undetermined.','Impression:',observations.trim() ? 'Draft based only on the supplied observations; confirm findings and differential on the original image.' : 'Insufficient observations to generate an impression. Enter visible findings and their side/zone.','Retrieved teaching guidance (not additional patient findings):',...refs.map(c=>`[${c.source}] ${c.text}`),'Limitations: Unmentioned structures are not assumed normal. No automatic image detection, diagnosis or localization was performed.','References:',...sources.filter(s=>refs.some(c=>c.source===s.id)).map(s=>`${s.title}: ${s.url}`)].join('\n\n');
 return {result,annotations:[],source:'local',references:sources.filter(s=>refs.some(c=>c.source===s.id))};
}
export function validateAI(value) {
 if (!value || typeof value.report!=='string' || !value.report.trim() || value.report.length>20000 || !Array.isArray(value.annotations) || value.annotations.length>12) throw new Error('Invalid report');
 const annotations=value.annotations.map(a=>{if(!a || typeof a.label!=='string' || !a.label.trim() || a.label.length>160 || !Number.isFinite(a.x)||!Number.isFinite(a.y)||a.x<0||a.x>1||a.y<0||a.y>1)throw new Error('Invalid annotation');return {label:a.label,x:a.x,y:a.y};});
 return {result:value.report,annotations,source:'ai'};
}
