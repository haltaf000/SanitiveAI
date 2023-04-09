import axios from 'axios';

const API_URL = 'http://localhost:8000/api/';

class AuthService {
  async login(username, password) {
    const response = await axios.post(API_URL + 'token/', {
      username,
      password,
    });

    if (response.data.access) {
      localStorage.setItem('user', JSON.stringify(response.data));
    }

    return response.data;
  }

  logout() {
    localStorage.removeItem('user');
  }

  async register(username, password) {
    const response = await axios.post(API_URL + 'register/', {
      username,
      password,
    });

    return response.data;
  }
}

export default new AuthService();