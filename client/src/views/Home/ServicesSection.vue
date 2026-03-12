<template>
    <section class="servises_section">
        <div class="header">
            <h1>Почему мы?</h1>
        </div>
        <div class="section_cards">
            <a-row :gutter="[16, 24]">
                <a-col class="gutter-row" :xs="24" :md="12" :lg="6">
                    <div class="section_card">
                        <div class="card_image">
                            <img src="./../../../public/key.png" alt="key image">
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
                            <img src="./../../../public/message.png" alt="key image">
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
                            <img src="./../../../public/car.png" alt="key image">
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
                            <img src="./../../../public/car2.png" alt="key image">
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
    </section>
</template>

<script setup>

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