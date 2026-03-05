import api from "@/utils/axios";
import { ref } from "vue";
import { useConversationStore } from "@/store/useConversationStore";

export function useConversations() {

    const ws = ref(null)
    const isConnect = ref(false)
    const loading = ref(false)
    const conversationStore = useConversationStore()

    async function fetchConversation() {
        loading.value = true
        try {
            const { data } = await api.get("/api/conversations")
            conversationStore.add_converstions(data)
        } catch (error) {
            console.log(error.response || error)
        } finally {
            loading.value = false
        }
    }

    function connect() {
        const token = localStorage.getItem("access_token")

        if (!token) {
            console.log("token topiladi")
            return
        }

        ws.value = new WebSocket(`ws://localhost:8000/ws/conversations/?token=${token}`)

        ws.value.onopen = () => {
            console.log("ulandi")
        }

        ws.value.onmessage = (e) => {
            const data = JSON.parse(e.data)
            console.log(data)
        }

        ws.value.onclose = () => {
            console.log("uzildi")
        }

        ws.value.onerror = (err) => {
            console.log("Websocket hatosi :", err)
        }
    }

    function disconnect() {
        ws.value?.close()
        ws.value = null
    }

    return { loading, isConnect, disconnect, connect, fetchConversation }
}