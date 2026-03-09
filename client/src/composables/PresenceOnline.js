import { ref } from "vue";

export function PresenceOnline() {

    const ws = ref(null)

    function connect() {

        const token = localStorage.getItem("access_token")

        if (!token) {
            console.log("token topilmadi")
            return
        }


        ws.value = new WebSocket(`ws://localhost:8000/ws/online/?token=${token}`)

        ws.value.onopen = () => {
            console.log("online ga ulandi")
        }

        ws.value.onmessage = (e) => {
            const data = JSON.parse(e.data)
            console.log(data)
        }

        ws.value.onclose = () => {
            console.log("onlineda uzildi")
        }
    }

    function disconnect(){
        ws.value?.close()
        ws.value = null
    }

    return { connect , disconnect }
}