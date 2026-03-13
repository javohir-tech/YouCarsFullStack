import api from "@/utils/axios";
import axios from "axios";
import { ref } from "vue";


export default function useFetch() {
    const data = ref(null)
    const loading = ref(false)
    const error = ref(null)

    const getData = async (apiUrl) => {
        loading.value = true
        try {
            const response = await api.get(apiUrl)
            // console.log(response.data)
            data.value = response.data
        } catch (err) {
            error.value = err
            console.log(err.response || err)
        } finally {
            loading.value = false
        }
    }

    return { data, loading, error, getData }
}

