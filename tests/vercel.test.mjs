import { test } from 'node:test';
import assert from 'node:assert/strict';
import handler from '../api/analyze.js';
const call=async req=>{const res={headers:{},setHeader(k,v){this.headers[k]=v;},status(s){this.code=s;return this;},json(body){this.body=body;return this;}};await handler(req,res);return res;};
test('GET rejected',async()=>assert.equal((await call({method:'GET'})).code,405));
test('missing key returns honest unavailable response',async()=>{delete process.env.GEMINI_API_KEY;assert.equal((await call({method:'POST'})).code,503);});
test('invalid payload rejected before provider call',async()=>{process.env.GEMINI_API_KEY='test';assert.equal((await call({method:'POST',body:{mode:'report',mimeType:'image/png',image:'not base64'}})).code,400);delete process.env.GEMINI_API_KEY;});
test('provider success and failure handled without leaking credentials',async()=>{const original=globalThis.fetch;process.env.GEMINI_API_KEY='test-secret';const req={method:'POST',body:{mode:'report',mimeType:'image/png',image:'aGVsbG8='}};try{globalThis.fetch=async()=>({ok:true,json:async()=>({candidates:[{content:{parts:[{text:'Draft report'}]}}]})});assert.equal((await call(req)).body.result,'Draft report');globalThis.fetch=async()=>({ok:false});const failed=await call(req);assert.equal(failed.code,502);assert.ok(!JSON.stringify(failed.body).includes('test-secret'));}finally{globalThis.fetch=original;delete process.env.GEMINI_API_KEY;}});
