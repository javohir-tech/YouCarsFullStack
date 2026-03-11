import api from "@/utils/axios"
import { ref } from "vue"
import { useConversationStore } from "@/store/useConversationStore"

export function useChat(initialUserId) {
    const messages = ref([])
    const ws = ref(null)
    const isConnect = ref(false)
    const currentUserId = ref(initialUserId)
    const partner_online = ref(false)
    const { onread } = useConversationStore()

    async function getChatHistory(userId = currentUserId.value) {
        currentUserId.value = userId
        try {
            const data = await api.get(`/api/chat/${userId}/history/`, {
                params: {
                    page_size: 100,
                }
            })
            //  console.log(data)
            messages.value = data.data.result.reverse()
        } catch (error) {
            console.log(error.reponse || error)
        }
    }

    function connect(userId = currentUserId.value) {

        currentUserId.value = userId
        const token = localStorage.getItem("access_token")

        if (!token) {
            console.log("token topilmadi")
            return
        }

        if (!userId) {
            console.log("userId topilmadi")
            return
        }

        ws.value = new WebSocket(`ws://localhost:8000/ws/chat/${userId}/?token=${token}`)

        ws.value.onopen = () => {
            console.log("ulandi")
            isConnect.value = true
        }

        ws.value.onclose = () => {
            console.log("uzildi")
            isConnect.value = false
        }

        ws.value.onmessage = (e) => {
            const data = JSON.parse(e.data)
            // console.log(data)
            if (data.type === "chat_send") {
                messages.value.push(data)
            } else if (data.type === "partner_online") {
                is_online(data)
            } else if (data.type === "message_read") {
                // console.log(data)
                onread(data.reader_id)
                messages.value = messages.value.map(msg => {
                    if (msg.sender_id !== userId) {
                        return { ...msg, is_read: true }
                    }
                    return msg
                })
            }
        }

        ws.value.onerror = (e) => {
            console.error("WebSocket xatosi:", e)
        }
    }

    function is_online(data) {
        partner_online.value = data.is_online
        return data.value
    }

    function SendMessage(text) {
        if (!text.trim()) return

        if (ws.value?.readyState === WebSocket.OPEN) {
            ws.value.send(JSON.stringify({ message: text.trim() }))
        } else {
            console.log("web socket ulanmagan")
        }
    }

    function disconnect() {
        ws.value?.close()
        ws.value = null
    }

    return { messages, isConnect, partner_online, connect, SendMessage, disconnect, getChatHistory, is_online }
}