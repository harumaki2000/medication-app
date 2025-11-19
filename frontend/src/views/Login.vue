<template>
  <div class="card">
    <h1>ログイン</h1>

    <div class="form-group">
      <label for="email">メールアドレス</label>
      <input type="email" id="email" v-model="email"/>
    </div>

    <div class="form-group">
      <label for="password">パスワード</label>
      <input type="password" id="password" v-model="password"/>
    </div>

    <button class="primary-button" @click="login">ログイン</button>
    <button class="secondary-button" @click="goToRegister">新規登録</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter()
const email = ref('')
const password = ref('')

const login = async () => {
  try {
    const params = new URLSearchParams()
    params.append('username', email.value)
    params.append('password', password.value)

    const response = await axios.post('http://127.0.0.1:8000/token', params)

    localStorage.setItem('token', response.data.access_token)

    router.push('/register')
  } catch (error) {
    console.error(error)
    alert('ログイン失敗: メールアドレスかパスワードが間違っています')
  }
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
body {
  font-family: 'Arial', sans-serif;
  background-color: #f0f2f5;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  margin: 0;
}

.container {
  max-width: 400px;
  width: 100%;
  padding: 30px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  color: #333;
  margin-bottom: 30px;
  font-size: 24px;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #555;
}

input[type="text"],
input[type="email"],
input[type="password"] {
  width: calc(100% - 20px);
  padding: 10px;
  border: 1px solid #555;
  border-radius: 5px;
  font-size: 16px;
}

input:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
}

button {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 10px;
}

.primary-button {
  background-color: #e0e0e0;
  color: #333;
}

.primary-button:hover {
  background-color: #d0d0d0;
}

.secondary-button {
  background-color: #627fce;
  color: #ffffff;
}

.secondary-button:hover {
  background-color: #4c6fce;
}
</style>