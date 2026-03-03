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
        <div class="messages-container" ref="messagesContainer">

            <!-- Loading -->
            <div v-if="isLoading" class="loading-state">
                <div class="spinner"></div>
                <p>Yuklanmoqda...</p>
            </div>

            <template v-else>
                <div v-if="messages.length === 0" class="empty-state">
                    Hali xabar yo'q. Birinchi xabar yuboring! 👋
                </div>

                <div
                    v-for="msg in messages"
                    :key="msg.id"
                    class="message-row"
                    :class="msg.sender_id !== route.params.userId ? 'sent' : 'received'"
                >
                    <div class="bubble">
                        <p class="text">{{ msg.content }}</p>
                        <div class="meta">
                            <span class="time">{{ formatTime(msg.created_time) }}</span>
                            <!-- O'qilgan belgisi faqat o'z xabarlarimizda -->
                            <span
                                v-if="msg.sender_id !== route.params.userId"
                                class="read-status"
                                :class="{ read: msg.is_read }"
                            >
                                {{ msg.is_read ? "✓✓" : "✓" }}
                            </span>
                        </div>
                    </div>
                </div>
            </template>

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
                ➤
            </button>
        </div>

    </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useChat } from '@/composables/useChat'
import { onMounted, onUnmounted, ref, watch, nextTick } from 'vue'

const route = useRoute()
const { messages, isConnect, isLoading, connect, SendMessage, disconnect, getChatHistory } = useChat(route.params.userId)

const inputText = ref("")
const messagesContainer = ref(null)

function formatTime(isoString) {
    if (!isoString) return ""
    const date = new Date(isoString)
    return date.toLocaleTimeString("uz-UZ", { hour: "2-digit", minute: "2-digit" })
}

function handleSend() {
    if (!inputText.value.trim()) return
    SendMessage(inputText.value)
    inputText.value = ""
}

function scrollToBottom() {
    nextTick(() => {
        if (messagesContainer.value) {
            messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
    })
}

// Yangi xabar kelsa pastga scroll
watch(messages, () => {
    scrollToBottom()
}, { deep: true })

onMounted(async () => {
    await getChatHistory() 
    connect()     
    scrollToBottom()
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
    background: #f0f2f5;
    font-family: sans-serif;
}

/* ---- Header ---- */
.chat-header {
    background: #ffffff;
    padding: 14px 20px;
    border-bottom: 1px solid #e5e7eb;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.user-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.avatar {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: #4f46e5;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 18px;
    flex-shrink: 0;
}

.username {
    font-weight: 600;
    font-size: 15px;
    margin: 0;
    color: #111827;
}

.status {
    font-size: 12px;
    color: #9ca3af;
    margin: 2px 0 0;
}

.status.online { color: #22c55e; }

/* ---- Messages ---- */
.messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 20px 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    gap: 12px;
    color: #9ca3af;
}

.spinner {
    width: 32px;
    height: 32px;
    border: 3px solid #e5e7eb;
    border-top-color: #4f46e5;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.empty-state {
    text-align: center;
    color: #9ca3af;
    margin: auto;
    font-size: 14px;
}

.message-row {
    display: flex;
}

.message-row.sent     { justify-content: flex-end; }
.message-row.received { justify-content: flex-start; }

.bubble {
    max-width: 65%;
    padding: 10px 14px;
    border-radius: 18px;
    background: white;
    box-shadow: 0 1px 2px rgba(0,0,0,0.08);
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
    margin: 0 0 4px;
    font-size: 14px;
    line-height: 1.5;
    word-break: break-word;
}

.meta {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 4px;
}

.time {
    font-size: 11px;
    opacity: 0.6;
}

.read-status {
    font-size: 11px;
    opacity: 0.5;
}

.read-status.read {
    opacity: 1;
    color: #a5f3fc;
}

/* ---- Input ---- */
.input-area {
    display: flex;
    gap: 10px;
    padding: 14px 16px;
    background: white;
    border-top: 1px solid #e5e7eb;
}

.input-area input {
    flex: 1;
    padding: 10px 18px;
    border: 1px solid #e5e7eb;
    border-radius: 24px;
    outline: none;
    font-size: 14px;
    background: #f9fafb;
    transition: border-color 0.2s;
}

.input-area input:focus   { border-color: #4f46e5; background: white; }
.input-area input:disabled { background: #f3f4f6; cursor: not-allowed; }

.input-area button {
    width: 44px;
    height: 44px;
    background: #4f46e5;
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
    flex-shrink: 0;
}

.input-area button:hover:not(:disabled) { background: #4338ca; }
.input-area button:disabled { background: #d1d5db; cursor: not-allowed; }
</style>