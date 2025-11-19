<template>
  <div class="auth-page">
    <div class="auth-card register">
      <header class="auth-header">
        <h1>新規登録</h1>
        <p class="description">毎日の服薬を安心して記録できるようになります。</p>
      </header>

      <form class="form-grid" @submit.prevent="registerUser">
        <label class="form-field" for="email">
          <span>メールアドレス</span>
          <input type="email" id="email" v-model="email" required autocomplete="email" />
        </label>

        <label class="form-field" for="username">
          <span>ユーザー名</span>
          <input type="text" id="username" v-model="username" required autocomplete="name" />
        </label>

        <label class="form-field" for="password">
          <span>パスワード</span>
          <input type="password" id="password" v-model="password" required autocomplete="new-password" />
        </label>

        <label class="form-field" for="passwordConfirm">
          <span>パスワード（確認）</span>
          <input type="password" id="passwordConfirm" v-model="passwordConfirm" required autocomplete="new-password" />
        </label>

        <button class="primary-button" type="submit">登録する</button>
      </form>

      <button class="text-button" @click="login">既にアカウントをお持ちの場合はこちら</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const email = ref('');
const username = ref('');
const password = ref('');
const passwordConfirm = ref('');

const registerUser = async () => {
  if (password.value !== passwordConfirm.value) {
    alert('パスワードが一致しません。');
    return;
  }

  try {
    const response = await axios.post('http://127.0.0.1:8000/users/', {
      email: email.value,
      username: username.value,
      password: password.value
    });

    alert('登録成功 ID: ' + response.data.user_id);
    email.value = '';
    username.value = '';
    password.value = '';
    passwordConfirm.value = '';
  } catch (error: any) {
    console.error(error);

    if (error.response && error.response.data && error.response.data.detail) {
      alert('登録失敗: ' + error.response.data.detail);
    } else {
      alert('登録失敗... サーバーエラーの可能性があります。');
    }
  }
};

const login = () => {
  router.push('/');
};
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background: #f6f7f9;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2.5rem 1.2rem;
  box-sizing: border-box;
}

.auth-card {
  width: min(460px, 100%);
  background: #ffffff;
  border-radius: 18px;
  padding: 2.2rem;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.auth-card.register {
  border: 1px solid rgba(52, 64, 88, 0.15);
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
  gap: 0.95rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  font-weight: 600;
  color: #1c2a42;
}

.form-field input {
  width: 100%;
  padding: 0.95rem 1rem;
  border: 1px solid rgba(76, 93, 139, 0.3);
  border-radius: 12px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  box-sizing: border-box;
}

.form-field input:focus {
  border-color: rgba(76, 93, 139, 0.8);
  box-shadow: 0 0 0 3px rgba(76, 93, 139, 0.15);
  outline: none;
}

.primary-button {
  width: 100%;
  padding: 1rem 1.1rem;
  border-radius: 14px;
  border: 1px solid #1f2b3a;
  background: #1f2b3a;
  color: #fff;
  font-size: 1.05rem;
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
  font-size: 0.95rem;
  cursor: pointer;
  padding: 0.25rem;
  align-self: center;
}

.text-button:hover {
  color: #0a0f18;
}

@media (max-width: 520px) {
  .auth-card {
    padding: 1.8rem;
    border-radius: 20px;
  }

  .auth-header h1 {
    font-size: 1.7rem;
  }
}
</style>
