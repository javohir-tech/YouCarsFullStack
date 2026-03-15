<template>
    <div class="container">
        <a-result status="404" title="404" sub-title="Sorry, the page you visited does not exist.">
            <template #extra>
                <router-link to="/">
                    <a-button type="primary">Back Home</a-button>
                </router-link>
            </template>
        </a-result>
    </div>
</template>

<script setup>

</script>

<style scoped></style>