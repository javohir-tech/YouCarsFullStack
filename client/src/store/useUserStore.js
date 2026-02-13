import { defineStore } from "pinia";

export const useUserStore = defineStore('user', {
    state: () => (
        {
            username: localStorage.getItem('username') || "",
            access_token: localStorage.getItem("access_token") || "",
            email: localStorage.getItem("email") || "",
            verify_token: localStorage.getItem("verify_token") || "",
            edit_password_token: localStorage.getItem("edit_password_token") || "",
            email_edit_token: localStorage.getItem("email_edit_token") || "",
            new_email: localStorage.getItem("new_email") || "",
            user_image : localStorage.getItem("profile" ) || undefined , 
        }
    ),
    getters: {
        get_user: (state) => state.username,
        avatarUrl: (state) =>state.user_image ? state.user_image : `https://api.dicebear.com/9.x/initials/svg?seed=${state.username}`
    },
    actions: {
        add_user(username, email, access_token) {
            this.username = username
            this.email = email
            this.access_token = access_token
            localStorage.setItem("username", username)
            localStorage.setItem("email", email)
        },
        updateAvatar(photo){
            this.user_image = photo
            localStorage.setItem('profile' , photo)
        },
        add_email(email) {
            this.email = email
            localStorage.setItem("email", email)
        },
        add_new_email(new_email) {
            this.new_email = new_email
            localStorage.setItem("new_email", new_email)
        },
        remove_new_email() {
            this.new_email = ""
            localStorage.removeItem("new_email")
        },
        add_verify_token(verify_token) {
            this.verify_token = verify_token
            localStorage.setItem("verify_token", verify_token)
        },
        remove_verify_token() {
            this.verify_token = "",
                localStorage.removeItem("verify_token")
        },
        add_edit_password_token(edit_password_token) {
            this.edit_password_token = edit_password_token
            localStorage.setItem("edit_password_token", edit_password_token)
        },
        remove_edit_password_token() {
            this.edit_password_token = "",
                localStorage.removeItem("edit_password_token")
        },
        add_email_edit_token(email_edit_token) {
            this.email_edit_token = email_edit_token
            localStorage.setItem("email_edit_token", email_edit_token)
        },
        remove_email_edit_token() {
            this.email_edit_token = ""
            localStorage.removeItem("email_edit_token")
        },
        add_access_token(access_token){
            this.access_token = access_token
        },
        clear() {
            this.username = ""
            this.email = ""
            this.access_token = ""
            this.verify_token = ""
            this.edit_password_token = ""
        }
    }

})