import { defineStore } from "pinia";

export const useUserStore = defineStore('user', {
    state: () => (
        {
            username: localStorage.getItem('username') || "",
            access_token: localStorage.getItem("access_token") || "",
            email: localStorage.getItem("email") || "",
        }
    ),
    getters: {
        get_user: (state) => state.username,
        avatarUrl : (state) => `https://api.dicebear.com/9.x/initials/svg?seed=${state.username}`
    },
    actions: {
        add_user(username, email, access_token) {
            this.username = username
            this.email = email
            this.access_token = access_token
            localStorage.setItem("username", username)
            localStorage.setItem("email", email)
        },

        clear(){
            this.username = ""
            this.email = ""
            this.access_token = ""
        }
    }

})