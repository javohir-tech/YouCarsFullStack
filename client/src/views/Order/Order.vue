<template>
  <div class="container">

    <a-breadcrumb class="bread_crumb" separator=">">
      <a-breadcrumb-item><router-link to="/">Главная</router-link></a-breadcrumb-item>
      <a-breadcrumb-item>Оставить заявку</a-breadcrumb-item>
    </a-breadcrumb>

    <div class="zayavka-wrap">

      <div class="zayavka-info">
        <div class="header">
          <h1>Оставьте заявку</h1>
        </div>
        <p class="zayavka-info__desc">
          Не можете определиться с выбором? Оставьте заявку — наш менеджер свяжется с вами,
          поможет подобрать автомобиль и ответит на все вопросы.
        </p>
        <ul class="zayavka-info__list">
          <li>
            <i class="fa-solid fa-circle-check"></i>
            <span>Бесплатная консультация</span>
          </li>
          <li>
            <i class="fa-solid fa-circle-check"></i>
            <span>Ответим в течение 30 минут</span>
          </li>
          <li>
            <i class="fa-solid fa-circle-check"></i>
            <span>Поможем с выбором и торгом</span>
          </li>
        </ul>
      </div>

      <div class="zayavka-form-wrap">
        <!-- Success state -->
        <div v-if="submitted" class="zayavka-success">
          <div class="zayavka-success__icon">
            <i class="fa-solid fa-circle-check"></i>
          </div>
          <h2 class="zayavka-success__title">Заявка отправлена!</h2>
          <p class="zayavka-success__desc">
            Мы получили вашу заявку и свяжемся с вами в ближайшее время.
          </p>
          <button class="zayavka-btn" @click="resetForm">Отправить ещё одну</button>
        </div>

        <!-- Form -->
        <form v-else class="zayavka-form" @submit.prevent="submitForm">
          <div class="zayavka-form__group">
            <label class="zayavka-form__label">Ваше имя <span class="req">*</span></label>
            <input v-model="form.name" type="text" class="zayavka-form__input"
              :class="{ 'zayavka-form__input--error': errors.name }" placeholder="Например: Иван Иванов" />
            <span v-if="errors.name" class="zayavka-form__error">{{ errors.name }}</span>
          </div>

          <div class="zayavka-form__group">
            <label class="zayavka-form__label">Номер телефона <span class="req">*</span></label>
            <input v-model="form.phone" type="tel" class="zayavka-form__input"
              :class="{ 'zayavka-form__input--error': errors.phone }" placeholder="+998 90 123 45 67" />
            <span v-if="errors.phone" class="zayavka-form__error">{{ errors.phone }}</span>
          </div>

          <div class="zayavka-form__group">
            <label class="zayavka-form__label">Какой автомобиль вас интересует? <span class="req">*</span></label>
            <input v-model="form.car" type="text" class="zayavka-form__input"
              :class="{ 'zayavka-form__input--error': errors.car }" placeholder="Например: Geely Monjaro 2025" />
            <span v-if="errors.car" class="zayavka-form__error">{{ errors.car }}</span>
          </div>

          <div class="zayavka-form__group">
            <label class="zayavka-form__label">Дополнительный комментарий</label>
            <textarea v-model="form.comment" class="zayavka-form__textarea"
              placeholder="Укажите бюджет, пожелания по цвету, комплектации и т.д." rows="4"></textarea>
          </div>

          <span v-if="errors.server" class="zayavka-form__error zayavka-form__error--server">
            <i class="fa-solid fa-triangle-exclamation"></i>
            {{ errors.server }}
          </span>

          <button type="submit" class="zayavka-btn" :disabled="loading">
            <i v-if="loading" class="fa-solid fa-spinner fa-spin"></i>
            <span>{{ loading ? 'Отправка...' : 'Отправить заявку' }}</span>
            <i v-if="!loading" class="fa-solid fa-paper-plane"></i>
          </button>
        </form>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

// ⚠️ Замените на свои данные
const TELEGRAM_BOT_TOKEN = import.meta.env.VITE_TELEGRAM_TOKEN
const TELEGRAM_CHAT_ID = import.meta.env.VITE_BOT_ID

const form = reactive({
  name: '',
  phone: '',
  car: '',
  comment: '',
})

const errors = reactive({
  name: '',
  phone: '',
  car: '',
  server: '',
})

const loading = ref(false)
const submitted = ref(false)

function validate() {
  let valid = true
  errors.name = ''
  errors.phone = ''
  errors.car = ''
  errors.server = ''

  if (!form.name.trim()) {
    errors.name = 'Пожалуйста, введите ваше имя'
    valid = false
  }

  if (!form.phone.trim()) {
    errors.phone = 'Пожалуйста, введите номер телефона'
    valid = false
  } else if (!/^[\d\s\+\-\(\)]{7,20}$/.test(form.phone.trim())) {
    errors.phone = 'Введите корректный номер телефона'
    valid = false
  }

  if (!form.car.trim()) {
    errors.car = 'Пожалуйста, укажите интересующий автомобиль'
    valid = false
  }

  return valid
}

async function submitForm() {
  if (!validate()) return

  loading.value = true

  const text =
    `🚗 <b>Новая заявка с YouCar</b>\n\n` +
    `👤 <b>Имя:</b> ${form.name}\n` +
    `📞 <b>Телефон:</b> ${form.phone}\n` +
    `🚘 <b>Интересует:</b> ${form.car}\n` +
    (form.comment ? `💬 <b>Комментарий:</b> ${form.comment}` : '')

  try {
    const res = await fetch(
      `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_id: TELEGRAM_CHAT_ID,
          text,
          parse_mode: 'HTML',
        }),
      }
    )

    const data = await res.json()

    if (!data.ok) {
      throw new Error(data.description || 'Telegram error')
    }

    submitted.value = true
  } catch (e) {
    errors.server = 'Не удалось отправить заявку. Попробуйте позже.'
    console.error(e)
  } finally {
    loading.value = false
  }
}

function resetForm() {
  form.name = ''
  form.phone = ''
  form.car = ''
  form.comment = ''
  errors.name = ''
  errors.phone = ''
  errors.car = ''
  errors.server = ''
  submitted.value = false
}
</script>

<style scoped>
.zayavka-wrap {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  padding: 40px 0 80px;
  align-items: start;
}

/* Info side */
.zayavka-info__desc {
  font-size: 15px;
  color: #555;
  line-height: 1.75;
  margin: 12px 0 28px;
  max-width: 440px;
}

.zayavka-info__list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.zayavka-info__list li {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  color: #333;
}

.zayavka-info__list li i {
  color: #0057ff;
  font-size: 16px;
}

/* Form side */
.zayavka-form-wrap {
  background: #fff;
  border: 1px solid #e8eaf0;
  border-radius: 16px;
  padding: 36px 32px;
}

.zayavka-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.zayavka-form__group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.zayavka-form__label {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.req {
  color: #e24b4a;
}

.zayavka-form__input,
.zayavka-form__textarea {
  width: 100%;
  padding: 11px 14px;
  border: 1px solid #dde0ea;
  border-radius: 10px;
  font-size: 14px;
  color: #0f0f1a;
  background: #fafbff;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
  font-family: inherit;
  resize: vertical;
}

.zayavka-form__input:focus,
.zayavka-form__textarea:focus {
  border-color: #0057ff;
  background: #fff;
}

.zayavka-form__input--error {
  border-color: #e24b4a !important;
  background: #fff8f8;
}

.zayavka-form__error {
  font-size: 12px;
  color: #e24b4a;
}

.zayavka-form__error--server {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  background: #fff0f0;
  border: 1px solid #f7c1c1;
  border-radius: 8px;
  padding: 10px 14px;
}

/* Button */
.zayavka-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 13px;
  background: #0057ff;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, opacity 0.2s;
  font-family: inherit;
}

.zayavka-btn:hover {
  background: #0047d4;
}

.zayavka-btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

/* Success */
.zayavka-success {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 16px;
  padding: 20px 0;
}

.zayavka-success__icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #e8f4e8;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #3b6d11;
}

.zayavka-success__title {
  font-size: 22px;
  font-weight: 700;
  color: #0f0f1a;
  margin: 0;
}

.zayavka-success__desc {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin: 0;
  max-width: 300px;
}

/* Responsive */
@media (max-width: 900px) {
  .zayavka-wrap {
    grid-template-columns: 1fr;
    gap: 36px;
  }
}

@media (max-width: 480px) {
  .zayavka-form-wrap {
    padding: 24px 18px;
  }
}
</style>