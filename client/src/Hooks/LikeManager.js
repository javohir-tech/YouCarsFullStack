import api from "@/utils/axios";
import { ref } from "vue";

export default function LikeManager() {
    const like = ref(false)

    const handleLike = async (id) => {
        try {
            await api.post(`/cars/car/like/${id}/`)
            like.value = true
            console.log(like.value)
        } catch (error) {
            console.log(error.response || error)
        }
    }

    const handleDisLike = async (id) => {
        try {
            await api.delete(`/cars/car/like/${id}/`)
            like.value = false
            console.log(like.value)
        } catch (error) {
            console.log(error.response || error)
        }
    }

    return { like, handleLike, handleDisLike }
}