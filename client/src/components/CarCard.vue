<template>
    <div>
        <div class="car_card" @click="handleNavigate(props.id)">
            <div class="car_card_image">
                <Swiper :scrollbar="{ draggable: true }" :modules="modules" class="mySwiper">
                    <SwiperSlide v-for="image in props.images">
                        <a-skeleton-image v-if="loading"/>
                        <img :src="image.image" v-show="!loading" @load="onLoad" @error="onError" :alt="props.model">
                    </SwiperSlide>
                </Swiper>
            </div>
            <div class="car_card_info">
                <div class="car_subtitle">
                    <p>{{ props.marka }} {{ props.model }} , {{ props.year }}</p>
                </div>
                <div class="car_price">
                    <p>{{ props.price }} $</p>
                </div>
                <div class="item">
                    <p>{{ props.milage }} км</p>
                    <p>{{ props.transmission_type }}</p>
                </div>
                <div class="item">
                    <p>
                        {{ props.displacement }}/{{ props.power }}л.с./ {{ props.fuel }}
                    </p>
                    <p>
                        {{ props.drive_type }}
                    </p>
                </div>
                <div class="item">
                    <p>{{ props.country }}</p>
                    <span @click.stop="liked ? handleCarDislike(props.id) : HandleCarLike(props.id)">
                        <HeartFilled class="car_like" :class="liked ? 'liked' : ''" />
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import api from '@/utils/axios';
import { HeartFilled } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
// Swiper Vue components
import { Swiper, SwiperSlide } from 'swiper/vue'

// Swiper styles
import 'swiper/css'
import 'swiper/css/scrollbar'

// Modules
import { Scrollbar } from 'swiper/modules'

// Modules array
const modules = [Scrollbar]
const loading = ref(true)
const router = useRouter()

const props = defineProps({
    id: String,
    like: Boolean,
    marka: String,
    model: String,
    price: String,
    milage: Number,
    year: Number,
    images: Array,
    transmission_type: String,
    displacement: String,
    power: Number,
    fuel: String,
    drive_type: String,
    country: String,
})

const emit = defineEmits(['dislike'])

const liked = ref(props.like)
const HandleCarLike = async (id) => {
    try {
        const { data } = await api.post(`/cars/car/like/${id}/`)
        if (data.success) {
            message.success(`${props.marka} ${props.model} liked`)
        }
        liked.value = true
    } catch (error) {
        console.log(error.response || response)
    }
}

const handleCarDislike = async (id) => {
    try {
        await api.delete(`/cars/car/like/${id}/`)
        liked.value = false
        message.info(`${props.marka} ${props.model} disliked`)
        emit('dislike', id)
    } catch (error) {
        console.log(error.response || error)
    }
}

const handleNavigate = (id) => {
    router.push(`/cars/detail/${id}`)
}

const onLoad = () => {
    loading.value = false
}

const onError = () => {
    loading.value = false
}

</script>

<style scoped>
.car_card_image {
    width: 100%;
    height: 160px;
    overflow: hidden;
    border-radius: 10px;
}

.car_card_image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
}

.car_card_info {
    padding: 10px 15px;
    background: #fff;
    border-bottom-left-radius: 14px;
    border-bottom-right-radius: 14px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
    transition: box-shadow 0.3s ease, transform 0.3s ease;

    p {
        margin-bottom: 10px;
    }
}


.car_subtitle {
    p {
        font-weight: 400;
        font-size: 17px;
        color: #293843;
    }
}

.car_price {
    p {
        font-weight: 700;
        font-size: 20px;
        color: #293843;
    }
}

.item {
    display: flex;
    align-items: center;
    justify-content: space-between;

    p {
        font-weight: 400;
        padding-right: 15px;
        font-size: 15px;
        color: #989898;
    }
}

.car_like {
    color: #989898;
    font-size: 16px;
    cursor: pointer;
}

.liked {
    color: #FF0000;
}

.swiper {
    width: 100%;
    height: 100%;
}

.swiper-slide {
    text-align: center;
    font-size: 18px;
    background: rgba(0, 0, 0, 0.06);

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

:deep(.mySwiper .swiper-scrollbar-drag) {
    background: #2684E5;
    /* och kulrang */
    height: 4px;
}

:deep(.mySwiper .swiper-scrollbar) {
    opacity: 0;
    transition: opacity 0.3s ease;
}

.car_card:hover .car_card_info {
    box-shadow: 0 14px 32px rgba(0, 0, 0, 0.14);
}

.car_card:hover :deep(.mySwiper .swiper-scrollbar) {
    opacity: 1;
}
</style>