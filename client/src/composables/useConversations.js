import { ref } from "vue";

export function useConversations() {

    const ws = ref(null)
    const isConnect = ref(false)

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

        ws.value.onmessage = (e)=>{
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

    return {isConnect , connect}
}