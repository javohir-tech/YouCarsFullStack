<template>
    <div class="registration-page">
        <div class="registration-container">
            <div class="registration-card">
                <h1 class="title">Новый пароль</h1>
                <p class="subtitle">Введите новый пароль для вашего аккаунта</p>

                <a-form :model="formState" :rules="rules" @finish="onFinish" @finishFailed="onFinishFailed"
                    layout="vertical" class="registration-form">
                    <!-- Новый пароль -->
                    <a-form-item name="password" class="form-item">
                        <a-input-password v-model:value="formState.password" placeholder="Новый пароль" size="large"
                            class="custom-input" />
                    </a-form-item>

                    <!-- Повторите пароль -->
                    <a-form-item name="confirmPassword" class="form-item">
                        <a-input-password v-model:value="formState.confirmPassword" placeholder="Повторите пароль"
                            size="large" class="custom-input" />
                    </a-form-item>

                    <!-- Submit Button -->
                    <a-form-item class="form-item">
                        <a-button :loading="loading" type="primary" html-type="submit" size="large" block
                            class="submit-button">
                            {{ loading ? "Loading..." : "Сохранить пароль" }}
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
import axios from 'axios';

const router = useRouter()

const formState = reactive({
    password: '',
    confirmPassword: '',
});

const loading = ref(false)

const rules = {
    password: [
        {
            required: true,
            message: 'Пожалуйста, введите пароль',
            trigger: 'blur',
        },
        {
            min: 8,
            message: 'Пароль должен содержать минимум 8 символов',
            trigger: 'blur',
        },
    ],
    confirmPassword: [
        {
            required: true,
            message: 'Пожалуйста, повторите пароль',
            trigger: 'blur',
        },
        {
            validator: (rule, value) => {
                if (value !== formState.password) {
                    return Promise.reject('Пароли не совпадают');
                }
                return Promise.resolve();
            },
            trigger: 'blur',
        },
    ],
};

const onFinish = async (values) => {
    loading.value = true
    try {
        const edit_password_token = localStorage.getItem("edit_password_token")
        const { data } = await axios.put(`${import.meta.env.VITE_API_URL}/auth/new_password/`,
            {
                password: values.password,
                confirm_password: values.confirmPassword
            },
            {
                headers: {
                    Authorization: `Bearer ${edit_password_token}`
                }
            }
        )
        localStorage.removeItem("edit_password_token")
        // console.log(data)
        message.success(data.message)
        router.push("login")
    } catch (error) {
        if (error.response) {
            const errors = error.response.data
            if (errors.password) {
                message.error(errors.password[0])
            } else if (errors.confirm_password) {
                message.error(errors.confirm_password[0])
            } else if (errors.detail) {
                message.error(errors.detail)
            } else {
                message.error('An error occurred.')
            }
            console.log(error.response)
        } else {
            message.error('No connection to the server')
            console.log(error)
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