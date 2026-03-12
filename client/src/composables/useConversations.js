import api from "@/utils/axios";
import { ref } from "vue";
import { useConversationStore } from "@/store/useConversationStore";
import { notification } from 'ant-design-vue';
import { useRouter, useRoute } from "vue-router";

const ws = ref(null)
const loading = ref(false)
const isConnect = ref(false)

export function useConversations() {

    const conversationStore = useConversationStore()
    const router = useRouter()
    const route = useRoute()

    async function fetchConversation() {
        const token = localStorage.getItem("access_token")
        if(!token){
            console.log("token topilmadi")
            return  
        }
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
            conversationStore.isConnect = true
            console.log("ulandi")
        }

        ws.value.onmessage = (e) => {
            const data = JSON.parse(e.data)
            if (data.type === "conversation") {
                // console.log(data)
                conversationStore.on_message(data)
                if (route.params.userId !== data.partner_id && route.params.username !== data.partner) {
                    notification.info({
                        message: `${data.partner}`,
                        description: data.last_message,
                        placement: "bottomRight",
                        style: { cursor: "pointer" },
                        onClick: async () => {
                            router.push(`/chat/${data.partner_id}/${data.partner}`)
                        },
                    });
                }
            } else if (data.type === "online_statuses") {
                // console.log(data.statuses)
                for (let user_id in data.statuses) {
                    conversationStore.set_online(user_id, data.statuses[user_id])
                }
            } else if (data.type === "partner_online") {
                conversationStore.set_online(data.user_id, data.is_online)
                // console.log(data)
            }
        }

        ws.value.onclose = () => {
            console.log("uzildi con")
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