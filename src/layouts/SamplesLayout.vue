<template>
  <q-layout view="hHh lpR fFf">
    <q-page-container class="justify-center">
      <q-page
            class="window-height window-width row justify-center items-center"
            style="background-color: #009688"
      >
        <q-card  style="width:1100px">
          <q-tabs
            v-model="tab"
            dense
            class="text-grey"
            active-color="primary"
            indicator-color="primary"
            align="justify"
          >
            <q-tab name="transcript" label="Transcipt" />
            <q-tab name="audio" label="Audio" />
            <q-tab name="sample" label="Sample" />
            <q-tab name="dataset" label="Dataset" />
            <q-tab name="model" label="Model" />
          </q-tabs>
          <q-separator />
          <q-tab-panels v-model="tab" animated class="shadow-2 rounded-borders">
            <q-tab-panel name="transcript">
              <TranscriptsManager/>
            </q-tab-panel>
            <q-tab-panel name="sample">
              <SamplesManager/>
            </q-tab-panel>
          </q-tab-panels>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import SamplesManager from '../components/SamplesManager.vue'
import TranscriptsManager from '../components/TranscriptsManager.vue'
import { defineComponent, ref } from "vue";
import axios from "axios";
import { onMounted } from 'vue';

onMounted(() => {
  this.fetchData()
})

export default defineComponent({
  name: "SamplesLayout",

  components: {
    SamplesManager,
    TranscriptsManager
  },
  methods: {
    async AddSample() {
      console.log(this.contentAdd);
      console.log(this.file);
      let data = new FormData();
      data.append('content', this.contentAdd );
      data.append('audio', this.file);

      let config = {
        method: 'post',
        maxBodyLength: Infinity,
        url: `${this.ip}/addsample`,
        headers: {
        ...(data.getHeaders
          ? data.getHeaders()
          : { "Content-Type": "multipart/form-data" }),
        },
        data : data
      };

      axios.request(config)
      .then((response) => {
        console.log(JSON.stringify(response.data));
      })
      .catch((error) => {
        console.log(error);
      });

    },
    deleteSample(id) {
      let config = {
        method: 'post',
        maxBodyLength: Infinity,
        url: `${this.ip}/deletesample?id=${id}`,
        headers: { }
      };

      axios.request(config)
      .then((response) => {
        console.log(JSON.stringify(response.data));
      })
      .catch((error) => {
        console.log(error);
      });

    },

    editTranscript(id, content) {
      if (this.contentEdit != content) {
        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: `${this.ip}/edittranscript?id=${id}&content=${this.contentEdit}`,
          headers: { }
        };

        axios.request(config)
        .then((response) => {
          console.log(JSON.stringify(response.data));
        })
        .catch((error) => {
          console.log(error);
        });
   
      }
    },
    fetchData() {
      let config = {
        method: 'get',
        maxBodyLength: Infinity,
        url: `${this.ip}/samples?start_idx=${(this.currentPageSample - 1) * 5}&count=${5}`,
        headers: { }
      };

      axios.request(config)
      .then((response) => {
        this.samples = response.data;
      })
      .catch((error) => {
        console.log(error);
      });

    }
  },

  data() {
    return {
      file: null,
      addDialog: false,
      editDialog: false,
      contentAdd: "",
      contentEdit: "",
      transcripts: [],
      audios: [],
      samples: [],
      currentPageTranscript: 1,
      currentPageAudio: 1,
      currentPageSample: 1,
      ip: "http://localhost:80",
      tab: "sample"
    };
  },
});
</script>
