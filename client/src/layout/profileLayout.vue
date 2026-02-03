<template>
    <div class="container">
        <a-row :gutter="[16, 24]" class="profile_container">
            <a-col class="gutter-row" :span="6">
                <div class="gutter-box profile_sidebar">
                    <div class="profile_info">
                        <a-flex gap="middle" align="center">
                            <div class="avatar">
                                <img :src="userStore.avatarUrl" alt="">
                            </div>
                            <div class="user_info">
                                <h3>
                                    {{ userStore.username }}
                                </h3>
                                <p>Рейтинг 5.0</p>
                            </div>
                        </a-flex>

                        <div class="under_line"></div>

                        <div class="user_email">
                            <a-flex justify="space-between" align="center">
                                <p>
                                    E-mail
                                </p>
                                <p>
                                    <a href="#">Khamzat.arslanaliyev@mail.ru</a>
                                </p>
                            </a-flex>
                            <a-flex justify="space-between" align="center">
                                <p>
                                    Тариф
                                </p>
                                <p>
                                    <a href="#"><InfoCircleOutlined /> Базовый тариф</a>
                                </p>
                            </a-flex>
                        </div>

                        <div class="profile_routes">
                            <router-link to="/" class="profile_route">
                                <OrderedListOutlined />
                                <p>
                                    Избранное
                                </p>
                            </router-link> 
                        </div>
                    </div>
                </div>
            </a-col>
            <a-col class="gutter-row" :span="18">
                <div class="gutter-box">
                    <RouterView />
                </div>
            </a-col>
        </a-row>
    </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import { useUserStore } from '@/store/useUserStore';

/////////////////////////// ICONS //////////////////
import { InfoCircleOutlined, OrderedListOutlined } from "@ant-design/icons-vue"

const userStore = useUserStore()


</script>

<style scoped>
.profile_container {
    margin-top: 20px;
}

.profile_sidebar {
    background-color: red;
    padding: 20px;
    border-radius: 10px;
}

.avatar {
    width: 36px;
    height: 36px;

    img {
        border-radius: 100%;
    }
}

.user_info {
    padding-bottom: 20px;

    h3 {
        border-radius: 700;
        font-size: 15px;
        color: #293843;
    }

    p {
        margin: 0;
        font-weight: 400;
        font-size: 14px;
        color: #5A5A5A;
    }
}

.under_line {
    height: 1.5px;
    border-radius: 10px;
    background-color: #F0F0F0;
}

.user_email {
    padding-top: 20px;
}

.profile_route{
    padding: 15px;
    background-color: blue;
    border-radius: 10px;
    display: flex;
    gap: 10px;
    align-items: center;
    p{
        margin: 0;
    }
}
</style>