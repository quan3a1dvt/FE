<template>
  <div style="display: flex" class="q-mb-sm q-pr-md">
    <q-pagination
      v-model="currentPage"
      :max="1000"
      input
      @update:model-value="(value) => fetchSamples()"
    />
    <q-space></q-space>
    <q-select
      filled
      stack-label
      dense
      style="width: 100px"
      v-model="datasetId"
      :options="datasetOptions"
      label="Dataset"
      emit-value
      map-options
      @update:model-value="
        (value) => {
          fetchSamples();
          currentPage = 1;
        }
      "
    />
    <q-btn label="Add" color="teal" @click="addDialog = true"></q-btn>
    <q-dialog v-model="addDialog">
      <q-card style="min-width: 350px">
        <q-card-section class="q-pt-none">
          <div class="flex q-pt-md">
            <q-input
              style="width: 240px"
              label="Enter sample name"
              type="text"
              dense
              v-model="sampleName"
            />
            <q-space />
            <q-btn label="Find" color="teal" @click="getSampleByName()"> </q-btn>
          </div>
          <div v-if="searchSample != null" class="q-pt-sm">
            {{ transcripts[searchSample.transcriptId].content }}
          </div>
          <div v-if="searchSample != null" class="q-pt-sm">
            <audio controls>
              <source :src="`${ip}/audiourl/${searchSample.audioId}`" type="audio/wav" />
            </audio>
          </div>
        </q-card-section>
        <q-card-actions align="right" class="text-primary">
          <q-btn label="Cancel" v-close-popup />
          <q-btn
            label="Add Sample"
            color="teal"
            v-close-popup
            @click="addSampleToDataset()"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
  <div>
    <div style="border: solid rgb(192, 192, 192); border-width: 0px 0px 1px 0px">
      <div class="flex">
        <div
          style="
            width: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: solid rgb(192, 192, 192);
            border-width: 1px 0px 0px 1px;
          "
        >
          STT
        </div>
        <div
          style="
            width: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: solid rgb(192, 192, 192);
            border-width: 1px 0px 0px 1px;
          "
        >
          Name
        </div>
        <div
          style="
            flex-grow: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            border: solid rgb(192, 192, 192);
            border-width: 1px 0px 0px 1px;
          "
        >
          Content
        </div>
        <div
          style="
            width: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: solid rgb(192, 192, 192);
            border-width: 1px 0px 0px 1px;
          "
        >
          Audio
        </div>
        <div
          style="
            width: 90px;
            border: solid rgb(192, 192, 192);
            border-width: 1px 1px 0px 1px;
          "
        ></div>
      </div>
      <q-separator />
      <div v-for="(sample, index) in samples" :key="sample.id">
        <div class="flex">
          <div
            style="
              width: 50px;
              display: flex;
              align-items: center;
              justify-content: center;
              border: solid rgb(192, 192, 192);
              border-width: 1px 0px 0px 1px;
            "
          >
            {{ index + (this.currentPage - 1) * this.itemPerPage }}
          </div>
          <div
            style="
              width: 100px;
              display: flex;
              align-items: center;
              justify-content: center;
              border: solid rgb(192, 192, 192);
              border-width: 1px 0px 0px 1px;
            "
          >
            {{ sample.name }}
          </div>
          <div
            style="
              width: 150px;
              flex-grow: 1;
              display: flex;
              align-items: center;
              word-break: break-all;
              border: solid rgb(192, 192, 192);
              border-width: 1px 0px 0px 1px;
            "
            class="q-pa-sm"
          >
            {{ transcripts[sample.transcriptId].content }}
          </div>
          <div
            style="
              width: 300px;
              display: flex;
              align-items: center;
              justify-content: center;
              border: solid rgb(192, 192, 192);
              border-width: 1px 0px 0px 1px;
            "
          >
            <audio controls>
              <source :src="`${ip}/audiourl/${sample.audioId}`" type="audio/wav" />
            </audio>
          </div>
          <div
            style="
              width: 90px;
              display: flex;
              align-items: center;
              justify-content: center;
              border: solid rgb(192, 192, 192);
              border-width: 1px 1px 0px 1px;
            "
            class="q-pa-sm"
          >
            <q-btn
              class="q-ml-sm"
              style="width: fit-content"
              label="Delete"
              color="red"
              @click="deleteSampleFromDataset(sample.id)"
            ></q-btn>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import axios from "axios";
import { onMounted } from "vue";

export default defineComponent({
  name: "DatasetsManager",
  components: {},
  methods: {
    async getSampleByName() {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/sample-by-name?name=${this.sampleName}`,
        headers: {},
      };

      axios
        .request(config)
        .then(async (response) => {
          var sample = response.data;
          var transcript = await this.fetchTranscript(sample.transcriptId);
          var audio = await this.fetchAudio(sample.audioId);
          this.transcripts[transcript.id] = transcript;
          this.audios[audio.id] = audio;
          this.searchSample = sample;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async addSampleToDataset() {
      let data = new FormData();
      data.append("datasetId", this.datasetId);
      data.append("sampleId", this.searchSample.id);
      let config = {
        method: "post",
        maxBodyLength: Infinity,
        url: `${this.ip}/dataset-addsample`,
        headers: {
          ...(data.getHeaders
            ? data.getHeaders()
            : { "Content-Type": "multipart/form-data" }),
        },
        data: data,
      };

      axios
        .request(config)
        .then((response) => {
          this.fetchSamples();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    deleteSampleFromDataset(sampleId) {
      let data = new FormData();
      data.append("datasetId", this.datasetId);
      data.append("sampleId", sampleId);
      let config = {
        method: "post",
        maxBodyLength: Infinity,
        url: `${this.ip}/dataset-deletesample`,
        headers: {
          ...(data.getHeaders
            ? data.getHeaders()
            : { "Content-Type": "multipart/form-data" }),
        },
        data: data,
      };

      axios
        .request(config)
        .then((response) => {
          this.fetchSamples();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async fetchTranscript(id) {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/transcript?id=${id}`,
        headers: {},
      };

      var res = await axios.request(config);
      return res["data"];
    },
    async fetchAudio(id) {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/audio?id=${id}`,
        headers: {},
      };
      var res = await axios.request(config);
      return res["data"];
    },
    fetchData() {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/datasets`,
        headers: {},
      };

      axios
        .request(config)
        .then(async (response) => {
          this.datasets = response.data;
          this.datasetOptions = [];
          for (var dataset of this.datasets) {
            this.datasetOptions.push({
              label: dataset.name,
              value: dataset.id,
            });
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    fetchSamples() {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/dataset-samples?start_idx=${
          (this.currentPage - 1) * this.itemPerPage
        }&count=${this.itemPerPage}&id=${this.datasetId}`,
        headers: {},
      };

      axios
        .request(config)
        .then(async (response) => {
          var samples = response.data;
          for (var sample of samples) {
            var transcript = await this.fetchTranscript(sample.transcriptId);
            var audio = await this.fetchAudio(sample.audioId);
            this.transcripts[transcript.id] = transcript;
            this.audios[audio.id] = audio;
          }
          this.samples = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  beforeMount() {
    this.fetchData();
  },
  data() {
    return {
      addDialog: false,
      editDialog: false,
      searchSample: null,
      sampleName: "",
      samples: [],
      transcripts: {},
      audios: {},
      datasets: [],
      datasetOptions: [],
      datasetId: null,
      currentPage: 1,
      itemPerPage: 5,
      ip: this.$ip,
    };
  },
});
</script>
<style lang="sass"></style>
