<template>
    <section class="servises_section">
        <div class="header">
            <h1>{{ t('services.title') }}</h1>
        </div>
        <div class="section_cards">
            <a-row :gutter="[16, 24]">
                <a-col class="gutter-row" :xs="24" :md="12" :lg="6" v-for="(card, index) in serviceCards" :key="index">
                    <div class="section_card">
                        <div class="card_image">
                            <img :src="`/public/${cardImages[index]}`" :alt="card.title">
                        </div>
                        <div class="card_info">
                            <p class="card_title">{{ card.title }}</p>
                            <p class="card_subtitle">
                                {{ card.description }}
                            </p>
                        </div>
                    </div>
                </a-col>
            </a-row>
        </div>
    </section>
</template>

<script setup>
import { useI18n } from 'vue-i18n';
import { computed } from 'vue';

const { locale, messages, t } = useI18n();

const cardImages = ['key.png', 'message.png', 'car.png', 'car2.png'];

const serviceCards = computed(() => {
    const cards = messages.value[locale.value]?.services?.cards || [];
    return Array.isArray(cards) ? cards : [];
});
</script>

<style scoped>
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

@media(max-width:992px) {
    .card_title {
        font-size: 18px;
        font-weight: 500;
    }

    .card_subtitle {
        font-weight: 400;
        font-size: 15px;
    }
}
</style>