<template>
    <!-- ============================ HERO SECTION ======================================= -->
    <section class="hero_section">
        <Swiper :pagination="{ el: '.my-pagination', clickable: true, dynamicBullets: true, }" :navigation="{
            nextEl: '.custom-next',
            prevEl: '.custom-prev'
        }" :spaceBetween="30" :loop="true" :modules="modules" class="mySwiper">
            <SwiperSlide v-for="banner in data" :key="banner.id">
                <a-row class="hero_section_row">
                    <a-col :md="12">
                        <div class="hero_section_info">
                            <h1 class="hero_section_header">{{ t('banner.moreHeader') }} {{ banner.marka }} {{
                                banner.model
                                }}!</h1>
                            <p class="hero_section_subtitle">
                                {{ banner.subtitle }}
                            </p>
                            <div class="her_section_btn">
                                <a-button @click="toNavigate(banner.car_id)" type="primary" block size="large">{{
                                    t('banner.buttonText') }}</a-button>
                            </div>
                        </div>
                    </a-col>
                    <a-col class="hero_section_col" :md="12">
                        <div class="hero_section_image">
                            <img :src="banner.image" @load="onLoad" @error="onError" alt="reclam car  image">
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
    </section>
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
// fetch
import useFetch from '@/Hooks/useFetch'
import { onMounted, ref } from 'vue'
import router from '@/router'
import { useI18n } from 'vue-i18n'

const modules = [Navigation, Pagination, Autoplay]

const { data, loading, error, getData } = useFetch()
const { t } = useI18n()

const imageLoading = ref(true)

const onLoad = () => {
    imageLoading.value = false
}

const onError = () => {
    imageLoading.value = false
}


const toNavigate = (car_id) => {
    router.push(`/cars/detail/${car_id}`)
}

onMounted(async () => {
    await getData("/cars/car/banner/")
})
</script>

<style scoped>
.hero_section {
    background-color: #F4F4F4;
    margin-top: 20px;
    padding: 20px 30px;
    border-radius: 10px;
    min-height: 500px;
}

.her_section_btn {
    display: inline-block;
}


.hero_section_header {
    font-weight: 500;
    font-size: 35px;
    text-transform: uppercase;
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