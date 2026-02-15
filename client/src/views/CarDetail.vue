<template>
    <div class="container">
        <a-breadcrumb class="bread_crumb" separator=">">
            <a-breadcrumb-item><router-link to="/">Главная</router-link></a-breadcrumb-item>
            <a-breadcrumb-item><router-link to="/katalog">Каталог</router-link></a-breadcrumb-item>
            <a-breadcrumb-item>{{ car_data.marka }} {{ car_data.car_model }}</a-breadcrumb-item>
        </a-breadcrumb>
        <div class="car_banner">
            <a-row :gutter="[16, 24]" aling="bottom" align="strech">
                <a-col class="gutter-row car_images" :md="24" :lg="14">
                    <div class="banner">
                        <swiper :style="{
                            '--swiper-navigation-color': '#fff',
                            '--swiper-pagination-color': '#fff',
                        }" :spaceBetween="10" :navigation="{
                            nextEl: '.custom-next',
                            prevEl: '.custom-prev'
                        }" :thumbs="{ swiper: thumbsSwiper }" :modules="modules" class="mySwiper2">
                            <swiper-slide v-for="image in car_data.images" :key="image.id">
                                <a-skeleton-image v-if="image_loader" />
                                <img :src="image.image" v-show="!image_loader" @load="onLoad" @error="onError" />
                            </swiper-slide>
                            <div class="navigation_btn">
                                <button class="custom-prev">
                                    <ArrowLeftOutlined class="naviagtion_btn" />
                                </button>
                                <button class="custom-next">
                                    <ArrowRightOutlined class="naviagtion_btn" />
                                </button>
                            </div>
                        </swiper>
                        <swiper @swiper="setThumbsSwiper" :spaceBetween="10" :slidesPerView="4" :freeMode="true"
                            :watchSlidesProgress="true" :modules="modules" class="mySwiper">
                            <swiper-slide v-for="image in car_data.images" :key="image.id">
                                <a-skeleton-image v-if="image_loader" />
                                <img :src="image.image" v-show="!image_loader" @load="onLoad" @error="onError" />
                            </swiper-slide>
                        </swiper>
                    </div>
                </a-col>
                <a-col class="gutter-row " :xs="24" :lg="10">
                    <div class="banner">
                        <div v-if="car_data_loader" class="skeleton">
                            <a-skeleton active />
                            <a-skeleton active />
                            <a-skeleton active />
                        </div>
                        <div v-else>
                            <div class="car_info">
                                <h2 class="car_name">{{ car_data.marka }} {{ car_data.car_model }}</h2>
                                <div class="car_header">
                                    <div class="car_view">
                                        <p class="title">{{ formatDate(car_data.created_time) }}</p>
                                        <p class="title">
                                            {{ car_data.views }}
                                            <EyeOutlined />
                                        </p>
                                        <p>
                                            <HeartFilled @click="like ? handleDisLike(route.params.id) : handleLike(route.params.id) " class="car_like" :class="like ? 'car_liked' : '' " />
                                        </p>
                                    </div>
                                    <div class="car_aviability" v-if="car_data.availability === 'in_stock'">
                                        <CheckOutlined class="aviability_icon" />
                                        <p class="subtitle">
                                            В наличии
                                        </p>
                                    </div>
                                    <div class="car_aviability" v-else-if="car_data.availability === 'on_order'">
                                        <ExclamationOutlined class="aviability_icon in_order_icon" />
                                        <p class="subtitle">
                                            Под заказ
                                        </p>
                                    </div>
                                </div>

                                <div class="under_line">
                                </div>

                                <div class="car_info_data">
                                    <div class="car_info_item">
                                        <p class="title">Марка</p>
                                        <p class="subtitle">{{ car_data.marka }}</p>
                                    </div>
                                    <div class="car_info_item">
                                        <p class="title">Модель</p>
                                        <p class="subtitle">{{ car_data.car_model }}</p>
                                    </div>
                                    <div class="car_info_item">
                                        <p class="title">Год выпуска</p>
                                        <p class="subtitle">{{ car_data.year }}</p>
                                    </div>
                                    <div class="car_info_item">
                                        <p class="title">Пробег</p>
                                        <p class="subtitle">{{ car_data.milage }} км</p>
                                    </div>
                                    <div class="car_info_item">
                                        <p class="title">Цвет</p>
                                        <p class="subtitle">{{ car_data.color }}</p>
                                    </div>
                                    <div class="car_info_item">
                                        <p class="title">Двигатель</p>
                                        <p class="subtitle">{{ car_data.displacement }} л / {{ car_data.power }} л.с</p>
                                    </div>
                                </div>
                            </div>
                            <div class="car_price">
                                <p class="price_text">Цена:</p>
                                <p class="price">{{ car_data.price }}$</p>
                            </div>
                            <div class="author_info">
                                <div class="user_card">
                                    <div class="user">
                                        <div class="author_profile">
                                            <img
                                                :src="`https://api.dicebear.com/9.x/initials/svg?seed=${car_data.author}}`">
                                        </div>
                                        <div class="author">
                                            <p class="author_name">{{ car_data.author }}</p>
                                            <p class="title">Рейтинг 5.0</p>
                                        </div>
                                    </div>
                                    <div class="message">
                                        <router-link to="/">
                                            <MessageOutlined class="message_icon" />
                                            <p class="subtitle">Написать</p>
                                        </router-link>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </a-col>
            </a-row>
        </div>

        <div class="description">
            <h2>Описание</h2>
            <div v-if="car_data_loader">
                <a-skeleton active />
            </div>
            <p v-else>
                {{ car_data.description }}
            </p>
        </div>

        <div class="car_info_under">
            <a-row :gutter="[16, 24]" align="stretch">
                <a-col class="gutter-row" :xs="24" :lg="12">
                    <div class="car_under_box">
                        <h2 class="header">Технические характеристики</h2>
                        <div v-if="car_data_loader">
                            <a-skeleton active />
                        </div>
                        <div v-else class="car_info_flex">
                            <div class="item">
                                <a-flex justify="space-between">
                                    <p class="title">Марка</p>
                                    <p class="subtitle">{{ car_data.marka }}</p>
                                </a-flex>
                                <a-flex justify="space-between">
                                    <p class="title">Модель</p>
                                    <p class="subtitle">{{ car_data.car_model }}</p>
                                </a-flex>
                                <a-flex justify="space-between">
                                    <p class="title">Год выпуска</p>
                                    <p class="subtitle">{{ car_data.year }}</p>
                                </a-flex>
                                <a-flex justify="space-between">
                                    <p class="title">Пробег</p>
                                    <p class="subtitle">{{ car_data.milage }} км</p>
                                </a-flex>
                                <a-flex justify="space-between">
                                    <p class="title">Цвет</p>
                                    <p class="subtitle">{{ car_data.color }}</p>
                                </a-flex>
                                <a-flex justify="space-between">
                                    <p class="title">Двигатель</p>
                                    <p class="subtitle">{{ car_data.displacement }} л / {{ car_data.power }} л.с</p>
                                </a-flex>
                            </div>
                            <div class="item">
                                <a-flex justify="space-between">
                                    <p class="title">Страна</p>
                                    <p class="subtitle">{{ car_data.country }}</p>
                                </a-flex>
                                <a-flex justify="space-between">
                                    <p class="title">Коробка</p>
                                    <p class="subtitle">{{ getDriveType(car_data.drive_type) }}</p>
                                </a-flex>
                                <a-flex justify="space-between">
                                    <p class="title">Топливо</p>
                                    <p class="subtitle">{{ getDriveType(car_data.fuel) }}</p>
                                </a-flex>
                            </div>
                        </div>
                    </div>
                </a-col>
                <a-col class="gutter-row" :xs="24" :lg="12">
                    <div class="car_under_box">
                        <h2 class="header">Задайте вопрос продавцу</h2>
                        <div v-if="car_data_loader">
                            <a-skeleton active />
                        </div>
                        <div v-else class="question_btns">
                            <button class="question_btn">Здравствуйте</button>
                            <button class="question_btn">Какой срок доставки?</button>
                            <button class="question_btn">птс ОРИГИНАЛ?</button>
                            <button class="question_btn">Пробег оригинал?</button>
                            <button class="question_btn">Какой бензин?</button>
                        </div>
                    </div>
                </a-col>
            </a-row>
        </div>

        <div class="similar_section">
            <div class="section_header">
                <h1>Похожие</h1>
            </div>
            <div class="similar_cars">
                <a-row :gutter="[16, 24]">
                    <a-col v-if="similar_loading" class="gutter-row" :xs="24" :md="12" :lg="8"
                        v-for="_ in new Array(3).fill(1)">
                        <a-skeleton active />
                    </a-col>
                    <a-col v-else class="gutter-row" :xs="24" :md="12" :lg="8" v-for="car in similar_cars"
                        :key="car.id">
                        <CarCard @click="handleNavigate" :id="car.id" :model="car.car_model" :like="car.me_liked"
                            :images="car.images" :marka="car.marka" :price="car.price" :milage="car.milage"
                            :displacement="car.displacement" :year="car.year" :transmission_type="car.transmission_type"
                            :power="car.power" :fuel="car.fuel" :drive_type="car.drive_type" :country="car.country" />
                    </a-col>
                </a-row>
            </div>
        </div>

        <CallCard />
    </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
// Import Swiper Vue.js components
import { Swiper, SwiperSlide } from 'swiper/vue';

// Import Swiper styles
import 'swiper/css';

import 'swiper/css/free-mode';
import 'swiper/css/navigation';
import 'swiper/css/thumbs';

// import required modules
import { FreeMode, Navigation, Thumbs } from 'swiper/modules';
import { ArrowLeftOutlined, ArrowRightOutlined, CheckOutlined, ExclamationOutlined, EyeOutlined, HeartFilled, MessageOutlined } from '@ant-design/icons-vue';
import api from '@/utils/axios';
import { CallCard, CarCard } from '@/components';
import LikeManager from '@/Hooks/LikeManager';

const { like , handleLike , handleDisLike } = LikeManager()



const modules = [FreeMode, Navigation, Thumbs]

const route = useRoute()
// refs
const thumbsSwiper = ref(null)
const car_data = ref([])
const similar_cars = ref([])

//  loaders
const car_data_loader = ref(false)
const image_loader = ref(true)
const similar_loading = ref(false)

// methods
const setThumbsSwiper = (swiper) => {
    thumbsSwiper.value = swiper
}

const onLoad = () => {
    image_loader.value = false
}

const onError = () => {
    image_loader.value = false
}

const getDriveType = (type) => {
    const types = {
        'FWD': 'Передний',
        'RWD': 'Задний',
        'AWD': 'Полный'
    }
    return types[type] || type
}

const formatDate = (dateString) => {
    if (!dateString) return ''
    const date = new Date(dateString)
    const months = [
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    ]
    const day = date.getDate()
    const month = months[date.getMonth()]
    const year = date.getFullYear()
    return `${day} ${month} ${year}`
}


const handleGetSimilarCar = async () => {
    similar_loading.value = true
    try {
        const { data } = await api.get(`/cars/car/similar/${route.params.id}/`)
        similar_cars.value = data
    } catch (error) {
        console.log(error.response || error)
    } finally {
        similar_loading.value = false
    }
}

const handleGetCar = async () => {
    car_data_loader.value = true
    try {
        const { data } = await api.get(`/cars/car/${route.params.id}/`)
        like.value = data.data.me_liked
        car_data.value = data.data
    } catch (error) {
        console.log(error.response || error)
    } finally {
        car_data_loader.value = false
    }
}

const handleNavigate = () => {
    handleGetCar()
}


onMounted(() => {
    handleGetCar()
    handleGetSimilarCar()
})

</script>

<style scoped>
.bread_crumb {
    margin: 15px 0;
}

/*  SWIPER STYLE */
.banner {
    height: 100%;
}

.swiper {
    width: 100%;
    height: 100%;
}

.swiper-slide {
    text-align: center;
    font-size: 18px;
    background: rgba(90, 90, 90, 1);

    /* Center slide text vertically */
    display: flex;
    justify-content: center;
    align-items: center;
}

.swiper-slide img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.swiper {
    width: 100%;
    height: 300px;
    margin-left: auto;
    margin-right: auto;
}

.swiper-slide {
    background-size: cover;
    background-position: center;
}

.mySwiper2 {
    height: 420px;
    width: 100%;
    border-radius: 10px;
}

.mySwiper {
    height: 100px;
    box-sizing: border-box;
    padding: 10px 0;
}

.mySwiper .swiper-slide {
    width: 20%;
    height: 100%;
    opacity: 0.4;
    border-radius: 10px;
}

.mySwiper .swiper-slide-thumb-active {
    opacity: 1;
}

.swiper-slide img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 10px;
}

.navigation_btn {
    position: absolute;
    top: 50%;
    width: 100%;
    display: flex;
    justify-content: space-between;
    z-index: 2;
}

.custom-next,
.custom-prev {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: white;
    border: none;
    cursor: pointer;
    margin: 10px;
}

.custom-next:hover {
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
}

.naviagtion_btn {
    color: #989898;
}

.car_like {
    color: #989898;
    font-size: 20px;
    cursor: pointer;
}

.car_liked {
    color : #FF0000;
}

/*  car style */
.car_info {
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
    padding: 20px;
    border-top-right-radius: 15px;
    border-top-left-radius: 15px;
}

.skeleton {
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
    padding: 20px;
    border-radius: 15px;
    height: 100%;
}

.car_name {
    font-weight: 500;
    font-size: 25px;
    color: rgba(41, 56, 67, 1);
}

.title {
    font-weight: 400;
    font-size: 14px;
    color: rgba(152, 152, 152, 1);
}

.subtitle {
    font-weight: 400;
    font-size: 15px;
    color: rgba(41, 56, 67, 1);
}

.car_header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    p {
        margin: 0;
    }
}

.car_view {
    display: flex;
    gap: 15px;
    align-items: center;
}

.car_aviability {
    display: flex;
    align-items: center;
    gap: 10px;
}

.aviability_icon {
    color: rgba(7, 197, 83, 1);
    width: 25px;
    height: 25px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(221, 250, 220, 1);
    border-radius: 100%;
}

.in_order_icon {
    color: rgba(245, 171, 48, 1);
    background-color: rgba(255, 235, 201, 1);
}

.under_line {
    height: 2px;
    margin: 10px 0;
    background-color: rgba(240, 240, 240, 1);
}

.car_info_data {
    width: 50%;
}

.car_info_item {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.car_price {
    background-color: rgba(38, 132, 229, 1);
    padding: 30px 15px;
    display: flex;
    gap: 40px;

    p {
        margin: 0;
    }
}

.car_price {
    color: rgba(255, 255, 255, 1);
    font-weight: 700;
}

.price_text {
    font-size: 16px;
}

.price {
    font-size: 20px;
}

.author_info {
    padding: 15px 20px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
    border-bottom-left-radius: 15px;
    border-bottom-right-radius: 15px;
}

.user {
    display: flex;
    align-items: center;
    gap: 20px;
}

.user_card {
    padding: 10px 30px;
    border-radius: 10px;
    border: 1px rgba(238, 238, 238, 1) solid;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;

}

.author_profile {
    width: 48px;
    height: 48px;

    img {
        border-radius: 100%;
    }
}

.author_name {
    font-size: 16px;
    margin-bottom: 8px;
}

.message_icon {
    font-size: 24px;
}

.message {
    height: 100%;
}

.message a {
    display: flex;
    align-items: center;
    height: 100%;
    padding-left: 30px;
    border-left: rgba(240, 240, 240, 1) solid 1px;
    gap: 20px;

    p {
        margin: 0;

    }
}

.description {
    padding: 15px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
    border-radius: 10px;
    margin-top: 20px;

    h2 {
        font-weight: 500;
        font-size: 23px;
        color: rgba(41, 56, 67, 1);
    }

    p {
        font-weight: 400;
        font-size: 16px;
        color: rgba(90, 90, 90, 1);
        margin: 0;
    }
}

.car_info_under {
    margin-top: 20px;
}

.car_under_box {
    padding: 15px 20px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
    border-radius: 15px;
    height: 100%;
}

.item {
    flex: 1;
    height: 100%;
}

.header {
    font-weight: 500;
    font-size: 23px;
    color: rgba(41, 56, 67, 1);
    margin-bottom: 15px;
}

.question_btns {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.question_btn {
    border-radius: 10px;
    padding: 10px 15px;
    border: none;
    color: rgba(255, 255, 255, 1);
    background-color: rgba(41, 56, 67, 1);
    cursor: pointer;
    transition: all 0.3s ease-in-out;
}

.question_btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
}

.car_info_flex {
    display: flex;
    gap: 100px;
}

.similar_section {
    margin-top: 50px;
}

.section_header {
    font-weight: 500;
    font-size: 30px;
    color: rgba(1, 1, 1, 1);
}

@media(max-width : 992px) {
    .car_info_data {
        width: 75%;
    }
}

@media(max-width : 768px) {
    .mySwiper2 {
        height: 200px;
    }

    .car_info_flex {
        flex-direction: column;
        gap: 0;
    }

    .mySwiper {
        height: 75px;
    }

    .car_info_data {
        width: 75%;
    }

    .message_icon {
        font-size: 18px;
    }

    .author_profile {
        width: 42px;
        height: 42px;
    }
}

@media(max-width : 576px) {
    .car_info_data {
        width: 100%;
    }

    .author_profile {
        width: 32px;
        height: 32px;
    }

    .message_icon {
        font-size: 16px;
    }

    .user_card {
        padding: 10px;
    }
}
</style>