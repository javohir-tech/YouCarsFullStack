import { defineStore } from "pinia";

export const useConversationStore = defineStore('conversations', {
    state: () => ({
        conversations: [],
        isConnect: false
    }),
    getters: {

    },
    actions: {
        add_converstions(conversations) {
            this.conversations = conversations
        },
        on_message(message) {

            if(message.is_new_partner){
                this.conversations.unshift({...message , unread_count : 1})
            }else{   
                const partner_id = message.partner_id
                const partner_index = this.conversations.findIndex(c => c.partner_id === partner_id)
                let unread_count = this.conversations[partner_index]?.unread_count || 0
                unread_count+=1
                this.conversations.splice(partner_index , 1)
                this.conversations.unshift({...message , unread_count : unread_count})
            }
        }
    }
})