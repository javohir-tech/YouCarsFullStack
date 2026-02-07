<template>
    <div class="container">

        <!-- ============================ HERO SECTION ======================================= -->
        <div class="hero_section">
            <Swiper :pagination="{ el: '.my-pagination', clickable: true, dynamicBullets: true, }" :navigation="{
                nextEl: '.custom-next',
                prevEl: '.custom-prev'
            }" :spaceBetween="30" :autoplay="{ delay: 5000, disableOnInteraction: false }" :loop="true"
                :modules="modules" class="mySwiper">
                <SwiperSlide>
                    <a-row class="hero_section_row">
                        <a-col :md="12">
                            <div class="hero_section_info">
                                <h1 class="hero_section_header">Новый Geely Monjaro!</h1>
                                <p class="hero_section_subtitle">
                                    Кроссовер Monjaro - премиальная модель Geely по уровню дизайна, материалов и
                                    технологий.
                                </p>
                                <div class="her_section_btn">
                                    <a-button type="primary" block size="large">Подробнее</a-button>
                                </div>
                            </div>
                        </a-col>
                        <a-col class="hero_section_col" :md="12">
                            <div class="hero_section_image">
                                <img src="./../../public/23a119dc1551a0b9b7c880ef67fed15b332f02b4 (1).png"
                                    alt="reclam car  image">
                            </div>
                        </a-col>
                    </a-row>
                </SwiperSlide>
                <SwiperSlide>
                    <a-row class="hero_section_row">
                        <a-col :md="12">
                            <div class="hero_section_info">
                                <h1 class="hero_section_header">Новый Geely Monjaro!</h1>
                                <p class="hero_section_subtitle">
                                    Кроссовер Monjaro - премиальная модель Geely по уровню дизайна, материалов и
                                    технологий.
                                </p>
                                <div class="her_section_btn">
                                    <a-button type="primary" block size="large">Подробнее</a-button>
                                </div>
                            </div>
                        </a-col>
                        <a-col class="hero_section_col" :md="12">
                            <div class="hero_section_image">
                                <img src="./../../public/23a119dc1551a0b9b7c880ef67fed15b332f02b4 (1).png"
                                    alt="reclam car  image">
                            </div>
                        </a-col>
                    </a-row>
                </SwiperSlide>
                <SwiperSlide>
                    <a-row class="hero_section_row">
                        <a-col :md="12">
                            <div class="hero_section_info">
                                <h1 class="hero_section_header">Новый Geely Monjaro!</h1>
                                <p class="hero_section_subtitle">
                                    Кроссовер Monjaro - премиальная модель Geely по уровню дизайна, материалов и
                                    технологий.
                                </p>
                                <div class="her_section_btn">
                                    <a-button type="primary" block size="large">Подробнее</a-button>
                                </div>
                            </div>
                        </a-col>
                        <a-col class="hero_section_col" :md="12">
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
                <button class="custom-prev">
                    <ArrowLeftOutlined class="naviagtion_btn" />
                </button>
                <button class="custom-next">
                    <ArrowRightOutlined class="naviagtion_btn" />
                </button>
            </div>
        </div>

        <!-- ============================ CARS SECTION ======================================= -->
        <div class="cars_section">
            <div class="header">
                <h1>
                    Автомобильный каталог
                </h1>
            </div>
            <a-row class="cars" :gutter="[16, 24]">
                <a-col v-for="car in carsData" class="gutter-row" :xs="24" :md="12" :xl="8">
                    <CarCard :id="car.id" :model="car.car_model" :like="car.me_liked" :images="car.images"
                        :marka="car.marka" :price="car.price" :milage="car.milage" :displacement="car.displacement"
                        :year="car.year" :transmission_type="car.transmission_type" :power="car.power" :fuel="car.fuel"
                        :drive_type="car.drive_type" :country="car.country" />
                </a-col>
            </a-row>
            <div class="link_cars">
                <router-link to="/">Перейти в каталог
                    <ArrowRightOutlined class="rounter_car" />
                </router-link>
            </div>
        </div>

        <!-- ============================ ABOUT SECTION ======================================= -->
        <div class="about_us">
            <div class="header">
                <h1>Почему мы?</h1>
            </div>
            <div class="section_cards">
                <a-row :gutter="[16, 24]">
                    <a-col class="gutter-row" :xs="24" :md="6">
                        <div class="section_card">
                            <div class="card_image">
                                <img src="./../../public/key.png" alt="key image">
                            </div>
                            <div class="card_info">
                                <p class="card_title">Работаем под ключ</p>
                                <p class="card_subtitle">
                                    У нас вы можете приобрести автомобиль напрямую у официального автодилера, без
                                    посредников и переводчиков.
                                </p>
                            </div>
                        </div>
                    </a-col>
                    <a-col class="gutter-row" :xs="24" :md="6">
                        <div class="section_card">
                            <div class="card_image">
                                <img src="./../../public/message.png" alt="key image">
                            </div>
                            <div class="card_info">
                                <p class="card_title">онлайн-чат 24/7</p>
                                <p class="card_subtitle">
                                    Мы всегда на связи, чтобы ответить на ваши вопросы и помочь вам с выбором.
                                </p>
                            </div>
                        </div>
                    </a-col>
                    <a-col class="gutter-row" :xs="24" :md="6">
                        <div class="section_card">
                            <div class="card_image">
                                <img src="./../../public/car.png" alt="key image">
                            </div>
                            <div class="card_info">
                                <p class="card_title">Упрощенный выбор авто</p>
                                <p class="card_subtitle">
                                   мы создали этот сайт, чтобы сделать поиск автомобиля по вашим критериям максимально простым и удобным.
                                </p>
                            </div>
                        </div>
                    </a-col>
                    <a-col class="gutter-row" :xs="24" :md="6">
                        <div class="section_card">
                            <div class="card_image">
                                <img src="./../../public/car2.png" alt="key image">
                            </div>
                            <div class="card_info">
                                <p class="card_title">Доставка</p>
                                <p class="card_subtitle">
                                    поставка в любой регион РФ, прямая связь без посредников
                                </p>
                            </div>
                        </div>
                    </a-col>
                </a-row>
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
import api from '@/utils/axios'
import { onMounted, ref } from 'vue'

//////////////////// COMPONENTS /////////////////////
import { CarCard } from '@/components'

const carsLoading = ref(false)
const carsData = ref([])

const modules = [Navigation, Pagination, Autoplay]

///////////////////////////////////////////////////////
////////////// GET CARS          //////////////////////
///////////////////////////////////////////////////////
const handleGetcCars = async () => {
    carsLoading.value = true
    try {
        const response = await api.get(`/cars/cars/?page_size=6`)
        carsData.value = response.data.result
        // console.log(response)
    } catch (error) {
        console.log(error.response || error)
    } finally {
        carsLoading.value = true
    }
}

onMounted(() => {
    handleGetcCars()
})

</script>

<style scoped>
/* ===============================  MAIN CSS ============================================== */
.header {
    h1 {
        font-size: 30px;
        font-weight: 600;
        color: #010101;
        margin-bottom: 20px;
    }
}

/* =============================== ABOUT SECTION ============================================== */
.section_card {
    height: 200px;
    background-color: #fff;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transition: box-shadow 0.3s ease, transform 0.3s ease;
    border-radius: 10px;
}

.section_card:hover {
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
    transform: translateY(-4px);
}

.card_image {
    height: 48px;
    width: 48px;
    img {
        height: 100%;
        width: 100%;
        /* object-fit: cover; */
    }
}

.card_info {
    margin-top: 15px;
}

.card_title {
    font-weight: 600;
    font-size: 18px;
    margin-bottom: 8px;
    color: #202020;
}

.card_subtitle {
    font-weight: 400;
    font-size: 15px;
    color: #989898;
}


/* =============================== HERO SECTION ============================================== */

.hero_section {
    background-color: #F4F4F4;
    margin-top: 20px;
    padding: 20px 30px;
    border-radius: 10px;
}

.her_section_btn {
    display: inline-block;
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

.naviagtion_btn {
    color: #989898;
}

.my-pagination {
    text-align: end;
}

/* ==================================CARS SECTION=====================================  */
.cars_section {
    margin-top: 100px;
    padding: 30px 0px;
}

.link_cars {
    padding: 30px 0px;
    text-align: end;

    a {
        color: #293843;
        font-weight: 400;
        font-size: 14px;
    }

    .car_route {
        text-decoration: none;
        color: #293843;
    }
}



@media(max-width: 1200px) {
    /* =============================== HERO SECTION ============================================== */

    .hero_section {
        padding: 0;
    }

    .hero_section_info {
        padding: 15px;
    }

    .hero_section_image {
        width: 100%;
        height: 250px;
        overflow: hidden;

        img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: left;
            transform: translateX(20px);
        }
    }

    .hero_section_header {
        font-size: 24px;
    }

    .hero_section_subtitle {
        font-size: 14px;
        width: 100%;
    }

    .her_section_btn {
        display: block;
    }

    .custom-navigation {
        padding: 10px 15px;
    }

}
</style>