<template>
  <div class="dashboard-page">
    <header class="dashboard-hero">
      <div>
        <p class="section-label">毎日の服薬</p>
        <h2>服用中の薬一覧</h2>
        <p class="hero-description">
          今日の記録を確認しながら、次の服用に備えられます。
        </p>
      </div>
    </header>

    <section class="medication-board">
      <div v-if="medications.length === 0" class="empty-state">
        <p>まだ登録された薬がありません。</p>
        <p>「服薬を追加する」から記録を始めましょう。</p>
      </div>

      <div v-else class="medication-grid">
        <article v-for="med in medications" :key="med.medication_id" class="med-card">
          <header class="med-card-header">
            <div>
              <h3>{{ med.name }}</h3>
              <p class="dosage">量: {{ med.dosage }}</p>
            </div>
            <button
              type="button"
              class="icon-action"
              @click.stop="deleteMedication(med.medication_id)"
              aria-label="薬を削除"
            >
              <i class="ti ti-trash"></i>
            </button>
          </header>

          <p class="memo" v-if="med.memo">{{ med.memo }}</p>

          <div class="timings">
            <button
              v-for="timing in med.timings"
              :key="timing.timing_id"
              type="button"
              :class="['tag', 'timing-button', { recorded: isTaken(med.medication_id, timing.timing_id) }]"
              :disabled="recordingTiming === timing.timing_id || isTaken(med.medication_id, timing.timing_id)"
              @click="recordIntake(med.medication_id, timing.timing_id)"
            >
              <span>{{ timing.take_time }}</span>
              <small v-if="recordingTiming === timing.timing_id">記録中...</small>
              <small v-else-if="isTaken(med.medication_id, timing.timing_id)" class="recorded-badge">
                <i class="ti ti-check"></i>
                記録済み
              </small>
            </button>
          </div>
        </article>
      </div>
    </section>

    <button class="add-new-button" @click="addMedication">
      <i class="ti ti-plus"></i>
      服薬を追加する
    </button>
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

interface IntakeRecord {
  record_id: number;
  user_id: number;
  medication_id: number;
  timing_id: number | null;
  taken_at: string;
}

const router = useRouter();
const medications = ref<Medication[]>([]);
const todayRecords = ref<IntakeRecord[]>([]);
const recordingTiming = ref<number | null>(null);

const fetchTodayRecords = async (userId: string, token: string) => {
  const today = new Date().toISOString().split('T')[0];

  const response = await axios.get(
    `http://127.0.0.1:8000/users/${userId}/intake-records/?date=${today}`,
    {
      headers: { Authorization: `Bearer ${token}` }
    }
  );

  todayRecords.value = response.data;
};

const isTaken = (medicationId: number, timingId: number) =>
  todayRecords.value.some(
    (record) => record.medication_id === medicationId && record.timing_id === timingId
  );

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
    await fetchTodayRecords(userId, token);
  } catch (error) {
    console.error(error);
    alert('データ取得失敗');
  }
});

const recordIntake = async (medicationId: number, timingId: number) => {
  const userId = localStorage.getItem('user_id');
  const token = localStorage.getItem('token');

  if (!userId || !token) {
    alert('ログインが必要です');
    router.push('/login');
    return;
  }

  if (!confirm('この時間の服薬を記録しますか？')) {
    return;
  }

  recordingTiming.value = timingId;

  try {
    await axios.post(
      `http://127.0.0.1:8000/users/${userId}/intake-records/`,
      {
        medication_id: medicationId,
        timing_id: timingId
      },
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    );
    await fetchTodayRecords(userId, token);
    alert('飲んだ記録を保存しました');
  } catch (error) {
    console.error(error);
    alert('記録を保存できませんでした');
  } finally {
    recordingTiming.value = null;
  }
};

const deleteMedication = async (medicationId: number) => {
  if (!confirm('この薬を完全に削除しますか？')) {
    return;
  }

  const userId = localStorage.getItem('user_id');
  const token = localStorage.getItem('token');

  if (!userId || !token) {
    alert('ログインが必要です');
    router.push('/login');
    return;
  }

  try {
    await axios.delete(`http://127.0.0.1:8000/users/${userId}/medications/${medicationId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    medications.value = medications.value.filter((med) => med.medication_id !== medicationId);
    todayRecords.value = todayRecords.value.filter((record) => record.medication_id !== medicationId);
    alert('薬を削除しました');
  } catch (error) {
    console.error(error);
    alert('削除に失敗しました');
  }
};

const addMedication = () => {
  router.push('/medications/add');
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

.med-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
}

.icon-action {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1px solid rgba(84, 101, 149, 0.4);
  background: transparent;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #c81d25;
  cursor: pointer;
  transition: background 0.2s ease, border-color 0.2s ease;
}

.icon-action:hover {
  background: rgba(200, 29, 37, 0.08);
  border-color: rgba(200, 29, 37, 0.6);
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
  gap: 0.8rem;
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

.timing-button {
  border: 1px solid rgba(76, 93, 139, 0.4);
  background: #fff;
  color: #1f2b3a;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.07);
  flex-direction: column;
  cursor: pointer;
  font-weight: 600;
  min-width: 120px;
  min-height: 56px;
  justify-content: center;
  transition: background 0.2s ease, border-color 0.2s ease;
}

.timing-button span {
  font-size: 1rem;
}

.timing-button small {
  display: block;
  font-size: 0.65rem;
  color: #4c4c4c;
  margin-top: 0.15rem;
}

.timing-button:disabled {
  cursor: not-allowed;
  opacity: 0.75;
}

.timing-button.recorded {
  background: #f0f0f0;
  color: #4c5566;
  border-color: rgba(76, 93, 139, 0.4);
  box-shadow: inset 0 0 0 1px rgba(76, 93, 139, 0.3);
}

.recorded-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  margin-top: 0.15rem;
  font-size: 0.65rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  flex-direction: row;
}

.recorded-badge i {
  font-size: 0.8rem;
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
  background: #1f2f4f;
  color: #fff;
  box-shadow: 0 10px 22px rgba(31, 47, 79, 0.25);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
}

.add-new-button:hover {
  transform: translateY(-1px);
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

  .timings {
    gap: 0.5rem;
  }
}
</style>
