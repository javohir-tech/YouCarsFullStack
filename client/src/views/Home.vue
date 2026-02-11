<template>
    <div class="container">

        <!-- ============================ HERO SECTION ======================================= -->
        <div class="hero_section">
            <Swiper :pagination="{ el: '.my-pagination', clickable: true, dynamicBullets: true, }" :navigation="{
                nextEl: '.custom-next',
                prevEl: '.custom-prev'
            }" :spaceBetween="30" :loop="true" :modules="modules" class="mySwiper">
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
                                <img src="./../../public/banner2.png" alt="reclam car  image">
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

        <!-- ============================ FILTER SECTION ======================================= -->
        <div class="filter_section">
            <div class="header">
                <h1>Подбор авто</h1>
            </div>
            <div>
                <Filter @params="handleGetcCars" :count="filterCount" />
            </div>
        </div>

        <!-- ============================ CARS SECTION ======================================= -->
        <div class="cars_section">
            <div class="header">
                <h1>
                    Автомобильный каталог
                </h1>
            </div>
            <div class="empty" v-if="carsData.length === 0 && !carsLoading">
                <a-empty description="filter bo'yicha ma'lumotlar toplimadi " />
            </div>
            <a-row class="cars" :gutter="[16, 24]">
                <a-col v-if="carsLoading" v-for="_ in new Array(8).fill(0)" :xs="24" :md="12" :lg="8" :xl="6">
                    <a-skeleton active />
                </a-col>
                <a-col v-if="!carsLoading && carsData.length > 0" v-for="car in carsData" class="gutter-row" :xs="24"
                    :md="12" :lg="8" :xl="6">
                    <CarCard :id="car.id" :model="car.car_model" :like="car.me_liked" :images="car.images"
                        :marka="car.marka" :price="car.price" :milage="car.milage" :displacement="car.displacement"
                        :year="car.year" :transmission_type="car.transmission_type" :power="car.power" :fuel="car.fuel"
                        :drive_type="car.drive_type" :country="car.country" />
                </a-col>
            </a-row>
            <div class="link_cars">
                <router-link to="/katalog">Перейти в каталог
                    <ArrowRightOutlined class="rounter_car" />
                </router-link>
            </div>
        </div>

        <!-- ============================ SERVISE SECTION ======================================= -->
        <div class="servises_section">
            <div class="header">
                <h1>Почему мы?</h1>
            </div>
            <div class="section_cards">
                <a-row :gutter="[16, 24]">
                    <a-col class="gutter-row" :xs="24" :md="12" :lg="6">
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
                    <a-col class="gutter-row" :xs="24" :md="12" :lg="6">
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
                    <a-col class="gutter-row" :xs="24" :md="12" :lg="6">
                        <div class="section_card">
                            <div class="card_image">
                                <img src="./../../public/car.png" alt="key image">
                            </div>
                            <div class="card_info">
                                <p class="card_title">Упрощенный выбор авто</p>
                                <p class="card_subtitle">
                                    мы создали этот сайт, чтобы сделать поиск автомобиля по вашим критериям максимально
                                    простым и удобным.
                                </p>
                            </div>
                        </div>
                    </a-col>
                    <a-col class="gutter-row" :xs="24" :md="12" :lg="6">
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

        <!-- ============================ ABOUT SECTION ======================================= -->
        <div class="about_section">
            <a-row class="about_section_box">
                <a-col class="gutter-row about_section_left" :xs="{ span: 24, order: 2 }" :md="{ span: 12, order: 1 }"
                    :lg="{ span: 12, order: 1 }">
                    <div class="about_section_image">
                        <img src="./../../public/image copy.png" alt="about_section_image">
                        <div class="secret_box"></div>
                    </div>
                </a-col>
                <a-col class="gutter-row" :xs="{ span: 24, order: 1 }" :md="{ span: 12, order: 2 }"
                    :lg="{ span: 12, order: 2 }">
                    <h3 class="about_section_title">
                        О нашей компании
                    </h3>
                    <p class="about_section_subtitle">
                        Мы имеем огромный опыт работы с автомобильным рынком Кореи и тщательно отбираем автомобили для
                        наших клиентов, учитывая их потребности и бюджет. Мы работаем только с надежными поставщиками и
                        перевозчиками, чтобы обеспечить безопасность и надежность доставки.
                    </p>
                    <div class="about_section_btn">
                        <a-button type="primary" block size="large">Связаться с нами</a-button>
                    </div>
                </a-col>
            </a-row>
        </div>
        <!-- ============================ MARKAS SECTION ======================================= -->
        <div class="markas_section">
            <a-row class="markas" :gutter="[0, 0]">
                <a-col v-if="loading" class="marka_col" v-for="_ in new Array(12).fill(1)" :xs="12" :sm="8" :md="6"
                    :lg="4">
                    <a-skeleton active />
                </a-col>
                <a-col v-else class="marka_col" :xs="12" :sm="8" :md="6" :lg="4" v-for="marka in data" :key="marka.id">
                    <div class="marka_box">
                        <img :src="marka.image" :alt="marka.name">
                        <p>{{ capitalize(marka.name) }}</p>
                    </div>
                </a-col>
            </a-row>
        </div>
        <!-- ============================ CALL  SECTION ======================================= -->
        <CallCard />
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
import { onMounted, ref, toRaw } from 'vue'

//////////////////// COMPONENTS /////////////////////
import { CallCard, CarCard, Filter } from '@/components'

//////////////////////////////// useFetch ///////////////////////
import useFetch from '@/Hooks/useFetch'

const { data, loading, error, getData } = useFetch()

const carsLoading = ref(false)
const carsData = ref([])
const filterCount = ref(0)

const modules = [Navigation, Pagination, Autoplay]

///////////////////////////////////////////////////////
////////////// GET CARS          //////////////////////
///////////////////////////////////////////////////////
const handleGetcCars = async (params) => {
    carsLoading.value = true
    try {
        const response = await api.get(`/cars/cars/`, {
            params: {
                page_size: 8,
                ...params
            }
        })
        carsData.value = response.data.result
        if (params) {
            localStorage.setItem('filter_params', JSON.stringify(params))
            filterCount.value = response.data.count
        } else {
            filterCount.value = 0
        }
    } catch (error) {
        console.log(error.response || error)
    } finally {
        carsLoading.value = false
    }
}

//////////////////////  methods ////////////////////////
const capitalize = (text) => {
    return text[0].toUpperCase() + text.slice(1, text.length)
}

onMounted(() => {
    handleGetcCars()
    getData('https://api.youcarrf.ru/marks')
})

</script>

<style scoped>



/* ===============================  MARKAS CSS ============================================== */
.markas_section {
    margin-top: 100px;
}

.error {
    display: flex;
    align-items: center;
    justify-content: center;
}

.marka_col {
    width: 216px;
}

.marka_col:hover {
    cursor: pointer;
    box-shadow: 0 21px 21px rgba(176, 176, 176, 0.09);

    img {
        transition: all 0.3s ease-in-out;
        scale: 1.1;
    }


}

.marka_box {
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
    height: 168px;
    width: 100%;
    border: 1px #F1F1F1 solid;

    p {
        margin: 0;
        font-size: 16px;
        font-weight: 500;
        color: rgba(41, 56, 67, 1);
    }
}

/* =============================== ABOUT SECTION ============================================== */
.filter_section {
    margin-top: 100px;
}

/* =============================== ABOUT SECTION ============================================== */
.about_section {
    margin-top: 150px;
    border-radius: 10px;
    background-color: #F6F6F6;
    padding: 40px;
    /* background: url(../../public/image.png); */
    background-image: url(../../public/image.png);
    background-size: 350px;
    background-position: 100px;
    background-repeat: no-repeat;
}


.about_section_image {
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: space-around;
    position: relative;
    bottom: 50px;

    img {
        /* width: 100%; */
        height: 100%;
        transform: scale(1.6);
    }
}

.about_section_title {
    font-weight: 600;
    font-size: 28px;
    color: #010101;
}

.about_section_subtitle {
    font-weight: 400;
    font-size: 16px;
    color: #989898;
}

.about_section_btn {
    display: inline-block;
}


/* =============================== SERVISES SECTION ============================================== */
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
    height: 400px;

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
    margin-top: 30px;
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

@media(max-width:992px) {
    .card_title {
        font-size: 18px;
        font-weight: 500;
    }

    .card_subtitle {
        font-weight: 400;
        font-size: 15px;
    }

    .about_section {
        background-size: 290px;
    }

    .marka_box {
        font-size: 12px;
    }

    .markas_section {
        margin-top: 75px;
    }
}

@media(max-width : 768px) {

    .marka_col {
        width: 167px;
    }

    .marka_box {
        height: 130px;
    }

    /* =============================== ABOUT SECTION ============================================== */
    .about_section_title {
        font-weight: 500;
        font-size: 23px;
    }

    .secret_box {
        display: none;
    }

    .about_section_subtitle {
        font-weight: 400;
        font-size: 14px;
    }

    .about_section {
        margin-top: 50px;
        padding: 15px;
        background-image: none;
        overflow: hidden;
    }

    .about_section_btn {
        display: block;
        margin-bottom: 80px;
    }

    .about_section_image {
        height: 180px;
        top: 1px;
        justify-content: center;
        align-items: center;
        background: url(../../public/image.png);
        background-position: top;
        background-repeat: no-repeat;
        background-size: 250px;

        img {
            position: absolute;
            top: -20px;
            transform: scale(1.5);
        }
    }
}
</style>