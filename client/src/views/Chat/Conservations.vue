<template>
    <div class="container">
        <h1 v-if="loading">loading....</h1>
        <div v-if="!loading">
            <a-flex class="header" align="center" gap="10">
                <div class="back">
                    <i class="fa-solid fa-angle-left" @click="toBack"></i>
                </div>
                <h1>Сообщения</h1>
            </a-flex>
            <div v-for="partner in conversationStore.conversations" :key="partner.partner_id" class="conversations">
                <ConversationItem :partner_id="partner.partner_id" :avatar="partner.avatar"
                    :partner_name="partner.partner" :last_message="partner.last_message"
                    :last_message_time="partner.last_message_time" :is_read="partner.is_read"
                    :unread_count="partner.unread_count" :is_online="partner.is_online"
                    :last_sent_me="partner.last_sent_me" :mute="true" />
            </div>
        </div>
    </div>
</template>

<script setup>
import router from '@/router';
import { useConversations } from '@/composables/useConversations';
import { useConversationStore } from '@/store/useConversationStore';

////////////////////// COMPONENTS //////////////////////////////
import { ConversationItem } from '@/components';
import { LeftOutlined } from '@ant-design/icons-vue';

const conversationStore = useConversationStore()
const { loading } = useConversations()

function toBack() {
    router.push("/profile")
}
</script>

<style scoped>
.conversations {
    margin-bottom: 15px;
}

.back i {
    font-size: 24px;
    color: rgba(41, 56, 67, 1);
}


.header {
    padding-bottom: 10px;
    color: rgba(41, 56, 67, 1);
}

.header h1 {
    font-weight: 700;
    font-size: 30px;
    padding: 0;
    margin: 0;
}

@media(max-width: 768px) {
    .header h1 {
        font-weight: 500;
        font-size: 22px;
    }

    .back{
        font-size: 22px;
    }
}

@media (min-width: 576px) {
    .back {
        display: none;
    }
}
</style>