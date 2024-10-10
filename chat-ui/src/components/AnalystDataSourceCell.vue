<template>
    <div class="datasource-container">
        <div class="datasource-cell">
            <Card 
                v-for="source in cards" 
                :key="source.name" 
                class="datasource"
            >
                <template #header>
                    <img 
                        class="datasource-logo" 
                        alt="logo" 
                        :src="`data:image/png;base64,${source.logo}`" 
                    />
                </template>
                <template #title>{{ source.name }}</template>
                <template #subtitle>
                    <a class="datasource-link" :href="source.base_url">{{ source.base_url }}</a>
                </template>
                <template #content>
                    <p class="m-0" style="box-sizing: border-box;; overflow-y: auto; margin: 0;">
                        {{ source.purpose }}
                    </p>
                </template>
            </Card>
        </div>
        <div
            class="datasource-show-more-container"
            v-if="cell?.metadata?.sources?.length > numCardsShownByDefault"
        >
            <Button 
                :label="`Show ${showMore ? 'Less' : 'More'}`"
                @click="showMore = !showMore"
                v-if="cell?.metadata?.sources?.length > numCardsShownByDefault"
                class="datasource-show-more"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
import { defineProps, ref, inject, computed, nextTick, onBeforeMount, defineExpose, getCurrentInstance, onBeforeUnmount} from "vue";
import { BeakerSessionComponentType } from 'beaker-vue/src/components/session/BeakerSession.vue';
import Card from 'primevue/card';
import Button from 'primevue/button';

const props = defineProps([
    "cell",
]);

const instance = getCurrentInstance();
const beakerSession = inject<BeakerSessionComponentType>("beakerSession");
const cell = ref(props.cell);
const showMore = ref(false);
const screenWidth = ref(Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0))

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

const getViewportWidth = () => Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);

const numCardsShownByDefault = computed(() => {
    // 940px is the breakpoint for when cards go to rows of 3 instead of 2
    // todo: programatically fetch this?
    return screenWidth.value > 940 ? 3 : 2;
});

const cards = computed(() => {
    let sources = props.cell?.metadata?.sources;
    if (sources !== undefined) {
        return showMore.value ? sources : sources.slice(0, numCardsShownByDefault.value)
    }
    return undefined;
})

onBeforeMount(() => {
    beakerSession.cellRegistry[cell.value.id] = instance.vnode;
    window.addEventListener("resize", () => {
        screenWidth.value = getViewportWidth();
    })
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

.datasource-container {
    margin-bottom: 2rem;
}

.datasource-cell {
    display: flex;
    flex-wrap: wrap;
}

.datasource {
    width: 16rem;
    height: 28rem;
    margin: 5px;
    display: flex;
    flex-direction: column;
}

.datasource-logo {
    width: 100%;
    height: 60px;
    border-radius: 0.5rem 0.5rem 0 0;
    object-fit: contain
}

.datasource-link[href] {
    text-overflow: ellipsis;
    overflow: hidden;
    max-width: 100%;
    display: inline-block;
    white-space: nowrap;
}

.datasource .p-card-body {
    display: flex;
    flex-direction: column;
    flex: 1 1 auto;
    overflow: auto;

    .p-card-title {
        font-size: 1.25rem;
    }
    .p-card-content {
        padding-top: 0rem;
        flex: 1 1 auto;
        overflow: auto;
    }
}

.datasource-show-more-container {
    display: flex;
    flex-direction: row;
    margin-top: 0.5rem;
}
.datasource-show-more {
    margin: auto;
}

</style>
