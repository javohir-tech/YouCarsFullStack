import { ref } from "vue"

export function useChat(userId) {
    const messages = ref([])
    const ws = ref(null)
    const isConnect = ref(false)

    function connect() {
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
            messages.value.push(data)
        }

        ws.value.onerror = (e) => {
            console.error("WebSocket xatosi:", e)
        }
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

    return { messages, isConnect, connect , SendMessage , disconnect }
}