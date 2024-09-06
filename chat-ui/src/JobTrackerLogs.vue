<template>
    <div v-autoscroll>
        <Fieldset 
            v-for="record, index in history" 
            :legend="titleFromRecord(record)" 
            :key="index"
            toggleable
            :pt="{
                'root': {
                    'class': ['job-tracker-job-header-root']
                },
                'content': {
                    'class': ['job-tracker-job-content']
                }
            }"
        >
            <span v-if="record?.type === 'action'">
                {{ record?.text ?? '' }}
            </span>
            <img 
                v-if="record?.type === 'image'" 
                :src="`http://localhost:8082/${ record?.path }`" 
                class="job-step-image"
            />
        </Fieldset>
    </div>
</template>

<script setup lang="ts">
import { ref, defineProps, computed } from 'vue';
import Fieldset from 'primevue/fieldset';
import Badge from 'primevue/badge';

const props = defineProps([
    'logs'
])

const history = computed(() => 
    (props?.logs?.history ?? []).filter((record) => {
        if (record?.type === 'image') {
            return true;
        }
        const excludedTitles = [
            'Supporting Information Task',
            'Current Downloads'
        ];
        if (excludedTitles.includes(record?.title)) {
            return false;
        }
        return true;
    }));

const titleFromRecord = record => 
    record.type === 'image' ? 'Image' : record ?.title ?? 'action';
</script>

<style lang="scss">

.job-tracker-job-header-root legend a {
    span {
        font-size: 0.8rem;
    }
    padding: 0.4em;
}

.job-tracker-job-header-root {
    margin-bottom: 0.75em;
}

.job-tracker-job-content {
    padding: 0.4rem;
    font-size: 0.8rem;
}

.job-step-image {
    width: 100%;
}

</style>
