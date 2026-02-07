<template>
    <div class="container">
        <div class="hero_section">
            <Swiper 
            :pagination="{ el: '.my-pagination', clickable: true , dynamicBullets: true, }" 
            :navigation="{
                nextEl: '.custom-next',
                prevEl: '.custom-prev'
            }" 
            :autoplay="{delay : 3000 , disableOnInteraction: false}"
            :loop="true"
            :modules="modules" class="mySwiper"
            >
                <SwiperSlide>
                    <a-row class="hero_section_row">
                        <a-col :xl="12">
                            <div>
                                <h1 class="hero_section_header">Новый Geely Monjaro!</h1>
                                <p class="hero_section_subtitle">
                                    Кроссовер Monjaro - премиальная модель Geely по уровню дизайна, материалов и
                                    технологий.
                                </p>
                                <a-button type="primary" size="large">Подробнее</a-button>
                            </div>
                        </a-col>
                        <a-col class="hero_section_col" :xl="12">
                            <div class="hero_section_image">
                                <img src="./../../public/23a119dc1551a0b9b7c880ef67fed15b332f02b4 (1).png"
                                    alt="reclam car  image">
                            </div>
                        </a-col>
                    </a-row>
                </SwiperSlide>
                <SwiperSlide>
                    <a-row class="hero_section_row">
                        <a-col :xl="12">
                            <div>
                                <h1 class="hero_section_header">Новый Geely Monjaro!</h1>
                                <p class="hero_section_subtitle">
                                    Кроссовер Monjaro - премиальная модель Geely по уровню дизайна, материалов и
                                    технологий.
                                </p>
                                <a-button type="primary" size="large">Подробнее</a-button>
                            </div>
                        </a-col>
                        <a-col class="hero_section_col" :xl="12">
                            <div class="hero_section_image">
                                <img src="./../../public/23a119dc1551a0b9b7c880ef67fed15b332f02b4 (1).png"
                                    alt="reclam car  image">
                            </div>
                        </a-col>
                    </a-row>
                </SwiperSlide>
                <SwiperSlide>
                    <a-row class="hero_section_row">
                        <a-col :xl="12">
                            <div>
                                <h1 class="hero_section_header">Новый Geely Monjaro!</h1>
                                <p class="hero_section_subtitle">
                                    Кроссовер Monjaro - премиальная модель Geely по уровню дизайна, материалов и
                                    технологий.
                                </p>
                                <a-button type="primary" size="large">Подробнее</a-button>
                            </div>
                        </a-col>
                        <a-col class="hero_section_col" :xl="12">
                            <div class="hero_section_image">
                                <img src="./../../public/23a119dc1551a0b9b7c880ef67fed15b332f02b4 (1).png"
                                    alt="reclam car  image">
                            </div>
                        </a-col>
                    </a-row>
                </SwiperSlide>
            </Swiper>

            <div class="custom-navigation">
                <div class="my-pagination"></div>
                <button class="custom-prev"><ArrowLeftOutlined class="naviagtion_btn"/></button>
                <button class="custom-next"><ArrowRightOutlined class="naviagtion_btn"/></button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue'

// styles
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

// modules
import { Navigation, Pagination, Autoplay } from 'swiper/modules'
import { ArrowLeftOutlined, ArrowRightOutlined } from '@ant-design/icons-vue'

const modules = [Navigation, Pagination , Autoplay]

</script>

<style scoped>
/* HERO SECTION */

.hero_section {
    background-color: #F4F4F4;
    margin-top: 20px;
    padding: 20px 30px;
    border-radius: 10px;
}


.hero_section_header {
    font-weight: 500;
    font-size: 35px;
    color: #000000;
}

.hero_section_subtitle {
    font-weight: 400;
    width: 80%;
    font-size: 16px;
    color: #5A5A5A;
}

.hero_section_image {
    width: 100%;
    height: 300px;

    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
}

.custom-navigation {
    justify-content: end;
    align-items: center;
    display: flex;
    gap: 10px;
}

.custom-prev,
.custom-next {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: white;
    border: none;
    cursor: pointer;
}

.naviagtion_btn{
    color: #989898;
}

.my-pagination {
    text-align: end;
}
</style>