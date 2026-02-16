<template>
    <div class="blog_card_wrapper">
        <router-link class="blog_card" :to="`blog/detail/${props.id}`">
            <div class="blog_image">
                <img :src="props.image" :alt="props.title">
            </div>
            <div class="car_info">
                <p class="title">{{ props.title }}</p>
                <p class="text">{{ shortText(props.text, 150) }}</p>
                <div class="link">
                    Подробнее
                    <ArrowRightOutlined />
                </div>
            </div>
        </router-link>
    </div>
</template>

<script setup>
import { ArrowRightOutlined } from '@ant-design/icons-vue';

const props = defineProps({
    image: String,
    text: String,
    title: String,
    id: String
})

function shortText(text, limit = 200) {
    if (!text) return ""

    return text.length > limit
        ? text.slice(0, limit) + "..."
        : text;
}
</script>

<style scoped>
.blog_card_wrapper {
    height: 100%;
}

.blog_card_wrapper:hover .car_info {
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.blog_card_wrapper:hover .blog_image img {
    scale: 1.1;
}

.blog_card {
    text-decoration: none;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.blog_image {
    border-radius: 10px;
    overflow: hidden;
    flex-shrink: 0;
}

.blog_image img {
    width: 100%;
    height: 220px;
    border-radius: 10px;
    object-position: center;
    object-fit: cover;
    transition: all 0.3s ease-in-out;
}

.car_info {
    transition: all 0.3s ease-in-out;
    padding: 15px 10px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

.title {
    font-weight: 500;
    font-size: 19px;
    color: rgba(41, 56, 67, 1);
}

.text {
    font-weight: 400;
    font-size: 15px;
    color: rgba(152, 152, 152, 1);
}

.link {
    display: flex;
    margin-top: auto;
    align-items: center;
    gap: 10px;
    font-size: 14px;
    color: rgba(41, 56, 67, 1);

    p {
        margin: 0;
    }
}

@media(max-width : 768px) {
    .blog_image img {
        height: 180px;
    }
}
</style>