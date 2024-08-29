<template>
    <div class="card flex justify-content-center">
        <Sidebar v-model:visible="visible" header="Jobs" position="right">
            <Accordion>
                <AccordionTab 
                    v-for="job, id in jobs" 
                    :key="id"
                    :pt="{
                        root: {
                            class: [`job-tab`]
                        },
                        header: {
                            class: [`job-tab-header`]
                        },
                        headerAction: {
                            class: [`job-tab-headeraction`]
                        },
                        content: {
                            class: [`job-tab-content`]
                        },
                        headerIcon: {
                            class: [`job-tab-icon`]
                        }
                    }"
                >
                    <template #header>
                        <span class="job-header-container">
                            <Badge 
                                :value="job.queue_order" 
                                class="job-header-badge" 
                                shape="circle" 
                                :severity="colorMap[job.status]"
                            />
                            <span class="job-uuid">{{ formatJob(job, id) }}</span>
                        </span>
                    </template>
                </AccordionTab>
            </Accordion>
        </Sidebar>
        <Button icon="pi pi-arrow-left" @click="visible = true" />
    </div>
</template>

<script setup lang="ts">
import { ref, defineProps } from 'vue';
import Sidebar from 'primevue/sidebar';
import Button from 'primevue/button';
import Badge from 'primevue/badge';
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';
import { type BiomeJobCollection, type BiomeJobStatus } from "./BiomeJob"

const props = defineProps<{
  jobs: BiomeJobCollection
}>()

const visible = ref()

const colorMap: {[key in BiomeJobStatus]: string} = {
    started: 'secondary',
    cancelled: 'warning',
    deferred: 'warning',
    failed: 'danger',
    finished: 'success',
    queued: 'info',
    scheduled: 'info'
}

const formatJob = (job, id) => {
    if (job?.url) {
        if (job?.task) {
            return `${job.url}: ${job.task}`
        }
        return job.url
    }
    return id
}

</script>

<style lang="scss">

div.job-tab {
    margin-bottom: 1rem;
}

.job-tab-icon {
    flex: 0 0 auto;
    margin-right: 0.5rem;
}

.job-header-container {
    display: flex;
    align-items: center;
    width: 100%;
    margin: auto;
}

.job-header-badge {
    margin-right: 0.5rem;
}

.job-uuid {
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow-x: hidden;
    width: 100%;
    font-weight: 400;
}

.job-tab-content {
    border: none;
}

a.job-tab-headeraction {
    background: none;
    padding: 0 0 0 0;
    display: flex;
    align-items: center;
    flex-direction: row;
    border:none;
}

</style>
