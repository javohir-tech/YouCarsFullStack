<template>
    <div class="container">
        <div>

            <div>
                <h1>Upload</h1>
                <router-link to="upload">
                    <a-button>
                        upload
                    </a-button>
                </router-link>
            </div>

            <h1>Profile</h1>

            <form @submit.prevent="handleEmailRetriew">
                <p>Edit Email</p>
                <div style="margin-bottom: 10px;">
                    <input type="email" v-model="email">
                </div>
                <div>
                    <a-button type="primary" html-type="submit">Saqlash</a-button>
                </div>
            </form>

            <form @submit.prevent="handleUpdateUser">
                <div>
                    <p>Change User</p>
                    <div style="margin-bottom: 10px;">
                        <input type="text" placeholder="username" v-model="username">
                    </div>
                    <div style="margin-bottom: 10px;">
                        <input type="text" placeholder="first_name" v-model="first_name">
                    </div>
                    <div style="margin-bottom: 10px;">
                        <input type="text" placeholder="last_name" v-model="last_name">
                    </div>
                    <div style="margin-bottom: 10px;">
                        <input type="file" @change="handlechange" accept="image/*">
                    </div>

                    <a-button type="primary" html-type="submit">Saqlash</a-button>
                </div>
            </form>
            <div>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
                <p>salom</p>
            </div>
                <p>salom</p>
        </div>
    </div>
</template>

<script setup>
import api from '@/utils/axios';
import { message } from 'ant-design-vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/store/useUserStore';

const userStore = useUserStore()
const email = ref(userStore.email)
const loading = ref(false)
const router = useRouter()

const username = ref("")
const first_name = ref("")
const last_name = ref("")
const photo = ref(null)
const handlechange = (event) => {
    photo.value = event.target.files?.[0]
}

const handleUpdateUser = async () => {
    loading.value = true
    try {
        const formData = new FormData()
        if (photo.value) formData.append('photo', photo.value)
        formData.append('username', username.value)
        formData.append("first_name", first_name.value)
        formData.append("last_name", last_name.value)

        const { data } = await api.put('auth/user/update/', formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        })
        message.success("ozgartirldi")
        photo.value = data.photo
        username.value = data.username
        userStore.username = data.username
        first_name.value = data.first_name
        last_name.value = data.last_name
        console.log(data)
    } catch (error) {
        console.log(error.response)
    } finally {
        loading.value = false
    }
}

const handleEmailRetriew = async () => {
    try {
        const { data } = await api.post("auth/email/",
            {
                old_email: userStore.email,
                email: email.value
            }
        )
        message.success(data.message)
        router.push("email_verify")
        userStore.add_email_edit_token(data.data.token.email_edit_token)
        userStore.add_new_email(email.value)
        console.log(data)
    } catch (error) {
        if (error.response) {
            const errors = error.response.data
            if (errors.old_email) {
                message.error(errors.old_email[0])
            } else if (errors.email) {
                message.error(errors.email[0])
            } else if (errors.dateil) {
                message.error(errors.dateil)
            } else {
                message.error("An error occurred.")
            }

            console.log(error.response)
        } else {
            message.error("No connection to the server.")
            console.log(error)
        }
    } finally {

    }
}
</script>

<style scoped></style>