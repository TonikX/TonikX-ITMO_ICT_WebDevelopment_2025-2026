import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 5000,
});

(async () => {
  try {
    console.log('Testing login endpoint...');
    const res = await api.post('/auth/token/login/', {
      username: 'testuser',
      password: 'testpass123',
    });
    console.log('✓ Login successful:', res.data);
  } catch (e) {
    console.error('✗ Login failed:', e.message);
    if (e.response) {
      console.error('Response status:', e.response.status);
      console.error('Response data:', e.response.data);
    }
  }
})();
