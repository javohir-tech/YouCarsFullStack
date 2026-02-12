<template>
    <div class="container">
        <a-breadcrumb class="bread_crumb" separator=">">
            <a-breadcrumb-item><router-link to="/">Главная</router-link></a-breadcrumb-item>
            <a-breadcrumb-item><router-link to="/katalog">Каталог</router-link></a-breadcrumb-item>
            <a-breadcrumb-item>Каталог</a-breadcrumb-item>
        </a-breadcrumb>
        <div class="car_banner">
            <a-row :gutter="[16, 24]">
                <a-col class="gutter-row car_images" :xs="24" :md="13">
                    <swiper :style="{
                        '--swiper-navigation-color': '#fff',
                        '--swiper-pagination-color': '#fff',
                    }" :loop="true" :spaceBetween="10" :navigation="{
                        nextEl: '.custom-next',
                        prevEl: '.custom-prev'
                    }" :thumbs="{ swiper: thumbsSwiper }" :modules="modules" class="mySwiper2">
                        <swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-1.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-2.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-3.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-4.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-5.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-6.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-7.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-8.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-9.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-10.jpg" /></swiper-slide>
                        <div class="navigation_btn">
                            <button class="custom-prev">
                                <ArrowLeftOutlined class="naviagtion_btn" />
                            </button>
                            <button class="custom-next">
                                <ArrowRightOutlined class="naviagtion_btn" />
                            </button>
                        </div>
                    </swiper>
                    <swiper :loop="true" @swiper="setThumbsSwiper" :spaceBetween="10" :slidesPerView="4" :freeMode="true"
                        :watchSlidesProgress="true" :modules="modules" class="mySwiper">
                        <swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-1.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-2.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-3.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-4.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-5.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-6.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-7.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-8.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-9.jpg" /></swiper-slide><swiper-slide><img
                                src="https://swiperjs.com/demos/images/nature-10.jpg" /></swiper-slide>
                    </swiper>
                </a-col>
                <a-col class="gutter-row car_info" :xs="24" :md="11">
                    info
                </a-col>
            </a-row>
        </div>
    </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { ref } from 'vue';
// Import Swiper Vue.js components
import { Swiper, SwiperSlide } from 'swiper/vue';

// Import Swiper styles
import 'swiper/css';

import 'swiper/css/free-mode';
import 'swiper/css/navigation';
import 'swiper/css/thumbs';

// import required modules
import { FreeMode, Navigation, Thumbs } from 'swiper/modules';
import { ArrowLeftOutlined, ArrowRightOutlined } from '@ant-design/icons-vue';

const modules = [FreeMode, Navigation, Thumbs]

const route = useRoute()
// refs
const thumbsSwiper = ref(null)

// methods
const setThumbsSwiper = (swiper) => {
    thumbsSwiper.value = swiper
}


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

.custom-next:hover{
     box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
}

.naviagtion_btn {
    color: #989898;
}
</style>