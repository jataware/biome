<template>
    <div class="job-notification">
        <Accordion v-if="notificationType === 'response'">
            <AccordionTab
                :pt="{
                    headerIcon: { class: [`job-notification-tab-icon`] },
                    headerAction: { class: [`job-notification-tab-headeraction`] },
                    content: { class: [`job-notification-tab-content`] },
                }"
            >
                <template #header>
                    <span class="job-name job-name-response">
                        Job
                    </span>
                    <Badge
                        :value="job.queue_order" 
                        shape="circle" 
                        :severity="biomeJobColorMap[job.status]"
                    />
                    <span class="job-response-text" v-if="notificationType === 'response'">
                        has finished. Click to expand response.
                    </span>
                </template>
                <template #default>
                    {{ job?.response }}
                </template>
            </AccordionTab>
        </Accordion>

        <div v-if="notificationType === 'creation'">
            <span class="job-name job-name-created">
                Job
            </span>
            <Badge
                :value="job.queue_order" 
                shape="circle" 
                :severity="biomeJobColorMap[job.status]"
            />
            <span class="job-creation">
                has been started. You can track its progress in the jobs sidebar on the right.
            </span>
        </div>

    </div>
</template>

<script setup lang="ts">
import { defineProps, ref, type Ref, inject, computed, onBeforeMount, defineExpose, getCurrentInstance, onBeforeUnmount} from "vue";
import { BeakerSessionComponentType } from 'beaker-vue/src/components/session/BeakerSession.vue';
import Badge from 'primevue/badge';
import Accordion from "primevue/accordion";
import AccordionTab from "primevue/accordiontab";
import { type BiomeJob, biomeJobColorMap } from "./BiomeJob";

const props = defineProps([
    "cell",
]);

const instance = getCurrentInstance();
const beakerSession = inject<BeakerSessionComponentType>("beakerSession");
const cell = ref(props.cell);
const job: Ref<BiomeJob> = ref(props.cell?.metadata?.job);
const notificationType = ref(props.cell?.metadata?.type);

// no-ops, read only cell
const no_op = () => {
    return;
}
const execute = no_op;
const enter = no_op;
const exit = no_op;
const clear = no_op;
defineExpose({
    execute,
    enter,
    exit,
    clear,
});

onBeforeMount(() => {
    beakerSession.cellRegistry[cell.value.id] = instance.vnode;
})

onBeforeUnmount(() => {
    delete beakerSession.cellRegistry[cell.value.id];
});

</script>

<script lang="ts">
import { BeakerRawCell } from "beaker-kernel";
export default {
    modelClass: BeakerRawCell
};
</script>

<style lang="scss" >

.job-notification {
    margin-bottom: 1rem;
    display:flex;
    flex-direction: column;
}

.job-name {
    padding-right: 0.25rem;
    font-weight: 600;
}

.job-name-created {
    padding-left: 1rem;
}

.job-response-text, .job-creation {
    padding-left: 0.25rem;
}

.job-response {
    padding-top: 0.5rem;
}

.job-notification-tab-icon {
    flex: 0 0 auto;
    margin-right: 0.5rem;
}

.job-notification-tab-content {
    border: none;
    background: none;
}

a.job-notification-tab-headeraction {
    background: none;
    padding: 0 0 0 0;
    display: flex;
    align-items: center;
    flex-direction: row;
    border:none;
}

.p-accordion .p-accordion-header a.p-accordion-header-link {
    background: none;
}


</style>
