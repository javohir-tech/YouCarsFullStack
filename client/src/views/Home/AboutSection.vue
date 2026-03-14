<template>
    <section class="about_section">
        <a-row class="about_section_box">
            <a-col class="gutter-row about_section_left" :xs="{ span: 24, order: 2 }" :md="{ span: 12, order: 1 }"
                :lg="{ span: 12, order: 1 }">
                <div class="about_section_image">
                    <img src="./../../../public/image copy.png" alt="about_section_image">
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
                    <a-button @click="router.push('/about')" type="primary" block size="large">Связаться с нами</a-button>
                </div>
            </a-col>
        </a-row>
    </section>
</template>

<script setup>
import router from '@/router';

</script>

<style scoped>
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

@media(max-width:992px) {
    .about_section {
        background-size: 290px;
    }
}

@media(max-width : 768px) {

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