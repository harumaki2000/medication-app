<template>
  <div class="form-page">
    <div class="form-card">
      <header class="form-header">
        <h1>薬の新規登録</h1>
        <p class="description">毎日飲む薬を記録して、次の服用予定を忘れないように管理しましょう。</p>
      </header>

      <div class="form-grid">
        <label class="form-field">
          <span>薬の名前 <span class="required">*</span></span>
          <input type="text" v-model="name" placeholder="例: ロキソニン" />
        </label>

        <label class="form-field">
          <span>飲む量 <span class="required">*</span></span>
          <input type="text" v-model="dosage" placeholder="例: 1回1錠" />
        </label>

        <label class="form-field">
          <span>メモ</span>
          <input type="text" v-model="memo" placeholder="例: 食後に飲む" />
        </label>

        <div class="form-field">
          <span>通知時間</span>
          <div class="time-list">
            <div v-for="(_, index) in timings" :key="index" class="time-row">
              <input type="time" v-model="timings[index]" />
              <button v-if="timings.length > 1" type="button" class="icon-btn" @click="removeTimingField(index)">×</button>
            </div>
          </div>
          <button type="button" class="add-time-btn" @click="addTimingField">+ 時間を追加</button>
        </div>
      </div>

      <div class="actions">
        <button class="primary-button" @click="register">登録する</button>
        <button class="ghost-button" type="button" @click="router.push('/dashboard')">キャンセル</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

const name = ref('');
const dosage = ref('');
const memo = ref('');
const timings = ref(['']);

const addTimingField = () => {
  timings.value.push('');
};

const removeTimingField = (index: number) => {
  timings.value.splice(index, 1);
};

const register = async () => {
  if (!name.value || !dosage.value) {
    alert('薬の名前と量は必須です');
    return;
  }

  const userId = localStorage.getItem('user_id');
  const token = localStorage.getItem('token');

  try {
    const validTimings = timings.value.filter(t => t !== '');

    await axios.post(`http://127.0.0.1:8000/users/${userId}/medications/`, {
      name: name.value,
      dosage: dosage.value,
      memo: memo.value,
      timings: validTimings
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    alert('登録しました');
    router.push('/dashboard');
  } catch (error) {
    console.error(error);
    alert('登録に失敗しました');
  }
};
</script>

<style scoped>
.form-page {
  min-height: 100vh;
  background: #f6f7f9;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2.5rem 1.2rem;
  box-sizing: border-box;
}

.form-card {
  width: min(540px, 100%);
  background: #ffffff;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.1);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-header h1 {
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
  border-radius: 10px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  box-sizing: border-box;
}

.form-field input:focus {
  border-color: rgba(76, 93, 139, 0.8);
  box-shadow: 0 0 0 3px rgba(76, 93, 139, 0.12);
  outline: none;
}

.time-list {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.time-row {
  display: flex;
  gap: 0.4rem;
  align-items: center;
}

.time-row input {
  flex: 1;
}

.icon-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1px solid rgba(76, 93, 139, 0.4);
  background: transparent;
  font-size: 1.2rem;
  line-height: 1;
  cursor: pointer;
  transition: background 0.2s ease, border-color 0.2s ease;
}

.icon-btn:hover {
  border-color: rgba(76, 93, 139, 0.8);
  background: rgba(76, 93, 139, 0.1);
}

.add-time-btn {
  margin-top: 0.4rem;
  padding: 0.45rem 0.9rem;
  border-radius: 999px;
  border: 1px dashed rgba(76, 93, 139, 0.4);
  background: transparent;
  font-size: 0.9rem;
  color: #1f2b3a;
  cursor: pointer;
  width: fit-content;
}

.add-time-btn:hover {
  border-color: rgba(76, 93, 139, 0.8);
}

.required {
  color: #d64545;
  font-weight: 600;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.primary-button {
  width: 100%;
  padding: 0.95rem 1rem;
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

.ghost-button {
  width: 100%;
  padding: 0.95rem 1rem;
  border-radius: 12px;
  border: 1px solid rgba(31, 43, 58, 0.4);
  background: transparent;
  color: #1f2b3a;
  font-weight: 600;
  cursor: pointer;
  transition: border-color 0.2s ease, color 0.2s ease;
}

.ghost-button:hover {
  border-color: rgba(31, 43, 58, 0.8);
}

@media (max-width: 540px) {
  .form-card {
    padding: 2rem;
    border-radius: 16px;
  }

  .time-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .icon-btn {
    align-self: flex-end;
  }
}
</style>
