import { defineStore } from "pinia";

export const useConversationStore = defineStore('conversations', {
    state: () => ({
        conversations: [],
        isConnect: false
    }),
    getters: {
        userAvatar: (state) => (userId) => {
            const conversation = state.conversations.find(c => c.partner_id === userId)
            return conversation?.avatar || null
        },
        connected: (state) => {
            return state.isConnect
        },
        unread_count: (state) => {
            return state.conversations.reduce((acc, curr) => acc + curr.unread_count, 0)
        }
    },
    actions: {
        add_converstions(conversations) {
            this.conversations = conversations
        },
        on_message(message) {

            if (message.is_new_partner) {
                this.conversations.unshift({ ...message, unread_count: 1 })
            } else {
                const partner_id = message.partner_id
                const partner_index = this.conversations.findIndex(c => c.partner_id === partner_id)

                if (partner_index === -1) {
                    this.conversations.unshift({ ...message, unread_count: 1 })
                    return
                }
                let unread_count = this.conversations[partner_index]?.unread_count || 0
                const is_online = this.conversations[partner_index]?.is_online
                if (!message.last_sent_me && !message.is_read) {
                    unread_count += 1
                }
                this.conversations.splice(partner_index, 1)
                this.conversations.unshift({ ...message, unread_count: unread_count, is_online })
            }
        },
        onread(userId) {
            const last_message_index = this.conversations.findIndex(c => c.partner_id === userId)
            const last_message = this.conversations[last_message_index]
            if (last_message?.is_read === false) {
                last_message.is_read = true
                last_message.unread_count = 0
            }
        },
        set_online(partner_id, is_online) {
            const index = this.conversations.findIndex(c => c.partner_id === partner_id)
            if (index !== -1) {
                this.conversations[index] = { ...this.conversations[index], is_online }
            }
        }
    }
})