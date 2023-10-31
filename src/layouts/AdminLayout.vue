<template>
  <q-layout view="hHh lpR fFf">
    <q-page-container class="justify-center">
      <q-page
        class="window-height window-width row justify-center items-center"
        style="background-color: #009688"
      >
        <q-card style="width: 1100px">
          <q-tabs
            v-model="tab"
            dense
            class="text-grey"
            active-color="primary"
            indicator-color="primary"
            align="justify"
          >
            <q-tab name="transcript" label="Transcript" />
            <q-tab name="audio" label="Audio" />
            <q-tab name="sample" label="Sample" />
            <q-tab name="dataset" label="Dataset" />
            <q-tab name="model" label="Model" />
          </q-tabs>
          <q-separator />
          <q-tab-panels v-model="tab" animated class="shadow-2 rounded-borders">
            <q-tab-panel name="transcript">
              <TranscriptsManager />
            </q-tab-panel>
            <q-tab-panel name="audio">
              <AudiosManager />
            </q-tab-panel>
            <q-tab-panel name="sample">
              <SamplesManager />
            </q-tab-panel>
            <q-tab-panel name="dataset">
              <DatasetsManager />
            </q-tab-panel>
            <q-tab-panel name="model">
              <ModelsManager />
            </q-tab-panel>
          </q-tab-panels>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import SamplesManager from "../components/SamplesManager.vue";
import TranscriptsManager from "../components/TranscriptsManager.vue";
import AudiosManager from "../components/AudiosManager.vue";
import DatasetsManager from "src/components/DatasetsManager.vue";
import ModelsManager from "src/components/ModelsManager.vue";
import { defineComponent, ref } from "vue";
import axios from "axios";
import { onMounted } from "vue";

onMounted(() => {
  this.fetchData();
});

export default defineComponent({
  name: "SamplesLayout",

  components: {
    SamplesManager,
    TranscriptsManager,
    AudiosManager,
    DatasetsManager,
    ModelsManager,
  },
  methods: {},

  data() {
    return {
      ip: "http://localhost:80",
      tab: "transcript",
    };
  },
});
</script>
