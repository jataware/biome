<template>
    <div id="app">
        <BeakerSession
            ref="beakerSessionRef"
            :connectionSettings="props.config"
            sessionName="dev_interface"
            :sessionId="sessionId"
            defaultKernel="beaker_kernel"
            :renderers="renderers"
            @iopub-msg="iopubMessage"
            @unhandled-msg="unhandledMessage"
            @any-msg="anyMessage"
            @session-status-changed="statusChanged"
            v-keybindings="sessionKeybindings"
        >
            <div class="beaker-dev-interface">
                <header style="justify-content: center;">
                    <VerticalToolbar style="align-self: flex-start;">
                        <template #start>
                            <Button
                                outlined
                                size="small"
                                icon="pi pi-angle-down"
                                iconPos="right"
                                class="connection-button"
                                @click="() => {contextSelectionOpen = !contextSelectionOpen}"
                                v-tooltip.right="{
                                    value: `${statusLabel}: ${beakerSessionRef?.activeContext?.slug || ''}`, 
                                    showDelay: 300
                                }"
                                :label="beakerSessionRef?.activeContext?.slug"
                                :loading="!(beakerSessionRef?.activeContext?.slug)"
                            >
                                <i class="pi pi-circle-fill" :style="`font-size: inherit; color: var(--${connectionColor});`" />
                            </Button>
                            <Button
                                @click="resetNotebook"
                                v-tooltip.right="{value: 'Reset notebook', showDelay: 300}"
                                icon="pi pi-refresh"
                                size="small"
                                severity="info"
                                text
                            />
                            <Button
                                @click="toggleFileMenu"
                                v-tooltip.right="{value: 'Show file menu', showDelay: 300}"
                                icon="pi pi-file-export"
                                size="small"
                                severity="info"
                                text
                            />
                            <OverlayPanel ref="isFileMenuOpen" style="overflow-y: auto; height:40em;">
                                <BeakerFilePane/>
                            </OverlayPanel>
                            <DarkModeButton :toggle-dark-mode="toggleDarkMode"/>
                        </template>
                        <template #center>
                            <div class="vertical-toolbar-divider" />
                        </template>
                        <template #end>
                            <a  
                                :href="`/${sessionId == 'dev_session' ? '' : '?session=' + sessionId}`" 
                                v-tooltip.right="{value: 'To Notebook View', showDelay: 300}"
                            >
                                <Button
                                    icon="pi pi-book"
                                    size="small"
                                    severity="info"
                                    text
                                />

                            </a>
                        </template>
                    </VerticalToolbar>
                </header>
                <main style="display: flex; overflow-y: auto; overflow-x: hidden;">
                    <div class="central-panel">
                        <ChatPanel
                            ref="chatPanelRef"
                            :cellMap="cellComponentMapping"
                            v-autoscroll
                        >
                            <template #help-text>
                                <p>Hi! I'm your Biome Agent and I can help you do tasks related to medicinal data sources.</p>
                                <p>Feel free to ask me about searching for data sources, fetching data, and navigating that downloaded data.</p>
                                <p>
                                    On top of answering questions, I can actually run code in a python environment, and evaluate the results. 
                                    This lets me do some pretty awesome things like: 
                                </p>
                                <p>"Search for data sources related to proteomics"</p>
                                <p>Just shoot me a message when you're ready to get started.</p>
                            </template>
                            <template #notebook-background>
                                <div class="welcome-placeholder">
                                </div>
                            </template>
                        </ChatPanel>
                        <AgentQuery
                            class="agent-query-container"
                        />
                    </div>
                    <VerticalToolbar>
                        <template #start>
                            <JobTracker :jobs="jobs"/>
                        </template>
                    </VerticalToolbar>
                </main>
            </div>
            <BeakerContextSelection
                :isOpen="contextSelectionOpen"
                :contextProcessing="contextProcessing"
                @context-changed="(contextData) => {console.log(contextData);beakerSessionRef.setContext(contextData)}"
                @close-context-selection="contextSelectionOpen = false"
            />
        </BeakerSession>
        <!-- Modals, popups and globals -->
        <Toast position="bottom-right" />
    </div>
</template>

<script setup lang="ts">
import { standardRendererFactories } from '@jupyterlab/rendermime';
import { JupyterMimeRenderer } from 'beaker-kernel';

import AgentQuery from 'beaker-vue/src/components/chat-interface/AgentQuery.vue';
import ChatPanel from 'beaker-vue/src/components/chat-interface/ChatPanel.vue';
import DarkModeButton from 'beaker-vue/src/components/chat-interface/DarkModeButton.vue';
import VerticalToolbar from 'beaker-vue/src/components/chat-interface/VerticalToolbar.vue';
import BeakerCodeCell from 'beaker-vue/src/components/cell/BeakerCodeCell.vue';
import BeakerLLMQueryCell from 'beaker-vue/src/components/cell/BeakerLLMQueryCell.vue';
import BeakerMarkdownCell from 'beaker-vue/src/components/cell/BeakerMarkdownCell.vue';
import BeakerRawCell from 'beaker-vue/src/components/cell/BeakerRawCell.vue';
import BeakerFilePane from 'beaker-vue/src/components/dev-interface/BeakerFilePane.vue';
import BeakerSession from 'beaker-vue/src/components/session/BeakerSession.vue';

import AnalystDataSourceCell from './AnalystDataSourceCell.vue';
import JobTracker from './JobTracker.vue';

import Button from "primevue/button";
import OverlayPanel from 'primevue/overlaypanel';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';

import { defineProps, inject, nextTick, onBeforeMount, onUnmounted, provide, ref, reactive, defineEmits, computed, shallowRef } from 'vue';
import { DecapodeRenderer, JSONRenderer, LatexRenderer, wrapJupyterRenderer } from 'beaker-vue/src/renderers';

import { IBeakerTheme } from 'beaker-vue/src/plugins/theme';

const { theme, toggleDarkMode } = inject<IBeakerTheme>('theme');
const toast = useToast();
const chatPanelRef = shallowRef();
const contextSelectionOpen = ref(false);
const contextProcessing = ref(false);
import BeakerContextSelection from 'beaker-vue/src/components/session/BeakerContextSelection.vue';
import { cell } from 'beaker-vue/dist/components';

import { BiomeJobCollection } from "./BiomeJob"

const jobs: BiomeJobCollection = reactive({
    "b936477a-55d2-4643-9730-21d200c3b9a2" : {
        status: 'finished',
        response: 'String Resopnse',
        queue_order: 1,
        url: 'google.com',
        task: 'find the forecast for the next seven days'
    },
    "1cf01215-ca30-4ba9-aa00-a1428e1841bb" : {
        status: 'finished',
        response: 'String Resopnse',
        queue_order: 2,
        url: 'pdc.cancer.gov',
        task: 'find data for the case ID: XXXXXX'
    },
    "1cf01215-ca30-4ba9-aa00-a1428e1841ba" : {
        status: 'failed',
        response: 'String Resopnse',
        queue_order: 3,
    },
    "2cf01215-ca30-4ba9-aa00-a1428e1841ba" : {
        status: 'started',
        response: 'String Resopnse',
        queue_order: 4,
    }
});

// NOTE: Right now, we don't want the context changing
const beakerNotebookRef = ref();

const defaultContext = {
    context: "biome", 
    language: "python3", 
    context_info: {}, 
    debug: false, 
    verbose: false 
};

const setDefaultContext = () => {
    beakerSessionRef.value.setContext(defaultContext);
}

// TODO -- WARNING: showToast is only defined locally, but provided/used everywhere. Move to session?
// Let's only use severity=success|warning|danger(=error) for now
const showToast = ({title, detail, life=3000, severity='success' as any}) => {
    toast.add({
        summary: title,
        detail,
        life,
        // for options, seee https://primevue.org/toast/
        severity,
    });
};

provide('show_toast', showToast);

const urlParams = new URLSearchParams(window.location.search);

const sessionId = urlParams.has("session") ? urlParams.get("session") : "dev_session";

const props = defineProps([
    "config",
    "connectionSettings",
    "sessionName",
    "sessionId",
    "defaultKernel",
    "renderers",
]);

const renderers = [
    ...standardRendererFactories.map((factory: any) => new JupyterMimeRenderer(factory)).map(wrapJupyterRenderer),
    JSONRenderer,
    LatexRenderer,
    DecapodeRenderer,
];

const cellComponentMapping = {
    'code': BeakerCodeCell,
    'markdown': BeakerMarkdownCell,
    'query': BeakerLLMQueryCell,
    'raw': BeakerRawCell,
    'data_sources': AnalystDataSourceCell
}

const isFileMenuOpen = ref();

const toggleFileMenu = (event) => {
    isFileMenuOpen.value.toggle(event);
}

const resetNotebook = async () => {
    const session = beakerSessionRef.value.session;
    session.reset();
    setDefaultContext();
};

const connectionStatus = ref('connecting');
const debugLogs = ref<object[]>([]);
const rawMessages = ref<object[]>([])
const previewData = ref<any>();
const saveInterval = ref();
const beakerSessionRef = ref<typeof BeakerSession>();

const statusLabels = {
    unknown: 'Unknown',
    starting: 'Starting',
    idle: 'Ready',
    busy: 'Busy',
    terminating: 'Terminating',
    restarting: 'Restarting',
    autorestarting: 'Autorestarting',
    dead: 'Dead',
    // This extends kernel status for now.
    connected: 'Connected',
    connecting: 'Connecting'
}

const statusColors = {
    connected: 'green-300',
    idle: 'green-400',
    connecting: 'green-200',
    busy: 'orange-400',
};

const statusLabel = computed(() => {
    return statusLabels[beakerSessionRef?.value?.status] || "unknown";

});

const connectionColor = computed(() => {
    // return connectionStatusColorMap[beakerSession.status];
    return statusColors[beakerSessionRef?.value?.status] || "grey-200"
});

const handleJobMessages = msg => {
    console.log("iopub", msg);
    const messageType = msg.header.msg_type;
    if (messageType === "job_create") {
        jobs[msg.content.job_id] = {
            status: 'queued',
            task: msg.content.task,
            url: msg.content.url,
            queue_order: Object.keys(jobs).length + 1
        }
    } else if (msg.header.msg_type === "job_status") {
        jobs[msg.content.job_id].status = msg.content.status;
    } else if (msg.header.msg_type === "job_failure") {
        // TODO: ui failure notice notificaion
        jobs[msg.content.job_id].response = msg.content.response;
    } else if (msg.header.msg_type === "job_response") {
        // TODO: good notification
        jobs[msg.content.job_id].response = msg.content.response;
        jobs[msg.content.job_id].raw = msg.content.raw;
    }
}

const iopubMessage = (msg) => {
    handleJobMessages(msg);
    if (msg.header.msg_type === "preview") {
        previewData.value = msg.content;
    } else if (msg.header.msg_type === "debug_event") {
        debugLogs.value.push({
            type: msg.content.event,
            body: msg.content.body,
            timestamp: msg.header.date,
        });
    } else if (msg.header.msg_type === "data_sources") {
        const metadata = {
            "sources": msg.content.sources
        }
        const newCell = beakerSessionRef.value.session.addRawCell("", metadata);
        newCell.cell_type = "data_sources"
    }
};

const anyMessage = (msg, direction) => {
    rawMessages.value.push({
        type: direction,
        body: msg,
        timestamp: msg.header.date,
    });
};

const unhandledMessage = (msg) => {
    console.log("Unhandled message recieved", msg);
}

const statusChanged = (newStatus) => {
    if (newStatus == 'connected' && beakerSessionRef?.value?.activeContext?.slug !== 'biome') {
        setDefaultContext();
    }
    connectionStatus.value = newStatus == 'idle' ? 'connected' : newStatus;
};

onBeforeMount(() => {
    document.title = "Analyst UI"
    var notebookData: {[key: string]: any};
    try {
        notebookData = JSON.parse(localStorage.getItem("notebookData")) || {};
    }
    catch (e) {
        console.error(e);
        notebookData = {};
    }
    if (notebookData[sessionId]?.data) {
        nextTick(() => {
            const notebook = beakerSessionRef?.value?.session?.notebook;
            if (notebook) {
                notebook.loadFromIPynb(notebookData[sessionId].data);
            }
        });
    }
    saveInterval.value = setInterval(snapshot, 30000);
    window.addEventListener("beforeunload", snapshot);
});

onUnmounted(() => {
    clearInterval(saveInterval.value);
    saveInterval.value = null;
    window.removeEventListener("beforeunload", snapshot);
});

// no state to track selection - find code editor divs and compare to evt
const executeActiveCell = (editorSourceElement) => {
    const panel = chatPanelRef?.value;
    const queryCellComponents = panel?.cellsContainerRef;
    queryCellComponents.forEach(cell => {
        const events = cell?.queryEventsRef;
        if (!events) {
            return;
        }
        events.forEach(eventRef => {
            const codeCellRef = eventRef?.codeCellRef;
            const codeEditor = codeCellRef?.codeEditorRef;
            if (!codeEditor) {
                return;
            }
            if (codeEditor.view._root.activeElement == editorSourceElement) {
                codeCellRef.execute();
            }
        });
    });
}

const sessionKeybindings = {
    "keydown.enter.ctrl.prevent.capture.in-editor": (evt) => {
        executeActiveCell(evt.srcElement);
        // execute
    },
    "keydown.enter.shift.prevent.capture.in-editor": (evt) => {
        // execute
        executeActiveCell(evt.srcElement);
    }
}

const snapshot = () => {
    var notebookData: {[key: string]: any};
    try {
        notebookData = JSON.parse(localStorage.getItem("notebookData")) || {};
    }
    catch (e) {
        console.error(e);
        notebookData = {};
    }
    // Only save state if there is state to save
    const notebook = beakerSessionRef.value.session?.notebook;
    if (notebook) {
        notebookData[sessionId] = {
            data: notebook.toIPynb(),
        };
        localStorage.setItem("notebookData", JSON.stringify(notebookData));
    }
};

</script>

<style lang="scss">
#app {
    margin: 0;
    padding: 0;
    overflow: hidden;
    background-color: var(--surface-b);
}
header {
    grid-area: l-sidebar;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
main {
    grid-area: main;
}
footer {
    grid-area: r-sidebar;
}
.main-panel {
    display: flex;
    flex-direction: column;
    &:focus {
        outline: none;
    }
}
div.beaker-notebook {
    padding-top: 1rem;
}

.central-panel {
    flex: 1000;
    display: flex;
    flex-direction: column;
    max-width: 820px;
    margin: auto;
}

.beaker-dev-interface {
    padding-bottom: 1rem;
    height: 100vh;
    width: 100vw;
    display: grid;
    grid-gap: 1px;
    grid-template-areas:
        "l-sidebar main r-sidebar"
        "l-sidebar main r-sidebar"
        "l-sidebar main r-sidebar";
    grid-template-columns: auto 1fr auto;
    grid-template-rows: auto 1fr auto;
}

div.cell-container {
    position: relative;
    display: flex;
    flex: 1;
    background-color: var(--surface-b);
    flex-direction: column;
    z-index: 3;
    overflow: auto;
}

div.llm-prompt-container {
    margin-right: 0rem;
}

div.llm-query-cell.beaker-chat-cell {
    padding: 0rem 0rem 0rem 0rem;
}

div.llm-prompt-container h2.llm-prompt-text {
    font-size: 1.25rem;
    max-width: 70%;
    margin-left: auto;
    background-color: var(--surface-a);
    padding: 1rem;
    border-radius: 16px;
}

div.llm-prompt-container {
    text-align: right;
    max-width: 60%;
    align-self: end;
}

div.query {
    display: flex;
    flex-direction: column;
}

div.query-steps {
    display: none;
}

div.events div.query-answer {
    background-color: var(--surface-b);
}

div.beaker-toolbar {
    flex-direction: column;
}

div.beaker-toolbar div {
    flex-direction: column;
}

div.central-panel, div.beaker-notebook {
    height: 100%;
}

button.connection-button {
    border: none;
}

div.code-cell {
    margin-bottom: 2rem;
}

div.code-cell.query-event-code-cell {
    margin-bottom: 0.25rem;
}

</style>