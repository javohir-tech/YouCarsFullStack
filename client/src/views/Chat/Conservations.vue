<template>
    <div class="container">
        <h1 v-if="loading">loading....</h1>
        <div v-if="!loading">
            <div v-for="partner in conversationStore.conversations" :key="partner.partner_id">
                <ConversationItem :partner_id="partner.partner_id" :avatar="partner.avatar" :partner_name="partner.partner" :last_message="partner.last_message" :last_message_time="partner.last_message_time" :is_read="partner.is_read" :unread_count="partner.unread_count" :last_sent_me="partner.last_sent_me" :mute="true"/>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useConversations } from '@/composables/useConversations';
import { useConversationStore } from '@/store/useConversationStore';

////////////////////// COMPONENTS //////////////////////////////
import { ConversationItem } from '@/components';

const conversationStore = useConversationStore()

const { loading } = useConversations()
</script>

<style scoped></style>