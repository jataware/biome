<template>
    <div class="card flex justify-content-center">
        <Sidebar v-model:visible="visible" header="Jobs" position="right" class="jobs-sidebar">
            <Accordion v-autoscroll>
                <AccordionTab 
                    v-for="[id, job] in chronologicalJobs" 
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
                                :severity="biomeJobColorMap[job.status]"
                            />
                            <span class="job-uuid">{{ formatJob(job, id) }}</span>
                        </span>
                    </template>
                    <div class="job-info">
                        <span class="job-uuid-small">{{ id }}</span>
                        <span class="job-url" v-if="job?.url">{{ job.url }}</span>
                        <span class="job-divider" />
                        <span class="job-status">Status: <b>{{ job.status }}</b></span>
                        <span class="job-task" v-if="job?.task">{{ job.task }}</span>
                    </div>
                    <span v-if="job?.logs" class="job-divider" />
                    <Accordion v-if="job?.logs">
                        <AccordionTab 
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
                            Details
                        </template>
                        <template #default>
                            <JobTrackerLogs :logs="job.logs" />
                        </template>
                        </AccordionTab>
                    </Accordion>
                </AccordionTab>
            </Accordion>
        </Sidebar>
        <Button 
            @click="visible = true" 
            rounded
            outlined
            :severity="jobsColor"
            size="small"
            class="jobs-button"
        >
            <span>{{ numJobs }}</span>
        </Button>
    </div>
</template>

<script setup lang="ts">
import { ref, defineProps, computed } from 'vue';
import Sidebar from 'primevue/sidebar';
import Button from 'primevue/button';
import Badge from 'primevue/badge';
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';
import { BiomeJob, type BiomeJobCollection, biomeJobColorMap, getJobGroupColor } from "./BiomeJob"
import JobTrackerLogs from './JobTrackerLogs.vue';

const props = defineProps<{
  jobs: BiomeJobCollection
}>()

const visible = ref();

const numJobs = computed(() => Object.keys(props.jobs).length);

const chronologicalJobs = computed((): [string, BiomeJob][] => 
    Object.entries(props.jobs).sort(([_, {queue_order}]) => queue_order));
        
const jobsColor = computed(() => getJobGroupColor(props.jobs))

const addNotification = (job: BiomeJob, duration: number) => {
    return '';
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

div.jobs-sidebar {
    width: 48rem;
    max-width: 80%;
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

button.jobs-button {
    padding: 0;
    width: 2rem;
    height: 2rem;
    align-items: center;
    border: 0.175rem solid;
    span {
        font-weight: 900;
        padding: 0;
        margin: auto;
    }
}

.job-tab-content {
    padding: 0.5rem 0 1.25rem 1.25rem;
}

.job-info {
    display: flex;
    flex-direction: column;
    .job-uuid-small {
        font-size: 0.8rem;
        font-style: italic;
        padding-bottom: 0.25rem;
    }
    .job-url {
        font-size: 0.8rem;
        padding-bottom: 0.5rem;
    }
    .job-status {
        padding-bottom: 0.5rem;
    }
    .job-task {
        padding-bottom: 0.5rem;
    }
}

.job-divider {
    width: 80%;
    background-color: var(--surface-200);
    height: 1px;
    margin: 0.25rem 0 0.5rem 0;
}

</style>
