import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
};

export default function () {
  const base = 'http://localhost:8000';
  // register temp user
  const email = `user_${Math.random().toString(36).slice(2)}@ex.com`;
  http.post(`${base}/api/auth/register`, JSON.stringify({user_name:'u', user_email:email, password:'pass1234'}), { headers: {'Content-Type':'application/json'} });

  // login
  const login = http.post(`${base}/api/auth/login`, JSON.stringify({user_email:email, password:'pass1234'}), { headers: {'Content-Type':'application/json'} });
  check(login, { 'login 200': r => r.status === 200 });
  const cookies = login.cookies['access_token'] ? `access_token=${login.cookies['access_token'][0].value}` : '';

  // create note
  const create = http.post(`${base}/api/notes/`, JSON.stringify({note_title:'k6', note_content:'hello'}), {
    headers: {'Content-Type':'application/json', 'Cookie': cookies}
  });
  check(create, { 'create 201': r => r.status === 201 });

  // list notes
  const list = http.get(`${base}/api/notes/`, { headers: {'Cookie': cookies}});
  check(list, { 'list 200': r => r.status === 200 });

  sleep(1);
}