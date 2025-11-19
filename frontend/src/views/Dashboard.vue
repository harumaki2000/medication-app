<template>
  <div class="dashboard-page">
    <header class="dashboard-hero">
      <div>
        <p class="section-label">毎日の服薬</p>
        <h2>服用中の薬一覧</h2>
        <p class="hero-description">
          予定された服用時間を見ながら、次に飲む薬をすぐに確認できます。
        </p>
      </div>
    </header>

    <section class="medication-board">
      <div v-if="medications.length === 0" class="empty-state">
        <p>まだ登録された薬がありません。</p>
        <p>画面上部の「新規追加」から記録を始めましょう。</p>
      </div>

      <div v-else class="medication-grid">
        <article v-for="med in medications" :key="med.medication_id" class="med-card">
          <header>
            <h3>{{ med.name }}</h3>
            <p class="dosage">量: {{ med.dosage }}</p>
          </header>

          <p class="memo" v-if="med.memo">{{ med.memo }}</p>

          <div class="timings">
            <span v-for="timing in med.timings" :key="timing.timing_id" class="tag">
              {{ timing.take_time }}
            </span>
          </div>
        </article>
      </div>
    </section>

    <button class="add-new-button" @click="addMedication">＋ 服薬を追加する</button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

interface MedicationTiming {
  timing_id: number;
  take_time: string;
  medication_id: number;
}

interface Medication {
  medication_id: number;
  name: string;
  dosage: string;
  memo?: string;
  timings: MedicationTiming[];
}

const router = useRouter();
const medications = ref<Medication[]>([]);

onMounted(async () => {
  const userId = localStorage.getItem('user_id');
  const token = localStorage.getItem('token');

  if (!userId || !token) {
    router.push('/login');
    return;
  }

  try {
    const response = await axios.get(`http://127.0.0.1:8000/users/${userId}/medications/`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    medications.value = response.data;
  } catch (error) {
    console.error(error);
    alert('データ取得失敗');
  }
});

const addMedication = () => {
  router.push('/medications/add')
};
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  padding: 1.5rem clamp(1rem, 2vw, 1.5rem) 2rem;
  background: #f6f7f9;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  box-sizing: border-box;
}

.dashboard-hero {
  width: min(1100px, 100%);
  margin: 0 auto;
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 20px;
  background: #ffffff;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
  box-sizing: border-box;
}

.dashboard-hero h2 {
  margin: 0.35rem 0 0.4rem;
  font-size: clamp(1.6rem, 1.8vw, 1.95rem);
  color: #1f2b3a;
}

.hero-description {
  margin: 0;
  font-size: 1rem;
  color: #4c5566;
}

.section-label {
  margin: 0;
  letter-spacing: 0.15em;
  font-size: 0.75rem;
  color: #8b96b1;
}

.medication-board {
  width: min(1100px, 100%);
  margin: 0 auto;
  background: #ffffff;
  border-radius: 28px;
  padding: 2rem;
  box-shadow: 0 15px 30px rgba(33, 41, 63, 0.1);
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  box-sizing: border-box;
}

.empty-state {
  text-align: center;
  color: #5b647b;
  line-height: 1.6;
  font-size: 1rem;
}

.medication-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}

.med-card {
  background: #f6f7fa;
  padding: 1.2rem;
  border-radius: 18px;
  border: 1px solid rgba(84, 101, 149, 0.15);
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  min-height: 160px;
}

.med-card header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #1b2440;
}

.dosage {
  margin: 0.35rem 0 0;
  font-size: 0.95rem;
  color: #49506a;
}

.memo {
  margin: 0;
  color: #5a5e73;
  font-size: 0.9rem;
}

.timings {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.tag {
  display: inline-flex;
  padding: 0.35rem 0.85rem;
  border-radius: 999px;
  background: #e3f2ff;
  color: #1f4da7;
  font-size: 0.8rem;
  border: 1px solid rgba(31, 77, 167, 0.2);
}

.add-new-button {
  width: 100%;
  max-width: 460px;
  align-self: center;
  padding: 0.95rem;
  border-radius: 18px;
  border: none;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.add-new-button {
  background: #1f2f4f;
  color: #fff;
  box-shadow: 0 10px 22px rgba(31, 47, 79, 0.25);
}

.add-new-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 12px 25px rgba(31, 47, 79, 0.25);
}

@media (max-width: 860px) {
  .dashboard-hero {
    flex-direction: column;
    align-items: flex-start;
  }

}

@media (max-width: 640px) {
  .dashboard-page {
    padding: 1rem;
  }

  .medication-board {
    padding: 1.5rem;
  }
}
</style>
