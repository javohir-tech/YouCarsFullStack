import { defineStore } from "pinia";

export const useConversationStore = defineStore('conversations', {
    state: () => ({
        conversations : [],
        isConnect : false
    }),
    getters : {

    }, 
    actions:{
        add_converstions(conversations){
            this.conversations = conversations
        }
    }
})