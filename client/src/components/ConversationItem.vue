<template>
    <div>
        <router-link :to="`/profile/chat/${props.partner_id}/${props.partner_name}`">
            <a-flex justify="space-between" align="center" class="partner_box">
                <a-flex align="center" gap="10" class="partner_info">
                    <div class="avatar">
                        <img :src="avatar" :alt="props.partner_name">
                        <span class="is_online" :class="!true ? 'online' : ''"></span>
                    </div>
                    <div class="partner">
                        <p class="partner_name">{{ props.partner_name }}</p>
                        <p class="last_message">{{ props.last_message }}</p>
                    </div>
                </a-flex>
                <div class="time_unread">
                    <a-flex align="center" gap="15">
                        <AudioOutlined  v-if="props.mute" class="call"/>
                        <AudioMutedOutlined v-else class="call" />
                        <p>{{ last_message_time }}</p>
                    </a-flex>
                    <p v-if="props.last_sent_me" class="is_read" :class="props.is_read ? 'read' : ''">
                        <CheckOutlined />
                    </p>
                    <p v-if="props.unread_count !== 0" class="unread_count">{{ props.unread_count }}</p>
                </div>
            </a-flex>
        </router-link>
    </div>
</template>

<script setup>
import { AudioMutedOutlined, AudioOutlined, CheckOutlined } from '@ant-design/icons-vue';
import { computed } from 'vue';


const props = defineProps({
    partner_id: String,
    avatar: String,
    partner_name: String,
    last_message: String,
    last_message_time: String,
    is_read: {
        type: Boolean, 
        default : false
    },
    last_sent_me : Boolean,
    unread_count: Number,
    mute: Boolean
})

const avatar = computed(() => {
    if (props.avatar) {
        return props.avatar
    }

    return `https://api.dicebear.com/9.x/initials/svg?seed=${props.partner_name}`
})

const last_message_time = computed(() => {
    if (!props.last_message_time) return ""
    const date = new Date(props.last_message_time)
    return date.toLocaleTimeString("uz-Uz", { hour: "2-digit", minute: "2-digit" })
})

</script>

<style scoped>
p {
    margin-bottom: 8px;
}

.partner_box {
    background-color: rgba(246, 246, 246, 1);
    padding: 25px 10px 20px 10px;
    border-radius: 10px;
    position: relative;
}

.avatar {
    width: 48px;
    height: 48px;
    border-radius: 100%;
    position: relative;

    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 100%;
    }
}

.is_online {
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 100%;
    position: absolute;
    background-color: rgba(152, 152, 152, 1);
    bottom: 0;
    right: 0;
}

.online {
    background-color: rgba(7, 197, 83, 1);
}

.partner_name {
    color: rgba(71, 71, 71, 1);
    font-weight: 700;
    font-size: 16px;
}

.last_message,
.time_unread {
    color: rgba(152, 152, 152, 1);
    font-weight: 500;
    font-size: 14px;
}

.is_read {
    text-align: end;
}

.read{
    color: rgba(38, 132, 229, 1);
}

.unread_count {
    background-color: rgba(38, 132, 229, 1);
    text-align: center;
    font-size: 13px;
    height: 20px;
    width: 20px;
    border-radius: 100%;
    color: rgba(255, 255, 255, 1);
    display: flex;
    align-items: center;
    justify-content: center;
    position: absolute;
    top: 5px;
    right: 10px;
}

.call{
    font-size: 16px;
}

@media(max-width : 768px) {
    .partner_box {
        background-color: rgba(255, 255, 255, 1);
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

}
</style>