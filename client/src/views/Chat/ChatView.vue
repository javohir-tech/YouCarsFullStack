<template>
    <div class="chat-wrapper">
        <!-- Header -->
        <div class="chat-header">
            <div class="user-info">
                <div class="avatar">{{ route.params.username?.charAt(0).toUpperCase() }}</div>
                <div>
                    <p class="username">{{ route.params.username }}</p>
                    <p class="status" :class="{ online: isConnect }">
                        {{ isConnect ? "Online" : "Offline" }}
                    </p>
                </div>
            </div>
        </div>

        <!-- Messages -->
        <div class="messages-container" ref="messagesEnd">
            <div
                v-for="(msg, index) in messages"
                :key="index"
                class="message-row"
                :class="msg.receiver_id !== route.params.userId ? 'sent' : 'received'"
            >
                <div class="bubble">
                    <p class="text">{{ msg.message }}</p>
                    <span class="time">{{ msg.created_time }}</span>
                </div>
            </div>

            <div v-if="messages.length === 0" class="empty-state">
                Hali xabar yo'q. Birinchi xabar yuboring! 👋
            </div>
        </div>

        <!-- Input -->
        <div class="input-area">
            <input
                v-model="inputText"
                @keyup.enter="handleSend"
                placeholder="Xabar yozing..."
                :disabled="!isConnect"
            />
            <button @click="handleSend" :disabled="!isConnect || !inputText.trim()">
                Yuborish
            </button>
        </div>
    </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useChat } from '@/composables/useChat'
import { onMounted, onUnmounted, ref, watch, nextTick } from 'vue'

const route = useRoute()
const { messages, isConnect, connect, SendMessage, disconnect } = useChat(route.params.userId)


const inputText = ref("")
const messagesEnd = ref(null)

function handleSend() {
    if (!inputText.value.trim()) return
    SendMessage(inputText.value)
    inputText.value = ""
}

// Yangi xabar kelganda pastga scroll qilish
watch(messages, async () => {
    await nextTick()
    if (messagesEnd.value) {
        messagesEnd.value.scrollTop = messagesEnd.value.scrollHeight
    }
}, { deep: true })

onMounted(() => {
    connect()
})

onUnmounted(() => {
    disconnect()
})
</script>

<style scoped>
.chat-wrapper {
    display: flex;
    flex-direction: column;
    height: 100vh;
    max-width: 700px;
    margin: 0 auto;
    background: #f5f5f5;
}

.chat-header {
    background: #ffffff;
    padding: 16px 20px;
    border-bottom: 1px solid #e0e0e0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}

.user-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.avatar {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: #4f46e5;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 18px;
}

.username {
    font-weight: 600;
    font-size: 15px;
    margin: 0;
}

.status {
    font-size: 12px;
    color: #999;
    margin: 0;
}

.status.online {
    color: #22c55e;
}

.messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.empty-state {
    text-align: center;
    color: #999;
    margin-top: 40px;
    font-size: 14px;
}

.message-row {
    display: flex;
}

.message-row.sent {
    justify-content: flex-end;
}

.message-row.received {
    justify-content: flex-start;
}

.bubble {
    max-width: 65%;
    padding: 10px 14px;
    border-radius: 16px;
    background: white;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.sent .bubble {
    background: #4f46e5;
    color: white;
    border-bottom-right-radius: 4px;
}

.received .bubble {
    border-bottom-left-radius: 4px;
}

.text {
    margin: 0 0 4px 0;
    font-size: 14px;
    line-height: 1.5;
}

.time {
    font-size: 11px;
    opacity: 0.6;
    float: right;
    margin-left: 8px;
}

.input-area {
    display: flex;
    gap: 10px;
    padding: 16px;
    background: white;
    border-top: 1px solid #e0e0e0;
}

.input-area input {
    flex: 1;
    padding: 10px 16px;
    border: 1px solid #e0e0e0;
    border-radius: 24px;
    outline: none;
    font-size: 14px;
    transition: border-color 0.2s;
}

.input-area input:focus {
    border-color: #4f46e5;
}

.input-area input:disabled {
    background: #f5f5f5;
    cursor: not-allowed;
}

.input-area button {
    padding: 10px 22px;
    background: #4f46e5;
    color: white;
    border: none;
    border-radius: 24px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: background 0.2s;
}

.input-area button:hover:not(:disabled) {
    background: #4338ca;
}

.input-area button:disabled {
    background: #c7c7c7;
    cursor: not-allowed;
}
</style>