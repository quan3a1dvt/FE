<template>
  <div>
    <div class="row">
      <div class="col">
        <q-select
          style="width: 200px"
          filled
          stack-label
          dense
          v-model="ttmId"
          :options="ttmOptions"
          label="Text to Mels"
          emit-value
          map-options
          class="q-mb-sm"
        />
        <q-select
          style="width: 200px"
          filled
          stack-label
          dense
          v-model="vocoderId"
          :options="vocoderOptions"
          label="Vocoder"
          emit-value
          map-options
          class="q-mb-sm"
        />
        <q-btn label="Select" color="teal" @click="SelectModel()"></q-btn>
      </div>
      <div class="col">
        <div class="flex">
          <q-select
            style="width: 200px"
            filled
            stack-label
            dense
            v-model="algorithmId"
            :options="algorithmOptions"
            label="Select Algorithm"
            emit-value
            map-options
            class="q-mb-sm"
          />
          <q-select
            class="q-ml-sm"
            filled
            stack-label
            dense
            style="width: 200px"
            v-model="datasetId"
            :options="datasetOptions"
            label="Select Dataset"
            emit-value
            map-options
          />
        </div>
        <q-input
          class="q-mb-sm"
          style="width: 240px"
          label="Enter model name"
          type="text"
          dense
          v-model="modelName"
        />
        <q-btn label="Train" color="teal" @click="Train()"></q-btn>
      </div>
      <!-- <div class="col">
        <div class="flex">
          <q-select
            style="width: 200px"
            filled
            stack-label
            dense
            v-model="ttmId"
            :options="ttmOptions"
            label="Select TTM Model"
            emit-value
            map-options
            class="q-mb-sm"
          />
          <q-select
            class="q-ml-sm"
            filled
            stack-label
            dense
            style="width: 200px"
            v-model="datasetId"
            :options="datasetOptions"
            label="Select Dataset"
            emit-value
            map-options
          />
        </div>
        <q-btn label="ReTrain" color="teal" @click="ReTrain()"></q-btn>
      </div> -->
    </div>
  </div>
</template>
<script>
import { defineComponent, ref } from "vue";
import axios from "axios";
import { onMounted } from "vue";

export default defineComponent({
  name: "ModelsManager",
  components: {},
  methods: {
    SelectModel() {
      let data = new FormData();
      console.log(this.ttmId);
      console.log(this.vocoderId);
      data.append("ttmId", this.ttmId);
      data.append("vocoderId", this.vocoderId);
      let config = {
        method: "post",
        maxBodyLength: Infinity,
        url: `${this.ip}/model`,
        headers: {
          ...(data.getHeaders
            ? data.getHeaders()
            : { "Content-Type": "multipart/form-data" }),
        },
        data: data,
      };

      axios
        .request(config)
        .then((response) => {})
        .catch((error) => {
          console.log(error);
        });
    },
    ReTrain() {},
    Train() {
      let data = new FormData();
      data.append("algorithmId", this.algorithmId);
      data.append("datasetId", this.datasetId);
      data.append("modelName", this.modelName);
      let config = {
        method: "post",
        maxBodyLength: Infinity,
        url: `${this.ip}/train`,
        headers: {
          ...(data.getHeaders
            ? data.getHeaders()
            : { "Content-Type": "multipart/form-data" }),
        },
        data: data,
      };

      axios
        .request(config)
        .then((response) => {})
        .catch((error) => {
          console.log(error);
        });
    },
    fetchTtm() {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/ttms`,
        headers: {},
      };

      axios
        .request(config)
        .then(async (response) => {
          this.ttms = response.data;
          this.ttmOptions = [];
          for (var ttm of this.ttms) {
            this.ttmOptions.push({
              label: ttm.name,
              value: ttm.id,
            });
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    fetchVocoder() {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/vocoders`,
        headers: {},
      };

      axios
        .request(config)
        .then(async (response) => {
          this.vocoders = response.data;
          this.vocoderOptions = [];
          for (var vocoder of this.vocoders) {
            this.vocoderOptions.push({
              label: vocoder.name,
              value: vocoder.id,
            });
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    fetchDataset() {
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
    fetchAlgorithm() {
      let config = {
        method: "get",
        maxBodyLength: Infinity,
        url: `${this.ip}/algorithms`,
        headers: {},
      };

      axios
        .request(config)
        .then(async (response) => {
          this.algorithms = response.data;
          this.algorithmOptions = [];
          for (var algorithm of this.algorithms) {
            this.algorithmOptions.push({
              label: algorithm.name,
              value: algorithm.id,
            });
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  beforeMount() {
    this.fetchTtm();
    this.fetchVocoder();
    this.fetchAlgorithm();
    this.fetchDataset();
  },
  data() {
    return {
      ttmId: null,
      vocoderId: null,
      ttms: [],
      ttmOptions: [],
      vocoders: [],
      vocoderOptions: [],
      datasets: [],
      datasetOptions: [],
      algorithms: [],
      algorithmOptions: [],
      modelName: "",
      algorithmId: null,
      datasetId: null,
      ip: this.$ip,
    };
  },
});
</script>
