<template>
    <header class="navbar">
        <!-- ///////////////////////////////// -->
        <!-- ////////// UNDER NAVBAR /////// -->
        <!-- /////////////////////////////// -->
        <div class="under_navbar">
            <div class="container">
                <Row align="center">
                    <Col :span="14">
                        <ul class="menu_list">
                            <li><router-link to="/">Главная</router-link></li>
                            <li><router-link to="/">Каталог</router-link></li>
                            <li><router-link to="/">О нас</router-link></li>
                            <li><router-link to="/">Новости</router-link></li>
                            <li><router-link to="/">Контакты</router-link></li>
                        </ul>
                    </Col>
                    <Col :span="10">
                        <div class="under_rigth">
                            <div class="icons">
                                <a href="#">
                                    <InstagramOutlined class="icon" />
                                </a>
                                <a href="#">
                                    <WhatsAppOutlined class="icon" />
                                </a>
                                <a href="#">
                                    <LinkedinOutlined class="icon" />
                                </a>
                            </div>
                            <div>
                                <a href="#">
                                    <PhoneOutlined class="icon" />
                                    <span> +77 123 29 04</span>
                                </a>
                            </div>
                            <div>
                                <a href="#">
                                    <MailOutlined class="icon" />
                                    <span> suvonovjavohir625@gmail.com</span>
                                </a>
                            </div>
                            <div>
                                <a-select ref="select" v-model:value="value1" style="width: 100px" @focus="focus"
                                    @change="handleChange">
                                    <a-select-option value="ru">RU</a-select-option>
                                    <a-select-option value="en">EN</a-select-option>
                                    <a-select-option value="uz">UZ</a-select-option>
                                </a-select>
                            </div>
                        </div>
                    </Col>
                </Row>
            </div>
        </div>
        <!-- ///////////////////////////////// -->
        <!-- ////////// BOTTOM NAVBAR /////// -->
        <!-- /////////////////////////////// -->
        <div class="bottom_navbar">
            <div class="container">
                <Row align="middle">
                    <Col :span="19">
                        <div class="bottom_left">
                            <div class="banner">
                                <router-link to="/">
                                    <span class="you">You</span>
                                    <span class="car">Car</span>
                                </router-link>
                            </div>
                            <div class="dropdown-wrapper">
                                <div>
                                    <span><router-link to="/">Автомобили</router-link></span>
                                    <SwapRightOutlined class="avto_icon" />
                                </div>
                                <div>
                                    <span><router-link to="/">Коммерческий транспорт</router-link></span>
                                    <SwapRightOutlined class="avto_icon" />
                                </div>
                                <div>
                                    <span><router-link to="/">Мотоциклы</router-link></span>
                                    <SwapRightOutlined class="avto_icon" />
                                </div>
                            </div>
                            <div class="search">
                                <a-input-search v-model:value="value" placeholder="input search text"
                                    style="width: 400px" />
                            </div>
                            <div class="message">
                                <router-link to="/">
                                    <a-badge count="0">
                                        <CommentOutlined class="messanger" />
                                    </a-badge>
                                </router-link>
                            </div>
                        </div>
                    </Col>
                    <Col :span="5">
                        <div class="bottom_rigth" v-if="userStore.access_token">
                            <router-link to="profile">
                                <div class="avatar">
                                    <p>{{ userStore.username }}</p>
                                    <a-spin v-if="loading" />
                                    <img v-show="!loading" :src="userStore.avatarUrl" @load="onLoad" @error="onError"
                                        alt="avatar image">
                                </div>
                            </router-link>
                        </div>
                        <div class="bottom_rigth" v-else>
                            <Button>
                                <router-link to="login">
                                    Войти
                                </router-link>
                            </Button>
                            <Button type="primary">
                                <router-link to="singup">
                                    Регистрация
                                </router-link>
                            </Button>
                        </div>
                    </Col>
                </Row>
            </div>
        </div>
    </header>
</template>

<script setup>
import { Button, Row, Col, Collapse } from 'ant-design-vue';
import { CommentOutlined, InstagramOutlined, LinkedinOutlined, MailOutlined, PhoneOutlined, SwapRightOutlined, WhatsAppOutlined } from "@ant-design/icons-vue"
import { ref } from 'vue';
import { useUserStore } from '@/store/useUserStore';

const userStore = useUserStore()
const value1 = ref('RU');
const value = ref("")
const loading = ref(true)
const focus = () => {
    console.log('focus');
};

const handleChange = value => {
    console.log(`selected ${value}`);
};

const onLoad = () => {
    loading.value = false
}

const onError = () => {
    loading.value = false
}

</script>

<style scoped>
/* UNDER NAVBAR */
.under_navbar {
    background-color: #F6F6F6;
    padding: 15px 0;
}


.menu_list {
    display: flex;
    height: 100%;
    gap: 15px;
    padding-left: 0;
    margin-bottom: 0;
    align-items: center;

    li {
        list-style: none;
        font-weight: 500;
        font-size: 14px;
        color: #434343;

        a {
            color: inherit;
        }
    }
}

.under_rigth {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 20px;
    justify-content: space-between;

    span {
        font-weight: 400;
        color: #989898;
        font-size: 14px;
    }
}

.under_navbar>div {
    flex: 1;
}

.icons {
    display: flex;
    gap: 10px;
    align-items: center;
}

.icon {
    font-size: 18px;
    color: #989898;
}

/* BUTTON NAVBAR */
.bottom_navbar {
    padding: 20px 0;
    background-color: #FFFFFF;
    box-shadow: 0 4px 6px -2px rgba(0, 0, 0, 0.15);
}

.banner {
    span {
        font-size: 30px;
        font-weight: 700;
    }

    .you {
        color: #2684E5;
    }

    .car {
        color: #010101;
    }
}

.bottom_left {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.messanger {
    font-size: 20px;
}

.bottom_rigth {
    display: flex;
    align-items: center;
    gap: 10px;
    justify-content: end;
}

/* Dropdown wrapper styling */
.dropdown-wrapper {
    display: flex;
    gap: 15px;

}

.dropdown-wrapper>div {
    display: flex;
    align-items: center;
    gap: 4px;

    a {
        color: inherit;
    }

    span {
        font-weight: 400;
        font-size: 16px;
        color: #010101;
    }
}

.avto_icon {
    color: #2684E5 !important;
}

.avatar {
    display: flex;
    align-items: center;
    gap: 15px;

    p {
        margin-bottom: 0;
        color: #293843ed;
        font-size: 14px;
        font-weight: 400;
    }

    img {
        width: 32px;
        height: 32px;
        border-radius: 100%;
    }
}
</style>