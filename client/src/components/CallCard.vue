<template>
    <div class="call_section">
        <a-row :gutter="[16, 24]">
            <a-col class="call_section_info" :lg="12">
                <h2>Не можете определится с выбором?</h2>
                <p>Оставьте заявку, и наши менеджеры проконсультируют вас!</p>
                <router-link to="/" class="call_btn"><a-button size="large" block>Оставить
                        заявку</a-button></router-link>
            </a-col>
            <a-col class="call_section_image" :lg="12">
                <img src="../../public/callImage.png" alt="call image">
            </a-col>
        </a-row>
    </div>
</template>

<script setup>
</script>

<style scoped>
/* ===============================  CALL CSS ============================================== */
.call_section {
    overflow: hidden;
    margin-top: 100px;
    border-radius: 15px;
    padding: 30px;
    background: linear-gradient(90deg, #3593F3 50.44%, #0C74DF 80.16%);
    min-height: 200px;
}

.call_section_info {
    color: rgba(255, 255, 255, 1);

    h2 {
        font-weight: 500;
        font-size: 28px;
    }

    p {
        font-size: 15px;
        font-weight: 400;
    }
}

.call_btn {
    display: inline-block;
}

.call_section_image img {
    object-fit: cover;
    width: 100%;
}

@media(max-width : 992px) {
    .call_section_image img {
        scale: 1.3;
        position: relative;
        left: 100px;
    }

    .call_section_info {
        h2 {
            font-size: 23px;
        }

        p {
            font-size: 14px;
        }
    }

    .call_btn {
        display: block;
        margin-bottom: 20px;
    }
}
</style>