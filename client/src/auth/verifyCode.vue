<template>
    <div class="registration-page">
        <div class="registration-container">
            <div class="registration-card">
                <h1 class="title">Подтверждение</h1>
                <p class="subtitle">Введите код из письма отправленного на <strong>{{ email }}</strong></p>

                <a-form :model="formState" @finish="onFinish" layout="vertical" class="registration-form">
                    <!-- Verification Code Inputs -->
                    <div class="code-inputs-wrapper">
                        <input
                            v-for="(digit, index) in code"
                            :key="index"
                            :ref="el => inputRefs[index] = el"
                            v-model="code[index]"
                            type="text"
                            maxlength="1"
                            class="code-input"
                            @input="handleInput(index, $event)"
                            @keydown="handleKeyDown(index, $event)"
                            @paste="handlePaste"
                        />
                    </div>

                    <!-- Timer or Resend Button -->
                    <div class="timer-wrapper">
                        <template v-if="timeLeft > 0">
                            <p class="timer-text">Отправить код повторно через {{ formattedTime }}</p>
                        </template>
                        <template v-else>
                            <a-button type="link" @click="resendCode" :loading="resending" class="resend-button">
                                Отправить повторно
                            </a-button>
                        </template>
                    </div>

                    <!-- Submit Button -->
                    <a-form-item class="form-item">
                        <a-button 
                            :loading="loading" 
                            :disabled="!isCodeComplete"
                            type="primary" 
                            html-type="submit" 
                            size="large"
                            block 
                            class="submit-button"
                        >
                            {{ loading ? "Loading..." : "Подтвердить" }}
                        </a-button>
                    </a-form-item>

                    <!-- Edit Email Link -->
                    <div class="login-link">
                        <router-link to="forget" class="edit-link">Редактировать</router-link>
                    </div>
                </a-form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { message } from 'ant-design-vue';
import { reactive, ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()

// Email prop yoki route params dan olish mumkin
const email = ref('example@mail.com') // Bu yerga haqiqiy emailni qo'yasiz

const code = reactive(['', '', '', ''])
const inputRefs = ref([])
const loading = ref(false)
const resending = ref(false)
const timeLeft = ref(120) // 2 minut = 120 sekund
let timerInterval = null

// Code to'liq kiritilganligini tekshirish
const isCodeComplete = computed(() => {
    return code.every(digit => digit !== '')
})

// Timer formatlash (mm:ss)
const formattedTime = computed(() => {
    const minutes = Math.floor(timeLeft.value / 60)
    const seconds = timeLeft.value % 60
    return `${minutes}:${seconds.toString().padStart(2, '0')}`
})

// Timer boshlash
const startTimer = () => {
    if (timerInterval) {
        clearInterval(timerInterval)
    }
    
    timeLeft.value = 120
    timerInterval = setInterval(() => {
        if (timeLeft.value > 0) {
            timeLeft.value--
        } else {
            clearInterval(timerInterval)
        }
    }, 1000)
}

// Input handling
const handleInput = (index, event) => {
    const value = event.target.value
    
    // Faqat raqam kiritishga ruxsat
    if (!/^\d*$/.test(value)) {
        code[index] = ''
        return
    }
    
    code[index] = value
    
    // Keyingi inputga o'tish
    if (value && index < 3) {
        inputRefs.value[index + 1]?.focus()
    }
}

// Backspace handling
const handleKeyDown = (index, event) => {
    if (event.key === 'Backspace' && !code[index] && index > 0) {
        inputRefs.value[index - 1]?.focus()
    }
}

// Paste handling
const handlePaste = (event) => {
    event.preventDefault()
    const pasteData = event.clipboardData.getData('text').slice(0, 4)
    
    if (/^\d{4}$/.test(pasteData)) {
        pasteData.split('').forEach((digit, index) => {
            code[index] = digit
        })
        inputRefs.value[3]?.focus()
    }
}

// Form submit
const onFinish = async () => {
    loading.value = true
    try {
        const verificationCode = code.join('')
        
        // Bu yerga o'zingizning API logikangizni yozing
        // const { data } = await api.post("auth/verify-code/", {
        //     email: email.value,
        //     code: verificationCode
        // })
        
        console.log('Verification code:', verificationCode)
        message.success('Код подтвержден!')
        
        // Keyingi sahifaga o'tish (masalan, parol o'zgartirish)
        // router.push('/reset-password')
    } catch (error) {
        message.error('Неверный код')
        // Kodni tozalash
        code.forEach((_, index) => {
            code[index] = ''
        })
        inputRefs.value[0]?.focus()
    } finally {
        loading.value = false
    }
}

// Kodni qayta yuborish
const resendCode = async () => {
    resending.value = true
    try {
        // Bu yerga o'zingizning API logikangizni yozing
        // const { data } = await api.post("auth/resend-code/", {
        //     email: email.value
        // })
        
        message.success('Код отправлен повторно!')
        
        // Kodni tozalash
        code.forEach((_, index) => {
            code[index] = ''
        })
        inputRefs.value[0]?.focus()
        
        // Timer qayta boshlash
        startTimer()
    } catch (error) {
        message.error('Ошибка при отправке кода')
    } finally {
        resending.value = false
    }
}

// Component mount bo'lganda timer boshlash
onMounted(() => {
    startTimer()
    inputRefs.value[0]?.focus()
})

// Component unmount bo'lganda timerni to'xtatish
onUnmounted(() => {
    if (timerInterval) {
        clearInterval(timerInterval)
    }
})
</script>

<style scoped>
.registration-page {
    min-height: calc(100vh - 200px);
    display: flex;
    align-items: center;
    justify-content: center;
    background: #F5F5F5;
    padding: 40px 20px;
}

.registration-container {
    width: 100%;
    max-width: 550px;
    margin: 0 auto;
}

.registration-card {
    background: white;
    padding: 48px 40px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.title {
    font-size: 28px;
    font-weight: 700;
    color: #000000;
    text-align: center;
    margin-bottom: 8px;
}

.subtitle {
    font-size: 14px;
    color: #8C8C8C;
    text-align: center;
    margin-bottom: 32px;
    line-height: 1.5;
}

.subtitle strong {
    color: #000000;
    font-weight: 500;
}

.registration-form {
    width: 100%;
}

.code-inputs-wrapper {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-bottom: 24px;
}

.code-input {
    width: 64px;
    height: 64px;
    border: 1px solid #D9D9D9;
    border-radius: 8px;
    text-align: center;
    font-size: 24px;
    font-weight: 600;
    color: #000000;
    background: #F5F5F5;
    outline: none;
    transition: all 0.3s;
}

.code-input:focus {
    border-color: #2684E5;
    background: #FFFFFF;
    box-shadow: 0 0 0 2px rgba(38, 132, 229, 0.1);
}

.code-input:hover {
    border-color: #2684E5;
}

.timer-wrapper {
    text-align: center;
    margin-bottom: 24px;
    min-height: 32px;
}

.timer-text {
    font-size: 14px;
    color: #8C8C8C;
    margin: 0;
}

.resend-button {
    font-size: 14px;
    color: #2684E5;
    padding: 0;
    height: auto;
}

.resend-button:hover {
    color: #1a6bc4;
}

.form-item {
    margin-bottom: 16px !important;
}

.form-item:last-child {
    margin-bottom: 0;
}

.submit-button {
    height: 48px;
    font-size: 16px;
    font-weight: 500;
    border-radius: 4px;
    background: #2684E5;
    border: none;
}

.submit-button:hover:not(:disabled) {
    background: #1a6bc4;
}

.submit-button:disabled {
    background: #D9D9D9;
    cursor: not-allowed;
}

.login-link {
    text-align: center;
    font-size: 14px;
    color: #000000;
    margin-top: 24px;
}

.edit-link {
    color: #2684E5;
    text-decoration: none;
    font-weight: 500;
    cursor: pointer;
}

.edit-link:hover {
    text-decoration: underline;
}

:deep(.ant-form-item) {
    margin-bottom: 0;
}

/* Raqam inputlari uchun spinner olib tashlash */
.code-input::-webkit-outer-spin-button,
.code-input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}


</style>