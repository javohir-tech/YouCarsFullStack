<template>
    <div class="container">
        <h1 v-if="loading">loading....</h1>
        <div v-if="!loading">
            <div v-for="partner in conversationStore.conversations" :key="partner.partner_id">
                <p>{{ partner.partner }}</p>
                <p>{{ partner.last_message }}</p>
                <p>{{ partner.unread_count }}</p>
                <p>{{ partner.last_message_time }}</p>
                <p>{{ partner.last_sent_me }}</p>
                <p>{{ partner.is_new_partner }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useConversations } from '@/composables/useConversations';
import { useConversationStore } from '@/store/useConversationStore';

const conversationStore = useConversationStore()

const { loading } = useConversations()
</script>

<style scoped></style>