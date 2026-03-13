<template>
    <div class="container">

        <!-- ============================ HERO SECTION ======================================= -->
        <BannerSection />

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
        <ServicesSection />

        <!-- ============================ ABOUT SECTION ======================================= -->
        <AboutSection />

        <!-- ============================ MARKAS SECTION ======================================= -->
        <MarkaSection />

        <!-- ============================ CALL  SECTION ======================================= -->
        <CallCard />

        <!-- =========================== BLog Section ========================================= -->
        <BlogSec />

    </div>
</template>

<script setup>

// modules
import api from '@/utils/axios'
import { onMounted, ref } from 'vue'
import { ArrowRightOutlined } from '@ant-design/icons-vue'

//////////////////// COMPONENTS /////////////////////
import { CallCard, CarCard, Filter } from '@/components'
import { BannerSection, ServicesSection, AboutSection, BlogSec, MarkaSection } from '.'

const carsLoading = ref(false)
const carsData = ref([])
const filterCount = ref(0)

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

onMounted(() => {
    handleGetcCars()
})

</script>

<style scoped>
/* =============================== ABOUT SECTION ============================================== */
.filter_section {
    margin-top: 100px;
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
</style>