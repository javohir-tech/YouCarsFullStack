<template>
    <div class="registration-page">
        <div class="registration-container">
            <div class="registration-card">
                <h1 class="title">Забыли пароль?</h1>
                <p class="subtitle">Введите e-mail or username для восстановления</p>

                <a-form :model="formState" :rules="rules" @finish="onFinish" @finishFailed="onFinishFailed"
                    layout="vertical" class="registration-form">
                    <!-- E-mail or username -->
                    <a-form-item name="user_input" class="form-item">
                        <a-input v-model:value="formState.user_input" placeholder="E-mail or Username" size="large"
                            class="custom-input" />
                    </a-form-item>

                    <!-- Submit Button -->
                    <a-form-item class="form-item">
                        <a-button :loading="loading" type="primary" html-type="submit" size="large" block
                            class="submit-button">
                            {{ loading ? "Loading..." : "Восстановить" }}
                        </a-button>
                    </a-form-item>

                    <!-- Login Link -->
                    <div class="login-link">
                        Вспомнили пароль? <router-link to="login">Войти</router-link>
                    </div>
                </a-form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { message } from 'ant-design-vue';
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/utils/axios';
import { notification } from 'ant-design-vue';

const router = useRouter()

const formState = reactive({
    user_input: '',
});

const loading = ref(false)


const rules = {
    user_input: [
        {
            required: true,
            message: 'Пожалуйста, введите email or username',
            trigger: 'blur',
        },
    ],
};

const onFinish = async (values) => {
    loading.value = true
    try {
        const data = await api.post("auth/forget/", {
            user_input: values.user_input
        })
        notification.success({ message: "Success", description: data.data.message })
        router.push("verify")
        // console.log(data)
    } catch (error) {
        if (error.response) {
            const errors = error.response
            console.log(errors)
            if (errors.data.code) {
                message.warning(errors.data.code[0])
            } else if (errors.data.user) {
                message.error(errors.data.user[0])
            } else {
                message.error("An error occurred.")
            }
        } else {
            message.error("No connection to the server.")
        }
    } finally {
        loading.value = false
    }
};

const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
};
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
}

.success-alert {
    background: #D4EDDA;
    border: 1px solid #C3E6CB;
    border-radius: 4px;
    padding: 12px 16px;
    margin-bottom: 24px;
    font-size: 14px;
    color: #155724;
    line-height: 1.5;
}

.registration-form {
    width: 100%;
}

.form-item {
    margin-bottom: 16px !important;
}

.form-item:last-child {
    margin-bottom: 0;
}

.custom-input {
    border-radius: 4px;
    background: #F5F5F5;
    border: 1px solid #F5F5F5;
    font-size: 14px;
    color: #000000;
}

.custom-input:hover,
.custom-input:focus {
    background: #F5F5F5;
    border-color: #D9D9D9;
}

:deep(.ant-input-affix-wrapper) {
    background: #F5F5F5;
    border: 1px solid #F5F5F5;
    border-radius: 4px;
}

:deep(.ant-input-affix-wrapper:hover),
:deep(.ant-input-affix-wrapper:focus),
:deep(.ant-input-affix-wrapper-focused) {
    background: #F5F5F5;
    border-color: #D9D9D9;
}

:deep(.ant-input) {
    background: #F5F5F5;
    font-size: 14px;
    color: #000000;
}

:deep(.ant-input::placeholder) {
    color: #BFBFBF;
}

.submit-button {
    height: 48px;
    font-size: 16px;
    font-weight: 500;
    border-radius: 4px;
    background: #2684E5;
    border: none;
    margin-top: 8px;
}

.submit-button:hover {
    background: #1a6bc4;
}

.login-link {
    text-align: center;
    font-size: 14px;
    color: #000000;
    margin-top: 24px;
}

.login-link a {
    color: #2684E5;
    text-decoration: none;
    font-weight: 500;
}

.login-link a:hover {
    text-decoration: underline;
}

:deep(.ant-form-item-explain-error) {
    font-size: 12px;
    margin-top: 4px;
}

:deep(.ant-form-item) {
    margin-bottom: 0;
}
</style>