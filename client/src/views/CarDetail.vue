<template>
    <div class="container">
        <a-breadcrumb class="bread_crumb" separator=">">
            <a-breadcrumb-item><router-link to="/">Главная</router-link></a-breadcrumb-item>
            <a-breadcrumb-item><router-link to="/katalog">Каталог</router-link></a-breadcrumb-item>
            <a-breadcrumb-item>{{ car_data.marka }} {{ car_data.car_model }}</a-breadcrumb-item>
        </a-breadcrumb>
        <div class="car_banner">
            <a-row :gutter="[16, 24]" aling="bottom">
                <a-col class="gutter-row car_images" :xs="24" :md="14">
                    <swiper :style="{
                        '--swiper-navigation-color': '#fff',
                        '--swiper-pagination-color': '#fff',
                    }" :spaceBetween="10" :navigation="{
                        nextEl: '.custom-next',
                        prevEl: '.custom-prev'
                    }" :thumbs="{ swiper: thumbsSwiper }" :modules="modules" class="mySwiper2">
                        <swiper-slide v-for="image in car_data.images" :key="image.id">
                            <img :src="image.image" />
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
                            <img :src="image.image" />
                        </swiper-slide>
                    </swiper>
                </a-col>
                <a-col class="gutter-row " :xs="24" :md="10">
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
                                    <HeartFilled class="car_like" />
                                </p>
                            </div>
                            <div class="car_aviability">
                                <CheckOutlined class="aviability_icon" />
                                <p class="subtitle">В наличии</p>
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
                        <p class="price">19 000 $</p>
                    </div>
                    <div class="author_info">
                        <div class="user_card">
                            <div class="author_profile">
                                <img :src="`https://api.dicebear.com/9.x/initials/svg?seed=${car_data.author}}`">
                            </div>
                            <div class="author">
                                <p>{{ car_data.author }}</p>
                                <p class="title">Рейтинг 5.0</p>
                            </div>
                        </div>
                    </div>
                </a-col>
            </a-row>
        </div>
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
import { ArrowLeftOutlined, ArrowRightOutlined, CheckOutlined, EyeOutlined, HeartFilled } from '@ant-design/icons-vue';
import api from '@/utils/axios';

const modules = [FreeMode, Navigation, Thumbs]

const route = useRoute()
// refs
const thumbsSwiper = ref(null)
const car_data = ref([])

// methods
const setThumbsSwiper = (swiper) => {
    thumbsSwiper.value = swiper
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

const formatNumber = (num) => {
    if (!num) return '0'
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
}

const handleGetCar = async () => {
    try {
        const { data } = await api.get(`/cars/car/${route.params.id}/`)
        console.log(data)
        car_data.value = data.data
    } catch (error) {
        console.log(error.response || error)
    }
}


onMounted(() => {
    handleGetCar()
})

</script>

<style scoped>
/*  SWIPER STYLE */

.swiper {
    width: 100%;
    height: 100%;
}

.swiper-slide {
    text-align: center;
    font-size: 18px;
    background: #444;

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

/*  car style */
.car_info {
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
    padding: 20px;
    border-top-right-radius: 15px;
    border-top-left-radius: 15px;
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

.user_card {
    padding: 10px 30px;
    border-radius: 10px;
    border: 1px rgba(238, 238, 238, 1) solid;
    display: flex;
    align-items: center;
    gap: 20px;

}

.author_profile{
    width: 48px;
    height: 48px;
    img{
        border-radius: 100%;
    }
}

@media(max-width : 768px) {
    .mySwiper2 {
        height: 200px;
    }

    .mySwiper {
        height: 75px;
    }
}
</style>