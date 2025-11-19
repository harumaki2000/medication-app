<template>
  <div class="auth-page">
    <div class="auth-card">
      <header class="auth-header">
        <h1>ログイン</h1>
        <p class="description">毎日の服薬予定を記録して、飲み忘れを減らしましょう。</p>
      </header>

      <div class="form-grid">
        <label class="form-field" for="email">
          <span>メールアドレス</span>
          <input type="email" id="email" v-model="email" autocomplete="username" />
        </label>

        <label class="form-field" for="password">
          <span>パスワード</span>
          <input type="password" id="password" v-model="password" autocomplete="current-password" />
        </label>
      </div>

      <div class="actions">
        <button class="primary-button" @click="login">ログイン</button>
        <button class="text-button" @click="goToRegister">新規登録はこちら</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const email = ref('');
const password = ref('');

const login = async () => {
  try {
    const params = new URLSearchParams();
    params.append('username', email.value);
    params.append('password', password.value);

    const response = await axios.post('http://127.0.0.1:8000/token', params);

    localStorage.setItem('token', response.data.access_token);
    localStorage.setItem('user_id', response.data.user_id);

    router.push('/dashboard');
  } catch (error) {
    console.error(error);
    alert('ログイン失敗: メールアドレスかパスワードが間違っています');
  }
};

const goToRegister = () => {
  router.push('/register');
};
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background: #f7f8fa;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
  box-sizing: border-box;
}

.auth-card {
  width: min(420px, 100%);
  background: #ffffff;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.auth-header {
  text-align: center;
}

.auth-header h1 {
  margin: 0;
  font-size: 2rem;
  color: #1f2b3a;
}

.description {
  margin: 0.4rem 0 0;
  font-size: 0.95rem;
  color: #4c5566;
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-field {
  font-weight: 600;
  color: #344058;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-field span {
  font-size: 0.95rem;
}

.form-field input {
  width: 100%;
  padding: 0.95rem 1rem;
  border: 1px solid rgba(52, 64, 88, 0.3);
  border-radius: 12px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  box-sizing: border-box;
}

.form-field input:focus {
  border-color: rgba(52, 64, 88, 0.8);
  box-shadow: 0 0 0 3px rgba(52, 64, 88, 0.15);
  outline: none;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.primary-button {
  width: 100%;
  padding: 0.95rem 1rem;
  font-size: 1rem;
  border-radius: 12px;
  border: 1px solid #1f2b3a;
  background: #1f2b3a;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
}

.primary-button:hover {
  background: #101826;
}

.text-button {
  background: transparent;
  border: none;
  color: #1f2b3a;
  font-weight: 600;
  cursor: pointer;
  font-size: 0.95rem;
  padding: 0.25rem;
}

.text-button:hover {
  color: #0a0f18;
}

@media (max-width: 480px) {
  .auth-card {
    padding: 1.5rem;
    border-radius: 20px;
  }

  .auth-header h1 {
    font-size: 1.6rem;
  }
}
</style>
