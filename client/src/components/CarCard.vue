<template>
    <div>
        <div class="car_card" @click="">
            <div class="car_card_image">
                <img :src="props.image" :alt="props.model">
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
                    <span @click="liked ? handleCarDislike(props.id) : HandleCarLike(props.id)">
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


const props = defineProps({
    id: String,
    like: Boolean,
    marka: String,
    model: String,
    price: String,
    milage: Number,
    year: Number,
    image: String,
    transmission_type: String,
    displacement: String,
    power: Number,
    fuel: String,
    drive_type: String,
    country: String,
})

const liked = ref(props.like)
const HandleCarLike = async (id) => {
    try {
        const {data} = await api.post(`/cars/car/like/${id}/`)
        if(data.success){
            message.success("like bosildi")
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
        message.info("dislike qilindi")
    } catch (error) {
        console.log(error.response || error)
    }
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
    border-radius: 10px;
}

.car_card_info {
    padding: 10px 15px;
    background: #fff;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
    transition: box-shadow 0.3s ease, transform 0.3s ease;

    p {
        margin-bottom: 10px;
    }
}

.car_card:hover .car_card_info {
    box-shadow: 0 14px 32px rgba(0, 0, 0, 0.14);
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

.liked{
    color: #FF0000;
}
</style>